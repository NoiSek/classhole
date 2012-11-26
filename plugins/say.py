import re
from util import hook


@hook.command
def say(inp, say=None, input=None):
  if input.nick in input.bot.config["admins"]:
    say(inp)
