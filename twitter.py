import re
import requests
import subprocess
import time

from datetime import datetime, timedelta
from os import environ

base_url = "https://api.twitter.com/2/"

bearer_token = environ.get("TWITTER_BEARER_TOKEN")
client_id = environ.get("TWITTER_OAUTH_CID")
client_secret = environ.get("TWITTER_OAUTH_CLIENT_SECRET")

# start_time,end_time,since_id,until_id,max_results,next_token,
#   expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': 'from:joshparktestacc','tweet.fields': 'created_at', 'max_results': '10'}

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def get_most_recent_tweet():
    response = requests.get(f'{base_url}tweets/search/recent', auth=bearer_oauth, params=query_params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    
    # text contents of most recent tweet
    r = response.json()
    return (r['data'][0]['text'], r['data'][0]['created_at'])

if __name__ == "__main__":
    last_tweet = None
    current_time = datetime.now().strftime('%H:%M:%S')
    print(f'starting at {current_time}')
    while True:
        time.sleep(1)
        tweet, utc_dt = get_most_recent_tweet()
        creation_time = datetime(*time.strptime(utc_dt, "%Y-%m-%dT%H:%M:%S.%fZ")[:6]) - timedelta(hours = 5)
        creation_time = creation_time.strftime('%H:%M:%S.%f')

        if tweet != last_tweet:
            phrase = re.search("\w+\d+ to \d+", str(tweet))
            if phrase:
                current_time = datetime.now().strftime('%H:%M:%S.%f')
                print(f'\ntweet created at {creation_time}, recieved at {current_time}')

                term = phrase.group().split()[0]
                subprocess.run(['osascript', 'text.applescript', term, '888222']) 

                current_time = datetime.now().strftime('%H:%M:%S.%f')
                print(f'sent {term} to 888222 at {current_time}\n')

            last_tweet = tweet