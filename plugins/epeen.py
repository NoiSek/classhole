from util import hook
from datetime import datetime, timedelta
import time
import pyexec
import usertracking
import re
import urllib
import urllib2

def db_init(db):
  db.execute("create table if not exists epeen"
    "(chan, nick, count default 0, "
    "primary key (chan, nick))")
  db.commit()

  db.execute("create table if not exists epeen_lockout"
    "(nick, time real, "
    "primary key (nick))")
  db.commit()

def massage_epeen(massager, nick, db):
  try:
    db.execute("insert or ignore into epeen_lockout(nick, time)"
      " values(?,?)", (massager, time.time()))
    db.commit()
    db.execute("update epeen_lockout set time=? where nick=?", 
      (time.time(), massager))
    db.commit()

  except db.IntegrityError:
    return "Error adding row to epeen lockout table."

  try:
    db.execute("insert or ignore into epeen(nick, count)"
      " values(?, ?)", (nick, 0))
    db.execute("update epeen set count = count + 1 where nick=?", 
      ([nick]))
    db.commit()

  except db.IntegrityError:
    return "Failed to update epeen count."

def measure_epeen(name, db):
  return db.execute("select count from epeen where nick=?", ([name])).fetchone()

def isgd(inp):
  data = urllib.urlencode(dict(format="simple", url=inp))

  try:
      return urllib2.urlopen("http://is.gd/create.php", data).read()
  except Exception as e:
      return "Error: %s" % e

  return shortened

@hook.regex(r'^\+1 .+$', re.I)
@hook.regex(r'^A\+\+ .+$', re.I)
@hook.command("plusone")
def plusone(inp, nick='', chan='', db=None, say=None, input=None):
  "+1 [user] / .plusone [user] - Only usable once every 24 hours, increases a user's e-peen length."
  
  db_init(db)
  
  if(len(input.lastparam.split(" ")) > 2):
    return None
  
  username = input.lastparam.split(" ")[1]
  
  if(username.lower() == nick.lower()):
    return "Stroking yourself aint right, you know."

  last_time = db.execute("select time from epeen_lockout where nick=?", ([nick.lower()])).fetchone()

  if(last_time):
    if(datetime.now() - datetime.fromtimestamp(last_time[0]) < timedelta(days=1)):
      time_elapsed = timedelta(days=1) - (datetime.now() - datetime.fromtimestamp(last_time[0]))
      hours_elapsed, rem = divmod(time_elapsed.seconds, 3600)
      say("%i hours remaining until you can stroke again." % hours_elapsed) 
    else:
      massage_epeen(nick.lower(), username.lower(), db)
      db.commit()
      return "A++"
  else:
    massage_epeen(nick.lower(), username.lower(), db)
    db.commit()
    return "A++"

@hook.command("length")
def length(inp, nick='', chan='', db=None, say=None):
  ".length [user] - Show off the length of your e-peen."

  epeen_length = measure_epeen(inp.lower(), db)
  
  say("%i centimeters of hard earned glory." % epeen_length[0]) if epeen_length else say("%s is a sad, sad individual." % inp)

@hook.command("epeen")
def epeen(inp, nick='', chan='', db=None, say=None):
  ".epeen length [user] / .epeen stroke [user] / .epeen render [user] - Displays the length of a given epeen, strokes, or renders to screen."
  args = inp.split(" ")
  if args[0]:
    if(args[0] == "length"):
      if(len(args) == 2):
        return "%i centimeters of hard earned glory." % measure_epeen(args[1].lower(), db)[0] \
          if measure_epeen(args[1].lower(), db) else say("%s is a sad, sad individual." % args[1])
      else:
        return "%i centimeters of hard earned glory." % measure_epeen(nick.lower(), db)[0] \
          if measure_epeen(nick, db) else say("You've got nothing, buddy.")
    
    elif(args[0] == "stroke"):
      if(len(args) == 2):
        last_time = db.execute("select time from epeen_lockout where nick=?", ([nick.lower()])).fetchone()[0]

        if(last_time):
          if datetime.now() - datetime.fromtimestamp(last_time) < timedelta(days=1):
            time_elapsed = timedelta(days=1) - (datetime.now() - datetime.fromtimestamp(last_time))
            hours_elapsed, rem = divmod(time_elapsed.seconds, 3600)
            say("%i hours remaining until you can stroke again." % hours_elapsed) 
          else:
            massage_epeen(nick.lower(), args[1].lower(), db)
            db.commit()
            return "A++"
        else:
          massage_epeen(nick.lower(), args[1].lower(), db)
          db.commit()
          return "A++"

      else:
        return "What? ...yourself?"

    elif(args[0] == "render"):
      if(len(args) == 2):
        return isgd("http://firefi.re/epeen/?length=%i" % measure_epeen(args[1].lower(), db)[0]) \
        if measure_epeen(args[1].lower(), db) else say("%s has nothing to show downstairs." % args[1])

      else:
        return isgd("http://firefi.re/epeen/?length=%i" % measure_epeen(nick.lower(), db)[0]) \
        if measure_epeen(nick.lower(), db) else say("You're all washed up, chump.")

    else:
      return "%i centimeters of hard earned glory." % measure_epeen(args[0].lower(), db)[0] \
          if measure_epeen(args[0].lower(), db) else say("%s is a sad, sad individual." % args[0])

#@hook.command("droptables")
#def droptables(inp, db=None):
#  db.execute("drop table epeen")
#  db.execute("drop table epeen_lockout")
#  db.commit()