import urlparse

from util import hook, http
from random import choice
import urllib2


@hook.command
def down(inp, say=None):
    '''.down <url> -- checks to see if the site is down'''

    if 'http://' not in inp:
        inp = 'http://' + inp

    inp = 'http://' + urlparse.urlparse(inp).netloc

    req = urllib2.Request(inp)
    try:
        resp = urllib2.urlopen(req)
    except urllib2.URLError, e:
        responses = ["was hacked by the turks.", "is currently on fire, somewhere.", "was seized for loli.", "is making great contributions to our glorious dear leader.", "is running on a toaster...", "doesn't know that it's supposed to show things.", "has some anxiety issues.", "is playing cards with satan.", "is in Tahiti.", "got lost on the way to Walmart?"]
        say("Looks like %s %s" % (inp, choice(responses)))
    else:
        return inp + " is up."