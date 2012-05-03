from util import hook, timesince
from random import choice
import re

@hook.regex(r'ACTION slaps', re.I)
def antitrout(inp, nick='', chan='', say=None):
  responses = ["Goddamnit, %s, I'm serious. Stop it.", "Fucking stop it %s. It isn't funny.", "Come on now %s :/", "%s. Please, no more goddamn trout.", "Seriously, %s, stop it.", "Oi! Stop that shit %s D:<", "Dude. Stop with the trout %s.", "I think we've had enough of that already %s.", "Look, we've been over this %s, chill out with the trout."]
  say(choice(responses) % nick)