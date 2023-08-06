from .models import *
from .parser import Parser

class Controller():
  def __init__(self):
    pass

  @classmethod
  def main(self):
    Database.connect()

    source = ui.get('source')
    parser = Parser(source)
    parser.parse()

    Database.disconnect()