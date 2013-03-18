from util import hook

@hook.command
def privmsg(inp, input=None, notice=None):
  if input.nick in input.bot.config["admins"]:
    notice(inp, True)
