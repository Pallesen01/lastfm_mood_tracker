import requests

info_file = "api_info.txt"
f = open(info_file)
application_name = f.readline().split(':')[1].strip()
api_key = f.readline().split(':')[1].strip()
shared_secret = f.readline().split(':')[1].strip()
registered_user = f.readline().split(':')[1].strip()
f.close()

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': registered_user}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = api_key
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


payload = {
    'method': 'chart.gettopartists',
}
print(lastfm_get(payload))
