from util import hook

import urllib2
import json

def get(symbol, exchange = "NASDAQ"):
  prefix = "http://finance.google.com/finance/info?client=ig&q="
  url = prefix + "%s:%s" % (exchange, symbol)
  u = urllib2.urlopen(url)
  content = u.read()

  obj = json.loads(content[3:])
  return obj[0]
        

@hook.command()
def stock(inp, say=None):
  ".stock <SYMBOL> / .squote <SYMBOL> <EXCHANGE> - Returns the current value of a given stock, default market is NASDAQ."

  values = inp.split(" ")
  if(len(values) > 1):
    quote = get(values[0], values[1])

  else:
    quote = get(values[0])

  say("%s:%s %s %s (%s) %s" % (quote['e'], quote['t'], quote['l_cur'], quote['c'], quote['cp'], quote['lt']))