import locale
import re
import time

from util import hook, http
from random import choice


locale.setlocale(locale.LC_ALL, '')

youtube_re = (r'(?:youtube.*?(?:v=|/v/)|youtu\.be/|yooouuutuuube.*?id=)'
              '([-_a-z0-9]+)', re.I)

base_url = 'http://gdata.youtube.com/feeds/api/'
url = base_url + 'videos/%s?v=2&alt=jsonc'
search_api_url = base_url + 'videos?v=2&alt=jsonc&max-results=1'
video_url = "http://youtube.com/watch?v=%s"

responses = ["\x02BIG BITTY TITCHES", "FUCKING YOUTUBE \x02GODDAMN", "ALLAH AKHBAR", "PRAISE SATAN", "DEATH TO THE INFIDELS", "GOD BLESS SUDAN", "LOOK AT THIS SHIT", "GIF WITH SOUND", "HARDCORE XBAWKS CHAMPILOON"]

def get_video_description(vid_id):
    j = http.get_json(url % vid_id)

    if j.get('error'):
        return

    j = j['data']

    out = '\x02%s\x02' % j['title']

    if 'contentRating' in j:
        out += ' - \x034NSFW\x02'

    return out


@hook.regex(*youtube_re)
def youtube_url(match, bot=None, say=None):
    if "autoreply" in bot.config and not bot.config["autoreply"]:
        return
    say("%s: %s" % (choice(responses), get_video_description(match.group(1))))


@hook.command('y')
@hook.command
def youtube(inp, say=None):
    '.youtube <query> -- returns the first YouTube search result for <query>'

    j = http.get_json(search_api_url, q=inp)

    if 'error' in j:
        return 'error performing search'

    if j['data']['totalItems'] == 0:
        return 'no results found'

    vid_id = j['data']['items'][0]['id']

    say(choice(responses) + ": " + get_video_description(vid_id) + " - " + video_url % vid_id)