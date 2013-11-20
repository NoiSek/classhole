'''ideone.py

I'm really pretty ashamed that I wrote this piece of shit. In for a penny in for a pound, though, right?
 - Noddy

'''

import re, time
from util import hook
from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import

@hook.command("exec")
@hook.command()
def ideone(inp, bot=None, say=None):
  ".ideone <language> <source> -- Executes code via ideone (Undoubtedly the shittiest API on earth). " \
  "Supported languages: http://ideone.com/faq#supported-languages. Most major languages have shortcuts (.rb, .java, .js, .php, etc.)"

  # Check if the input syntax is correct
  sane = re.match("^(\S*)\s(.*)$", inp)
  if sane:
    language, source = sane.groups()

  # List of languages because for some reason IdeOne doesn't name them reasonably instead.
  # Whenever possible, defaults to the more used of existing versions.
  languages = {
    "ada": 7,
    "assembler": 13,
    "assembly": 13,
    "asm": 13,        # Assembler
    "awk": 104,
    "gawk": 104,
    "mawk": 105,
    "bash": 28,
    "bc": 110,
    "bf": 12,         # Brainfuck
    "brainfuck": 12,
    "c": 11,
    "c#": 27,
    "c++": 44,
    "c++4.3.2": 41,
    "c++4.8.1": 1,
    "c++11": 44,
    "c99": 34,
    "clips": 14,
    "clojure": 111,
    "cobol": 118,
    "cobol85": 106,
    "clisp": 32,
    "d": 102,
    "erlang": 36,
    "f#": 124,
    "factor": 123,
    "falcon": 125,
    "forth": 107,
    "fortran": 5,
    "go": 114,
    "groovy": 121,
    "haskell": 21,
    "icon": 16,
    "intercal": 9,
    "java": 10,
    "java7": 55,
    "javascript": 35,
    "js": 35,         # Javascript
    "jsr": 35,        # Javascript Rhino
    "jss": 112,       # Javascript SpiderMonkey
    "lua": 26,
    "nemerle": 30,
    "nice": 25,
    "nimrod": 122,
    "node": 56,
    "nodejs": 56,
    "node.js": 56,
    "objc": 43, 
    "ocaml": 8,
    "octave": 127,
    "oz": 119,
    "pari": 57,       # PARI/GP
    "pascal": 22,
    "pascalfpc": 22,
    "pascalgpc": 2,
    "perl": 3,
    "perl6": 54,
    "php": 29,
    "pike": 19,
    "prolog": 108,
    "prologgnu": 108,
    "prologswi": 15,
    "py": 4,
    "python": 4,
    "py3": 116,
    "python3": 116,
    "r": 117,
    "rb": 17,         # Ruby
    "ruby": 17,
    "scala": 39,
    "scheme": 33,
    "smalltalk": 23,
    "sql": 40,
    "tcl": 38,
    "text": 62,
    "unlambda": 115,
    "vb": 101,        # VB.NET
    "vb.net": 101,
    "whitespace": 6
  }

  language_id = languages[language]

  # Get API key
  api_key = bot.config.get("api_keys", {}).get("ideone", None)
  if api_key is None:
    return "Error: Specify an API key in your bot config. See http://ideone.com for instructions. Format is user:apikey."

  user, key = api_key.split(":")

  # Fix IdeOne's broken ass SOAP implementation. Fuck SOAP and fuck everyone who uses it.
  imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
  imp.filter.add('http://ideone.com/api/1/service')
  doctor = ImportDoctor(imp)

  # Open connection to SOAP server
  url = 'http://ideone.com/api/1/service.wsdl'
  ide = Client(url, doctor=doctor)
  
  # Compile / Interpret source code
  response = ide.service.createSubmission(user, key, source, language_id, "", True, False)
  result_id = response[0][1].value[0]

  # What the fuck? Who wrote this fucking API? 
  # Get result, poll it until compiled and then print results.
  result = ide.service.getSubmissionDetails(user, key, result_id, False, False, True, True, False)
  
  status = result[0][7].value[0]
  output = result[0][11].value[0].replace('\n', ' ')
  stderr = result[0][12].value[0].replace('\n', ' ')

  while status not in [11, 12, 13, 15, 17, 19, 20]:
    time.sleep(1)

    result = ide.service.getSubmissionDetails(user, key, result_id, False, False, True, True, False)
    
    output = result[0][11].value[0].replace('\n', ' ')
    stderr = result[0][12].value[0].replace('\n', ' ')
    status = result[0][7].value[0]

  if not stderr:
    print output
    say(output)
    say("%s" % ("http://ideone.com/" + result_id))
  else:
    say("Error interpreting input. See %s" % ("http://ideone.com/" + result_id))
