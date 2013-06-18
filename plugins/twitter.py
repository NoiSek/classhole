import random
import re
import json
import urllib
import urllib2
from time import strptime, strftime

from util import hook

def authenticate(api_key):
  oauth_url = "https://api.twitter.com/oauth2/token"
  authorization_string = "Basic %s" % api_key

  headers = { 
    "User-agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13", 
    "Authorization" : authorization_string,
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
  }
  parameters = { "grant_type" : "client_credentials" }
  
  request = urllib2.Request(oauth_url, urllib.urlencode(parameters), headers)
  response = urllib2.urlopen(request).read()
  response = json.loads(response)

  return response['access_token']

def get_data(url, bearer_token):
  authorization_string = "Bearer %s" % bearer_token

  headers = { 
    "User-agent" : "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13", 
    "Authorization" : authorization_string,
  }
  
  request = urllib2.Request(url, None, headers)
  response = urllib2.urlopen(request).read()
  response = json.loads(response)

  return response

@hook.command
def twitter(inp, bot=None, say=None):
  ".twitter <user> [n] / .twitter <id> / .twitter #<hashtag> / .twitter @<user> -- " \
  "Returns Twitter statuses based on different queries."

  # Get API key from Bot config, warn otherwise
  api_key = bot.config.get("api_keys", {}).get("twitter", None)
  if api_key is None:
    return "Error: Specify an API key in your bot config. See https://dev.twitter.com/docs for instructions."

  # Prepare API URL's
  base_url = 'https://api.twitter.com/1.1'
  api_search = base_url + "/search/tweets.json"
  api_timeline = base_url + "/statuses/user_timeline.json"

  # Set for later
  searching_hashtag = False
  index = 0

  # What are we looking for?
  user_id = re.match(r'^(\d+)\s(\d+)?$', inp)
  username = re.match(r'^\w{1,15}$', inp, re.I)
  username_incremented = re.match(r'^(\w{1,15})\s+(\d+)$', inp)
  hashtag = re.match(r'^#\w+$', inp)

  if user_id:
    url = api_timeline + "?user_id=%s" % user_id.group(1)
    index = user_id.group(2)

  elif username:
    url = api_timeline + "?screen_name=%s" % inp

  elif username_incremented:
    # Get just enough tweets to grab the requested one
    count = 10
    while count <= int(username_incremented.group(2)):
      count += 10

    url = api_timeline + "?screen_name=%s&count=%i" % (username_incremented.group(1), count)
    index = username_incremented.group(2)

  elif hashtag:
    url = api_search + "?q=%23" + inp[1:]
    searching_hashtag = True

  else:
    return 'error: invalid request'

  # Attempt to authenticate with Twitter using API key
  bearer_token = authenticate(api_key)

  # Attempt to query Twitter
  data = get_data(url, bearer_token)

  # Choose a random tweet from collection and print it if we're searching hashtags
  if searching_hashtag:
    tweet = random.choice(data['statuses'])
    say("@%s: %s" % (tweet['user']['screen_name'], tweet['text']))

  # Pick selected tweet and print
  if index > 1:
    index = int(index) - 1

  tweet = data[index]
  
  username = tweet['user']['screen_name']
  status = tweet['text']
  date = strftime('%a, %b %d %l:%M %p', strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))


  say("\x02@%s - %s\x02: %s" % (username, date, status))
