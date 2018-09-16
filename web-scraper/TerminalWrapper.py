"""
Usage:
  index.py [-i self.LEAGUE_ID -u USERNAME -p PASSWORD --file --print]

Options:
  -i --league_id=<league_id>     ESPN League ID [default: 6059].
  -u --username=<username>       ESPN Login Username [default: ].
  -p --password=<password>       ESPN Login Password [default: ].
  --file                         Setting to create JSON file [default: false].
  --print                        Setting print data to console [default: false].

"""
import os
import json
import datetime

# Local Dependencies
from ESPNWebScraper import ESPNWebScraper
from utils import (
  PygmentsPrint
)

# Third Party Dependencies
from docopt import docopt

# Collect Terminal Arguments
if __name__ == '__main__':
    arguments = docopt(__doc__)

LEAGUE_ID = arguments['--league_id']
USERNAME = arguments['--username']
PASSWORD = arguments['--password']
OUTPUT_SETTINGS = {
  "file": arguments['--file'],
  "print": arguments['--print']
}
if OUTPUT_SETTINGS['file'] == False and OUTPUT_SETTINGS['print'] == False:
  OUTPUT_SETTINGS['file'] = True

print('\n<---------------> espn-fantasy-scraper - TerminalWrapper initializing <--------------->')
print(f"LEAGUE_ID was set to '{LEAGUE_ID}'")
print(f"USERNAME was set to '{USERNAME}'")
print(f"PASSWORD was set to  '{PASSWORD}'")
print("\n")

class TerminalWrapper:
  def __init__(self, league_id, username, password, output_settings):
    self.LEAGUE_ID = league_id
    self.USERNAME = username
    self.PASSWORD = password
    self.OUTPUT_SETTINGS = output_settings
    self.ESPNWebScraper = ESPNWebScraper(self.LEAGUE_ID, self.USERNAME, self.PASSWORD)

  def closeBrowser(self):
    self.ESPNWebScraper.closeBrowser()
  
  def timeScrape(self, start_time, end_time, name):
    print(f"INFO - TerminalWrapper - {name} Crawl Completed: Total Time {str(end_time - start_time)}")

  def json_output(self, data, file=None):
    if self.OUTPUT_SETTINGS['print']:
      PygmentsPrint(data)

    if self.OUTPUT_SETTINGS['file']:
      if not os.path.exists('json'):
        os.mkdir('json')

      script_dir = os.path.dirname(__file__)
      file_path = os.path.join(script_dir, f"../json/{file}.json")
      with open(file_path, 'w') as outfile:
          json.dump(data, outfile)
      print(f"INFO - SUCCESS - TerminalWrapper - Successfully Created json file: '{file_path}'")

  def getLeagueStandings(self):
    start_time = datetime.datetime.now()
    standings = self.ESPNWebScraper.getLeagueStandings()
    self.json_output(standings, 'standings')
    end_time = datetime.datetime.now()
    self.timeScrape(start_time, end_time, 'League Standings')

  def getDraftRecap(self):
    start_time = datetime.datetime.now()
    draft_recap = self.ESPNWebScraper.getDraftRecap()
    self.json_output(draft_recap, 'draft_recap')
    end_time = datetime.datetime.now()
    self.timeScrape(start_time, end_time, 'Draft Recap')

  def getAllRosters(self):
    start_time = datetime.datetime.now()
    rosters = self.ESPNWebScraper.getAllRosters()
    self.json_output(rosters, 'rosters')
    end_time = datetime.datetime.now()
    self.timeScrape(start_time, end_time, 'All Rosters')

  def getWeekScores(self):
    start_time = datetime.datetime.now()
    scores = self.ESPNWebScraper.getWeekScores()
    self.json_output(scores, 'scores')
    end_time = datetime.datetime.now()
    self.timeScrape(start_time, end_time, 'All Weekly Scores')

  def getTransactionCount(self):
    start_time = datetime.datetime.now()
    scores = self.ESPNWebScraper.getTransactionCount()
    self.json_output(transactions, 'transactions')
    end_time = datetime.datetime.now()
    self.timeScrape(start_time, end_time, 'Transactions Count')

# Start TerminalWrapper
start_time = datetime.datetime.now()
terminalwrapper = TerminalWrapper(LEAGUE_ID,USERNAME, PASSWORD, OUTPUT_SETTINGS)
terminalwrapper.getLeagueStandings()
terminalwrapper.getDraftRecap()
terminalwrapper.getWeekScores()
terminalwrapper.getAllRosters()
terminalwrapper.getTransactionCount()
terminalwrapper.closeBrowser()
end_time = datetime.datetime.now()
print('<---------------> TerminalWrapper COMPLETE <--------------->')
print(f"Total Time: {str(end_time - start_time)}")