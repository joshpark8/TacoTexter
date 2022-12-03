import re
import requests
import subprocess
import time
import sys

from os import environ

base_url = "https://api.twitter.com/2/"

bearer_token = environ.get("TWITTER_BEARER_TOKEN")
client_id = environ.get("TWITTER_OAUTH_CID")
client_secret = environ.get("TWITTER_OAUTH_CLIENT_SECRET")

# start_time,end_time,since_id,until_id,max_results,next_token,
#   expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': 'from:ChipotleTweets','max_results': '10'}

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, query_params):
    response = requests.get(url, auth=bearer_oauth, params=query_params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def connect_to_endpoint2(url):
    response = requests.request('get', url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_most_recent_ID():
    json_response = connect_to_endpoint(f'{base_url}tweets/search/recent', query_params)
    ids = []
    return json_response['data'][0]['id']

def get_tweet():
    tweets = []
    id = get_most_recent_ID()
    r = connect_to_endpoint2(f'{base_url}tweets?ids={id}')['data'][0]
    return (id, r['text'])

if __name__ == "__main__":
    used_ids = []
    while True:
        time.sleep(1)
        id, tweet = get_tweet()
        if (id not in used_ids):
            phrase = re.search("\w+\d+ to \d+", str(tweet))
            if phrase:
                split_phrase = phrase.group().split()
                term = split_phrase[0]
                subprocess.run(['osascript', 'text.applescript', term]) 
                print(f'\nsent {term} to 888222')
        print('.', end='')
        sys.stdout.flush()
        used_ids.append(id)