from util import hook

import urllib2
import json


def get_data(url = "https://mtgox.com/api/1/BTCUSD/ticker"):
  headers = { 'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13' }

  request = urllib2.Request(url, None, headers)
  content = urllib2.urlopen(request).read()
  content = json.loads(content)

  return content

def format_data(exchange, data):
  if(exchange == "mtgox"):
    return("MtGox // Current: %s, High: %s, Low: %s, Best Ask: %s, Volume: %s" % (data['return']['last']['display'], \
      data['return']['high']['display'], data['return']['low']['display'], data['return']['buy']['display'], \
      data['return']['vol']['display']))

  elif(exchange == "bitpay"):
    data = data[0]
    return("Bitpay // Current: $%s" % data['rate'])

  elif(exchange == "bitstamp"):
    return("BitStamp // Current: $%s, High: $%s, Low: $%s, Volume: %.2f BTC" % (data['last'], data['high'], data['low'], \
      float(data['volume'])))

@hook.command(autohelp = False)
def bitcoin(inp, say = None):
  ".bitcoin <exchange> -- gets current exchange rate for bitcoins from several exchanges, default is MtGox. Supports MtGox, Bitpay, and BitStamp."

  enabled_exchanges = [ "mtgox", "bitpay", "bitstamp" ]
  api_list = { "mtgox": "https://mtgox.com/api/1/BTCUSD/ticker", "bitpay": "https://bitpay.com/api/rates", \
   "bitstamp": "https://www.bitstamp.net/api/ticker/" }

  if(inp):
    if(inp.lower() in enabled_exchanges):
      values = get_data(api_list[inp.lower()])
      say(format_data(inp.lower(), values))

  else:
    values = get_data()
    say(format_data("mtgox", values))

