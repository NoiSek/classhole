from util import hook

import urllib2
import json
import re

def get(symbol, exchange = 'NASDAQ'):
  prefix = "http://finance.google.com/finance/info?client=ig&q="
  url = prefix + "%s:%s" % (exchange, symbol)

  try:
    u = urllib2.urlopen(url)
    
  except urllib2.HTTPError:
    return False

  content = u.read()
  obj = json.loads(content[3:])

  return obj[0]
        
def findsymbol(name, exchange = 'NASDAQ'):
  with open('symbols/%s.json' % exchange.lower()) as data_file:
    data = json.load(data_file)

    for company in data:
      if(name in company['Name'].lower()):
        return company['Symbol']

    return False

@hook.command()
def stock(inp, say=None):
  ".stock <symbol> / .stock <exchange>:<symbol> - Returns the current value of a given stock, default market is NASDAQ. Automatically searches for symbols given company names."

  # Match with regex to SYMBOL, or EXCHANGE:SYMBOL
  find_exchange = re.search("^(.+):(.+)$", inp, re.I)
  exchange, company = find_exchange.groups() if find_exchange else ["NASDAQ", inp]
  symbol = ""

  # Convert to a symbol if the symbol provided is actually a multi-word name.
  if(len(company.split(" ")) > 1):
    symbol = findsymbol(company, exchange)

    if(not symbol):
      return "Unable to match your company name to a symbol."

  else:
    symbol = company

  quote = get(symbol, exchange)

  # Try converting to a symbol, in the case of one word company names like "Google"
  if(not quote):
    symbol = findsymbol(symbol, exchange)
    quote = get(symbol, exchange)

    if(not quote):
      return "Unable to match your company name to a symbol."

  say("%s:%s %s %s (%s) %s" % (quote['e'], quote['t'], quote['l_cur'], quote['c'], quote['cp'], quote['lt']))

@hook.command('findsymbol')
def findsymbol_command(inp, say=None):
  ".findsymbol <name> / .findsymbol <exchange>:<name> - Finds the Symbol name of a company, defaults to the NASDAQ exchange."

  # Match with regex to COMPANY NAME, or EXCHANGE:COMPANY NAME
  find_exchange = re.search("^(.+):(.+)$", inp, re.I)
  if(find_exchange):
    exchange, name = find_exchange.groups()  

    valid_market = re.match(r"^(nyse|nasdaq|amex)$", exchange, re.I)
    if(not valid_market):
      return "Not a valid exchange. Valid exchanges are NYSE, NASDAQ, and AMEX."
    
    with open('symbols/%s.json' % exchange) as data_file:
      data = json.load(data_file)

      for company in data:
        if(name in company['Name'].lower()):
          return "%s:%s" % (company['Symbol'], company['Name'])

      return "Couldn't find that company."

  else:
    name = inp
    with open('symbols/nasdaq.json') as data_file:
      data = json.load(data_file)

      for company in data:
        if(name.lower() in company['Name'].lower()):
          return "%s:%s" % (company['Symbol'], company['Name'])

      return "Couldn't find that company."