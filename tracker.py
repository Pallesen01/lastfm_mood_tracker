import requests, json, datetime, shelve, time

#Setup Variables
unix_day = 86400
unix_timezone = 46800
info_file = "lastfm_api.txt"
f = open(info_file)
application_name = f.readline().split(':')[1].strip()
api_key = f.readline().split(':')[1].strip()
shared_secret = f.readline().split(':')[1].strip()
registered_user = f.readline().split(':')[1].strip()
f.close()

def lastfm_get(payload):
    """Perfoms a lastfm api request"""
    # define headers and URL
    headers = {'user-agent': registered_user}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = api_key
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response.json()

def lastfm_gettracks(user, from_unix, to_unix):
    """Gets all track data for between givin time"""
    payload = {
        'method': 'user.getweeklytrackchart',
        'user':user,
        'from':from_unix,
        'to':to_unix,
        'limit':200
    }
    response = lastfm_get(payload)
    return response

def get_unix_time(year,month,day):
    """Formats a date to unix time"""
    return int(str((datetime.datetime(year,month,day,0,0).timestamp()) + unix_timezone).split('.')[0])


startdate = get_unix_time(2020, 1, 1)
print('Starting...')

shelf = shelve.open('hashtable')
hashtable = shelf['hashtable']

start = time.time()
days_count = {}
i = 0
while startdate+(i*unix_day) < time.time():    
    date_unix = startdate+(i*unix_day)
    data = lastfm_gettracks(registered_user, date_unix, date_unix+unix_day)
    track_list = data['weeklytrackchart']['track']
    count_dict = {}
    for track in track_list:
        key = track['name'].lower().replace(' ','') + '_' + track['artist']['#text'].lower().replace(' ','')
        values = hashtable.get_value(key)
        for value in values:
            count_dict[value] = count_dict.get(value, 0) + int(track['playcount'])
    days_count[date_unix] = count_dict
    i+=1

threshold = 10
#Output formatted data to file
f = open("output.txt", "w")
f.write('')
f.close()
f = open("output.txt", "a")
for unix in days_count:
    date = time.gmtime(unix)
    f.write("Date "+str(date.tm_mday)+'/'+str(date.tm_mon)+'/'+str(date.tm_year)+':''\n')
    for playlist in days_count[unix]:
        f.write(playlist + ': ' + str(days_count[unix][playlist]))
        if playlist != 'Other' and days_count[unix][playlist] > threshold:
            f.write('***\n')
        else:
            f.write('\n')
    f.write('-'*15 + '\n')
f.close()
time_taken = time.time() - start
print("Done in {:.3f} seconds".format(time_taken))
