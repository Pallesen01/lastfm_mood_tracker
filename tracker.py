import requests, json, datetime

#Setup Variables
unix_day = 86400
unix_timezone = 43200
info_file = "api_info.txt"
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
        'to':to_unix
    }
    response = lastfm_get(payload)
    return response

def get_unix_time(year,month,day):
    """Formats a date to unix time"""
    return int(str((datetime.datetime(year,month,day,0,0).timestamp()) - unix_timezone).split('.')[0])

unixtime = get_unix_time(2020, 10, 31)

data = lastfm_gettracks('sparks_of_fire',unixtime , unixtime+unix_day)

track_list = data['weeklytrackchart']['track']


#Output raw data to file
f = open("output.txt", "w")
f.write(json.dumps(data, sort_keys=True, indent=4))
f.close()
print("Done")