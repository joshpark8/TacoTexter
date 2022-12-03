
import requests
from requests_oauthlib import OAuth2Session
from os import environ

base_url = "https://api.twitter.com/2/"
redirect_uri = "https://joshpark.dev/tweetkinetics"
oauth_url = f'{base_url}oauth2/'

bearer_token = environ.get("TWITTER_BEARER_TOKEN")
client_id = environ.get("TWITTER_OAUTH_CID")
client_secret = environ.get("TWITTER_OAUTH_CLIENT_SECRET")
scope = [
    "tweet.fields=non_public_metrics,organic_metrics",
    "expansions=attachments.media_keys&media.fields=non_public_metrics,organic_metrics",
]

# start_time,end_time,since_id,until_id,max_results,next_token,
#   expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': 'from:johngreen','tweet.fields': 'author_id'}
twitter = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
authorization_url, state = twitter.authorization_url(oauth_url)

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    # print(response.status_code) # uncomment if needed to debug
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def connect_to_endpoint2(url):
    response = requests.get(url, auth=bearer_oauth)
    # print(response.status_code) # uncomment if needed to debug
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_recent_IDs():
    json_response = connect_to_endpoint(f'{base_url}tweets/search/recent', query_params)
    ids = []
    for tweet in json_response['data']:
        ids.append(tweet['id'])
    return ids

def get_likes():
    likes = []
    for id in get_recent_IDs():
        r = connect_to_endpoint2(f'{base_url}tweets?ids={id}&tweet.fields=public_metrics')['data'][0] # &expansions=attachments.media_keys&media.fields=public_metrics')['data'][0]
        likes.append(r['public_metrics']['like_count'])
    return likes

def get_tweets():
    tweets = []
    for id in get_recent_IDs():
        r = connect_to_endpoint2(f'{base_url}tweets?ids={id}&tweet.fields=public_metrics')['data'][0] # &expansions=attachments.media_keys&media.fields=public_metrics')['data'][0]
        tweets.append(r['text'])
    return tweets

'''def get_impressions():
    tweets = []
    for id in get_recent_IDs():
        r = connect_to_endpoint2(f'{search_url}tweets/{id}?tweet.fields=non_public_metrics,organic_metrics&media.fields=non_public_metrics,organic_metrics&expansions=attachments.media_keys') # &expansions=attachments.media_keys&media.fields=public_metrics')['data'][0]
        tweets.append(r)
        return tweets
    return tweets'''

if __name__ == "__main__":
    tweets = get_tweets()
    likes = get_likes()
    # impressions = get_impressions() # not public
    # print(f'{impressions}\n')
    for like, tweet in zip(likes, tweets):
        print(f'{like}: {tweet}')
