import re
import random

from util import hook


@hook.command
def say(inp):
    ".say <words> -- Echos what you said"

    return inp
