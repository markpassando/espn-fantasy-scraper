"""
Usage:
  index.py [-i LEAGUE_ID -u USERNAME -p PASSWORD]

Options:
  -i --league_id=<league_id>     ESPN League ID [default: 6059].
  -u --username=<username>       ESPN Login Username [default: ].
  -p --password=<password>       ESPN Login Password [default: ].
"""
import sys
import re
import json
import time
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__)

BASE_URL = "http://fantasy.espn.com/basketball/league/"
LEAGUE_ID = arguments['--league_id']
USERNAME = arguments['--username']
PASSWORD = arguments['--password']
TIMEOUT = 30

print('\n<---------------> espn-fantasy-scraper initializing <--------------->')
print(f"LEAGUE_ID: '{LEAGUE_ID}'")
print(f"USERNAME: '{USERNAME}'")
print(f"PASSWORD: '{PASSWORD}'")

# Helpers TODO: put in utils.py
def strip_special_chars(string):
  return re.sub('[^A-Za-z0-9]+', '', string)

def PygmentsPrint(dict_obj):
  json_obj = json.dumps(dict_obj, sort_keys=True, indent=4)
  print(highlight(json_obj, JsonLexer(), TerminalFormatter()))

def checkIfAuthRequired():
  # Selenium throws NoSuchElementException if it can not find an element
  try:
    login_button = browser.find_element_by_link_text('You need to login')

    if login_button.text == 'You need to login':
      print(f"LOG - Attempting to Log In with User: '{USERNAME}''")
      try:
        # Wait for iframe to load and switch to it
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//iframe[@id='disneyid-iframe']")))
        browser.switch_to.frame(browser.find_element_by_id('disneyid-iframe'))
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']")))

        # Get elements
        email_input_element = browser.find_elements_by_xpath("//input[@type='email']")[0]
        password_input_element = browser.find_elements_by_xpath("//input[@type='password']")[0]
        login_button_element = browser.find_elements_by_xpath("//button[text()='Log In']")[0]

        # Attempt Login
        email_input_element.send_keys(USERNAME)
        password_input_element.send_keys(PASSWORD)
        login_button_element.click()
        print(f"LOG - Successfully logged in for user '{USERNAME}'!")

        # Needs to sleep, logging in too fast causing ESPN to ask to log in again
        time.sleep(3)
        return True
      except Exception as e:
        print(f"ERROR - {e}")
  except NoSuchElementException as e:
    print('LOG - User does not require Auth')
    return False
    
driver = webdriver.ChromeOptions()
# driver.add_argument(" — incognito")
browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=driver)
browser.get(f"{BASE_URL}standings?leagueId={LEAGUE_ID}&seasonId=2018")

def getLeagueStandings():
  try:
      print('LOG - Attempting to Crawl League Standings Page')
      WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='Nav__Primary__Branding Nav__Primary__Branding--espn']")))
      if checkIfAuthRequired():
        browser.get(f"{BASE_URL}standings?leagueId={LEAGUE_ID}")
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Standings']")))

      teams_elements = browser.find_elements_by_xpath("//tr[@class='Table2__tr Table2__tr--md Table2__odd']")
      header = browser.find_elements_by_xpath("//tr[@class='Table2__header-row Table2__tr Table2__even']")
      league_categories = header[4].text.split('\n')

      # Teams elements returns an array of values from 4 different tables
        # 1/4 - Team Standings
        # 2 - 4 ESPN is combining 3 columns of tables into one
        # 2/4 The team names
        # 3/4 Season States
        # 4/4 Team Transactions
      amount_of_teams = int(len(teams_elements)/4)
      teams_standings = teams_elements[0:amount_of_teams]
      season_stats_teams_names = teams_elements[amount_of_teams:amount_of_teams * 2]
      season_stats = teams_elements[amount_of_teams * 2:amount_of_teams * 3]
      transaction_stats = teams_elements[amount_of_teams * 3:amount_of_teams * 4]
      teams = {}

      # Build teams dictionary with standing stats
      for team in teams_standings:
        team_vals = team.text.split('\n')
        teams[team_vals[0]] = {
          "name": team_vals[0],
          "wins": int(team_vals[1]),
          "losses": int(team_vals[2]),
          "ties": int(team_vals[3]),
          "percent": team_vals[4],
          "season_stats": {}
        }

        try:
          teams[team_vals[0]]["games_behind"] = team_vals[5]
        except IndexError:
          pass
          # Leagues that are complete will not have "games behind" field

      # Build Up Season Stats
      for i in range(amount_of_teams):
        current_team = season_stats_teams_names[i].text.split('\n')[1]
        category_stat_values = season_stats[i].text.split('\n')
        current_season_stats = {}

        # Dynamically pull the categories and stats
        for j in range(len(league_categories)):
          category = strip_special_chars(league_categories[j])
          current_season_stats[category] = category_stat_values[j]
          current_season_stats['transactions'] = int(transaction_stats[j].text.split('\n')[1])

        # Assign it back to the team
        teams[current_team]["season_stats"] = current_season_stats
      print('\n<---------------> League Standings and Season Stats <--------------->')
      PygmentsPrint(teams)
  except TimeoutException as e:
      print("Timed out waiting for page to load")
      browser.quit()

# Get Scores
def getWeekScores ():
  print('LOG - Attempting to Crawl League Scoreboard Page')
  browser.get(f"{BASE_URL}scoreboard?leagueId={LEAGUE_ID}&matchupPeriodId=1")
  try:
      WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='Nav__Primary__Branding Nav__Primary__Branding--espn']")))

      if checkIfAuthRequired():
        browser.get(f"{BASE_URL}scoreboard?leagueId={LEAGUE_ID}&matchupPeriodId=1")
        WebDriverWait(browser, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Scoreboard']")))

      week_dropdown_selector = browser.find_elements_by_class_name('dropdown__select')[0]
      weeks = week_dropdown_selector.text.split('\n')
      amount_of_weeks = len(weeks)
      scoreboard = {}
      
      for index, week in enumerate(weeks):
        # Change Page to week
        Select(week_dropdown_selector).select_by_visible_text(week)
        week_number = index + 1
        weeks_score = {}
        scores = []
        teams_elements = browser.find_elements_by_xpath("//div[@class='ScoreCell__TeamName ScoreCell__TeamName--short truncate']")
        cats_score_elements = browser.find_elements_by_xpath("//div[@class='ScoreCell__Score h4 clr-gray-01 fw-bold tar ScoreCell_Score--scoreboard pl2']")
        scores_elements = browser.find_elements_by_class_name('Table2__tbody')

        # Get Week's score for each team
        for score in scores_elements:
          all_scores = score.text.split('\n')
          amount_of_cats = int(len(all_scores) / 2)
          scores.append(all_scores[:amount_of_cats])
          scores.append(all_scores[amount_of_cats:])

        for i in range(len(teams_elements)):
          team_name = teams_elements[i].text
          team_number = i + 1

          if len(cats_score_elements) == 0:
            # Week has not been played yet
            cats_score = [0,0,0]
          else:
            cats_score = cats_score_elements[i].text.split('-')

          # Find opponent
          if team_number % 2 == 0:
            opponent = teams_elements[i - 1]
          else:
            opponent = teams_elements[i + 1]
          
          # Build team dictionary
          weeks_score[team_name] = {
            "scores": scores[i],
            "opponent": opponent.text,
            "cats_won": int(cats_score[0]),
            "cats_lost": int(cats_score[1]),
            "cats_tied": int(cats_score[2])
          }

        # Add Data for an entire week
        scoreboard[f"week{week_number}"] = {
          "week": week_number,
          "date": week,
          "scores": weeks_score
        }

      print('\n<---------------> Scoreboard of Entire Season <--------------->')
      PygmentsPrint(scoreboard)
      browser.quit()
  except TimeoutException as e:
      print("Timed out waiting for page to load")
      browser.quit()

# getLeagueStandings()
getWeekScores()