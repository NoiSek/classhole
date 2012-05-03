from util import hook
import re

@hook.regex(r'.*\s?dad\sare\syou.*?', re.I)
def space_core(inp, nick='', say=None):
  say("Yes %s, now we can be a family again." % nick)