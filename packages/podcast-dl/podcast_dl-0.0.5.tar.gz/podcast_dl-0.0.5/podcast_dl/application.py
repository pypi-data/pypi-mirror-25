from .parser import Parser
from .models import *
from .config import DBFILE

class Application():
  def __init__(self):
    pass

  @classmethod
  def run(self):
    Application.connect()

    source = ui.get('source')
    parser = Parser(source)
    parser.parse()

    Application.disconnect()

  @classmethod
  def connect(self):
    if ui.get('drop'):
      os.remove(DBFILE)
      open(DBFILE, 'w+')

    tables = [Download, Enclosure, Episode, Podcast]
    db.connect()
    db.create_tables(tables, safe=True)

  @classmethod
  def disconnect(self):
    db.close()