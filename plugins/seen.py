" seen.py: written by sklnd in about two beers July 2009"

import time

from util import hook, timesince


def db_init(db):
    "check to see that our db has the the seen table and return a connection."
    db.execute("create table if not exists seen(name, time, quote, chan, "
                 "primary key(name, chan))")
    db.commit()


@hook.singlethread
@hook.event('PRIVMSG', ignorebots=False)
def seeninput(paraml, input=None, db=None, bot=None):
    db_init(db)
    db.execute("insert or replace into seen(name, time, quote, chan)"
        "values(?,?,?,?)", (input.nick.lower(), time.time(), input.msg,
            input.chan))
    db.commit()


@hook.command
def seen(inp, nick='', chan='', db=None, input=None, say=None):
    ".seen <nick> -- Tell when a nickname was last in active in irc"

    if input.conn.nick.lower() == inp.lower():
        # user is looking for us, being a smartass
        say("YES THIS IS DOG")

    elif inp.lower() == nick.lower():
        say("That'd be you, dear.")

    else:
        db_init(db)

        last_seen = db.execute("select name, time, quote from seen where name"
                               " like ? and chan = ?", (inp, chan)).fetchone()

        if last_seen:
            reltime = timesince.timesince(last_seen[1])
            if last_seen[0] != inp.lower():  # for glob matching
                inp = last_seen[0]
            say('%s was last seen %s ago saying: %s' % \
                        (inp, reltime, last_seen[2]))
        else:
            say("User not in database")
