from util import hook

import urllib2
import json
import re

def get(symbol, exchange = "NASDAQ"):
  prefix = "http://finance.google.com/finance/info?client=ig&q="
  url = prefix + "%s:%s" % (exchange, symbol)
  u = urllib2.urlopen(url)
  content = u.read()

  obj = json.loads(content[3:])
  return obj[0]
        

@hook.command()
def stock(inp, say=None):
  ".stock <SYMBOL> / .squote <EXCHANGE> <SYMBOL> - Returns the current value of a given stock, default market is NASDAQ."

  values = inp.split(" ")
  if(len(values) > 1):
    quote = get(values[1], values[0])

  else:
    quote = get(values[0])

  say("%s:%s %s %s (%s) %s" % (quote['e'], quote['t'], quote['l_cur'], quote['c'], quote['cp'], quote['lt']))

@hook.command()
def findsymbol(inp):
  ".findsymbol <name> / .findsymbol <exchange> <name> - Finds the Symbol name of a company, defaults to the NASDAQ exchange."

  values = inp.split(" ")

  if(len(values) > 1):
    market_match = re.match(r"^(nyse|nasdaq|amex)\s(.*)$", inp.lower(), re.I)
    exchange, name = market_match.groups()

    with open('symbols/%s.json' % exchange) as data_file:
      data = json.load(data_file)

      for company in data:
        if(name in company["Name"].lower()):
          return company["Symbol"]

  else:
    with open('symbols/nasdaq.json') as data_file:
      data = json.load(data_file)

      for company in data:
        if(values[0].lower() in company["Name"].lower()):
          return company["Symbol"]