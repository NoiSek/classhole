from util import hook
import random
import time
nextgreeting = None
findnext()
def findnext():
    global nextgreeting
    nextgreeting = time.time() + (1500) + (random.random() * 6000)
@hook.event("JOIN")
def join(inp, input=None):
    if input.nick == input.conn.nick:
        time.sleep(random.random())
	input.say("hi everyone!")
    elif time.time() > nextgreeting:
        time.sleep(random.random()+0.1)
        input.say("%s%s" % (input.nick.upper(), "!"*random.randint(1,5)))
        time.sleep(1.0+(random.random()*2.0))
        input.me("glomps %s" % random.choice([input.nick.lower(), input.nick.lower(), input.nick, input.nick.capitalize()]))
	findnext()
