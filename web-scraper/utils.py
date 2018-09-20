import re
import json

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

def strip_special_chars(string):
  return re.sub('[^A-Za-z0-9]+', '', string)

def PygmentsPrint(dict_obj):
  json_obj = json.dumps(dict_obj, sort_keys=True, indent=4)
  print(highlight(json_obj, JsonLexer(), TerminalFormatter()))