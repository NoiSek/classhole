from util import hook
from collections import defaultdict

import random

channel = "#skywolf"

wolfcount = 2
seercount = 1

def wolves(players):
    shuffled = random.sample(players, len(players))
    return shuffled[wolfcount:], set(shuffled[:wolfcount])

def seers(players):
    if "Iguana" in players:
        
    shuffled = random.sample(players, len(players))
    return set(shuffled[seercount:]), set(shuffled[:seercount])


werewolfintro = """GAME START: You are a WEREWOLF.  You want to kill everyone while they sleep. Whatever happens, keep your identity secret.  Act natural!
The other %s %s.  Confer privately."""
werewolfnight = """NIGHT: As the villagers sleep, you must now decide who you want to kill.
You and the other were%s should discuss (privately) and choose a victim.
Please type 'kill <nickname>' (as a private message to me).
"""

seerintro = """GAME START: You're a villager, but also a SEER.  Later on, you'll get chances to learn whether someone is or isn't a werewolf.  Keep your identity secret, or the werewolves may kill you!"""
seernight = """NIGHT: In your dreams, you have the ability to see whether a certain person  is or is not a werewolf.
You must use this power now: please type 'see <nickname>' (as a private message to me) to learn about one living player's true identity."""

villagerintro = "GAME START: You're an ordinary villager."

chanintro = """GAME START: This is a game of paranoia and psychological intrigue.  Everyone in this group appears to be a common villager, but some of you are different. Some of you are actually evil werewolves, seeking to kill everyone while concealing their identity.
One (or more) of you are seers; you have the ability to learn whether a specific person is normal, seer, or werewolf.
As a community, your group objective is to weed out the werewolves and lynch them both, before you're all killed in your sleep."""

nightintro = """NIGHT: Darkness falls. Everyone relax and wait for morning... I'll tell you when night is over."""


dayintro = """DAY: Sunlight pierces the sky."""

daymurdered = """The village awakes to find the mutilated body of %s!!"""


murdertype  = """*** Examining the body, you see that this player was %s"""

murderseer  = """a SEER!"""
murderwolf  = """a WEREWOLF!"""
murderother = """a normal villager."""

class Werewolf:
    def __init__(self, starter, say, mode, msg):
        self.players = set([])
        self.dead = set([])
        self.wolves = None
        self.seers = None
        self.villagers = None
        self.state = 0
        self.votes = {}
        self.wolfvotes = {}
        self.sees = {}

        self.say = say
        self.mode = mode
        self.msg = msg

    def join(self, say, mode, name):
        if self.state == 0:
            self.players.add(name)
            self.mode("+v %s" % name)
            self.say("%s is now in the game!" % name)
        else:
            self.say("sorry, you can't join a running game")

    def start(self, say, msg, mode):
        if len(players) < minplayers:
            self.say("too few players! need at least %d" % minplayers)
            return
        self.say("A new game has begun! Please wait, assigning roles...")
        self.mode("+m")
        
        remaining, self.wolves = wolves(self.players)
        self.villagers, self.seers = seers(remaining)
        
         
        for i in self.wolves:
            types = "werewolves are" if len(self.wolves) > 2 else "werewolf is"
            others = list(self.wolves - set(i))
            if len(others) < 3:
                othertext = " and ".join(others)
            else:
                othertext = ", ".join(others[:-1])
                othertext = " and ".join([othertext, others[-1]])
            message = werewolfintro % (types, others)
            for line in message.split("\n"):
                self.msg(i, line)
        for i in self.seers:
            for line in seerintro.split("\n"):
                self.msg(i, line)
        for i in self.villagers:
            for line in villagerintro.split("\n"):
                self.msg(i, line)
        
        for line in chanintro:
            self.say(line)
        self.night()

    def whosleft(self, say):
        self.say("The following players are still alive: %s" % (", ".join(self.alive())))

    def alive(self):
        return self.wolves + self.villagers + self.seers

    def night(self, say):
        self.state = 1 
        for i in nightintro.split("\n"):
            self.say(i)
        for i in self.wolves:
            for line in werewolfnight.split("\n"):
                self.msg(i, line)
        for i in self.seers:
            for line in seernight.split("\n"):
                self.msg(i, line)
