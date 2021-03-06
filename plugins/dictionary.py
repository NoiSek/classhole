import re

from util import hook, http


@hook.command('u')
@hook.command('ud')
@hook.command
def urban(inp):
  '''.u/.urban <phrase> [#] -- looks up <phrase> with [#] definition on urbandictionary.com'''

  args = inp.split(" ")

  # Look for a number to cycle through definitions, optionally
  if(len(args) > 1):
    try:
      int(args[-1])
      number = int(args.pop())
      index = number - 1
    except(ValueError):
      index = 0

  else:   
    index = 0

  args = " ".join(args)

  url = 'http://www.urbandictionary.com/define.php'
  page = http.get_html(url, term=args)
  words = page.xpath("//*[@id='entries']/div/span")
  defs = page.xpath("//div[@class='definition']")

  if not defs:
    return 'no definitions found'

  # Put together a string from the xpath requests.
  out = words[index].text.strip() + ': ' + ' '.join(
      defs[index].text.split())

  if len(out) > 400:
    out = out[:out.rfind(' ', 0, 400)] + '...'

  return out


# define plugin by GhettoWizard & Scaevolus
@hook.command('dictionary')
@hook.command
def define(inp):
  ".define/.dictionary <word> -- fetches definition of <word>"

  url = 'http://ninjawords.com/'

  h = http.get_html(url + http.quote_plus(inp))

  definition = h.xpath('//dd[@class="article"] | '
                       '//div[@class="definition"] |'
                       '//div[@class="example"]')

  if not definition:
    return 'No results for ' + inp

  def format_output(show_examples):
    result = '%s: ' % h.xpath('//dt[@class="title-word"]/a/text()')[0]

    correction = h.xpath('//span[@class="correct-word"]/text()')
    if correction:
      result = 'definition for "%s": ' % correction[0]

    sections = []
    for section in definition:
      if section.attrib['class'] == 'article':
        sections += [[section.text_content() + ': ']]
      elif section.attrib['class'] == 'example':
        if show_examples:
            sections[-1][-1] += ' ' + section.text_content()
      else:
        sections[-1] += [section.text_content()]

    for article in sections:
      result += article[0]
      if len(article) > 2:
        result += ' '.join('%d. %s' % (n + 1, section)
                            for n, section in enumerate(article[1:]))
      else:
        result += article[1] + ' '

    synonyms = h.xpath('//dd[@class="synonyms"]')
    if synonyms:
      result += synonyms[0].text_content()

    result = re.sub(r'\s+', ' ', result)
    result = re.sub('\xb0', '', result)
    return result

  result = format_output(True)
  if len(result) > 450:
    result = format_output(False)

  if len(result) > 450:
    result = result[:result.rfind(' ', 0, 450)]
    result = re.sub(r'[^A-Za-z]+\.?$', '', result) + ' ...'

  return result


@hook.command('e')
@hook.command
def etymology(inp):
    ".e/.etymology <word> -- Retrieves the etymology of chosen word"

    url = 'http://www.etymonline.com/index.php'

    h = http.get_html(url, term=inp)

    etym = h.xpath('//dl')

    if not etym:
        return 'No etymology found for ' + inp

    etym = etym[0].text_content()

    etym = ' '.join(etym.split())

    if len(etym) > 400:
        etym = etym[:etym.rfind(' ', 0, 400)] + ' ...'

    return etym
