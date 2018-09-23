
import time
import math
import datetime
import json

# Local Dependencies
from utils import (
  strip_special_chars
)

# Third Party Dependencies
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

class ESPNWebScraper:
  def __init__(self, options):
    self.__dict__ = options
    self.BASE_URL = "http://fantasy.espn.com/basketball/league/"
    self.ROSTER_URL = "http://fantasy.espn.com/basketball/"
    self.TIMEOUT = 30
    self.is_browser_open = False

    if 'league_id' in options:
      self.LEAGUE_ID = options['league_id']
    else:
      raise TypeError("'league_id' is a required field!")

    self.USERNAME = '' if not 'username' in options else options['username']
    self.PASSWORD = '' if not 'password' in options else options['password']
    self.headless = False if not 'headless' in options else options['headless']
    self.YEAR = '' if not 'year' in options else (f"&seasonId={options['year']}")
    self.startBrowser()
    
  def startBrowser(self):
    chrome_options = webdriver.ChromeOptions()
    if self.headless:
      chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    self.browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=chrome_options,
      service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
    self.is_browser_open = True
    print(f"INFO - browser webdriver Instance has been OPENED.")

  def closeBrowser(self):
    if self.is_browser_open:
      self.is_browser_open = False
      self.browser.quit()
      print(f"INFO - browser webdriver Instance has been CLOSED.")

  def checkIsBrowserOpen(self):
    if not self.is_browser_open:
      self.startBrowser()

  def returnErrorJson(self, errMsg, status):
    error = {
          "error": {
            "status_code": str(status),
            "message": str(errMsg)
          }
        }

    return json.dumps(error)

  def checkIfAuthRequired(self):
    # Selenium throws NoSuchElementException if it can not find an element
    try:
      login_button = self.browser.find_element_by_link_text('You need to login')

      if login_button.text == 'You need to login':
        print(f"INFO - Attempting to Log In with User: '{self.USERNAME}'")

        # Wait for iframe to load and switch to it
        WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//iframe[@id='disneyid-iframe']")))
        self.browser.switch_to.frame(self.browser.find_element_by_id('disneyid-iframe'))
        WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']")))

        # Get elements
        email_input_element = self.browser.find_elements_by_xpath("//input[@type='email']")[0]
        password_input_element = self.browser.find_elements_by_xpath("//input[@type='password']")[0]
        login_button_element = self.browser.find_elements_by_xpath("//button[text()='Log In']")[0]

        # Attempt Login
        email_input_element.send_keys(self.USERNAME)
        password_input_element.send_keys(self.PASSWORD)
        login_button_element.click()

        # Check Login
        time.sleep(3)
        try:
          self.browser.find_element_by_xpath("//div[@class='banner message-error message ng-isolate-scope state-active']")
          print("ERROR - Username or Password is Incorrect")
          self.closeBrowser()
          raise ValueError("Username or Password is Incorrect")
        except NoSuchElementException as e:
          print(f"INFO - Successfully logged in for user '{self.USERNAME}'!")

        # Needs to sleep, logging in too fast is causing ESPN to ask to log in again
        time.sleep(3)
        return True

    except NoSuchElementException as e:
      print('INFO - User does not require Auth')
      return False
  
  def getDraftRecap(self):
    try:
        print('INFO - Attempting to Draft Recap Page')
        self.checkIsBrowserOpen()
        self.browser.get(f"{self.BASE_URL}draftrecap?leagueId={self.LEAGUE_ID}{self.YEAR}")
        WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='Nav__Primary__Branding Nav__Primary__Branding--espn']")))

        if self.checkIfAuthRequired():
          self.browser.get(f"{self.BASE_URL}draftrecap?leagueId={self.LEAGUE_ID}{self.YEAR}")
          WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='Table2__Title']")))

        round_elements = self.browser.find_elements_by_xpath("//div[@class='Table2__Title']")
        player_elements = self.browser.find_elements_by_xpath("//div[@class='jsx-2810852873 table--cell Player']")
        team_drafted_elements = self.browser.find_elements_by_xpath("//a[@class='flex items-center team--link inline-flex v-mid']")
        draft= []

        for i, player in enumerate(player_elements):
          player_info = player.text.split(', ')

          player_obj = {
            "draft_position": i + 1,
            "draft_team": team_drafted_elements[i].text,
            "draft_round": math.ceil((i + 1) / 12)
          }

          # Check if Draft has not occured yet
          if len(player_info) == 1:
            player_obj["name"] = ''
            player_obj["team"] = ''
            player_obj["position"] = ''
          else:
            # Draft is complete
            player_obj["name"] = player_info[0][:-4] #Remove team
            player_obj["team"] = player_info[0][-3:] #Remove player name
            player_obj["position"] = player_info[1]

          draft.append(player_obj)

        print('INFO - SUCCESS! - Draft Recap has been scraped.\n')
        return draft
    except TimeoutException as e:
        error_msg = "ERROR - Timed out waiting for page to load"
        print(error_msg)
        self.closeBrowser()
        return self.returnErrorJson(error_msg, 504)
    except Exception as e:
        self.closeBrowser()
        print(f"ERROR - {e}")
        return self.returnErrorJson(e, 500)

  def getLeagueStandings(self):
    try:
        print('INFO - Attempting to Crawl League Standings Page')
        self.checkIsBrowserOpen()
        self.browser.get(f"{self.BASE_URL}standings?leagueId={self.LEAGUE_ID}{self.YEAR}")
        WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='Nav__Primary__Branding Nav__Primary__Branding--espn']")))
        if self.checkIfAuthRequired():
          self.browser.get(f"{self.BASE_URL}standings?leagueId={self.LEAGUE_ID}{self.YEAR}")
          WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Standings']")))

        teams_elements = self.browser.find_elements_by_xpath("//tr[@class='Table2__tr Table2__tr--md Table2__odd']")
        header = self.browser.find_elements_by_xpath("//tr[@class='Table2__header-row Table2__tr Table2__even']")
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

            try:
              current_season_stats['transactions'] = int(transaction_stats[j].text.split('\n')[1])
            except IndexError as e:
              # New leagues will not have the "LAST" column, no games have started
              current_season_stats['transactions'] = int(transaction_stats[j].text.split('\n')[0])

          # Assign it back to the team
          teams[current_team]["season_stats"] = current_season_stats

        print('INFO - SUCCESS! - League Standings and Season Stats have been scraped.\n')
        return teams
    except TimeoutException as e:
        error_msg = "ERROR - Timed out waiting for page to load"
        print(error_msg)
        self.closeBrowser()
        return self.returnErrorJson(error_msg, 504)
    except Exception as e:
        self.closeBrowser()
        print(f"ERROR - {e}")
        return self.returnErrorJson(e, 500)

  def getRoster(self, team_id):
    try:
        print(f"INFO - Attempting crawl to Roster Page for team_id '{team_id}'")
        self.checkIsBrowserOpen()
        self.browser.get(f"{self.ROSTER_URL}team?leagueId={self.LEAGUE_ID}{self.YEAR}&teamId={team_id}")
        WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='Nav__Primary__Branding Nav__Primary__Branding--espn']")))

        if self.checkIfAuthRequired():
          self.browser.get(f"{self.ROSTER_URL}team?leagueId={self.LEAGUE_ID}{self.YEAR}&teamId={team_id}")
          WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='jsx-2947067311 player-column-table2 justify-start pa0 flex items-center player-info']")))

        player_elements = self.browser.find_elements_by_xpath("//div[@class='jsx-2947067311 player-column-table2 justify-start pa0 flex items-center player-info']")
        team_name = self.browser.find_elements_by_xpath("//span[@class='teamName truncate']")[0].text
        players = []

        for player in player_elements:
          player_info = player.text.split('\n')

          # Check if Player plays multiple Positions
          if ', ' in player_info[2]:
            player_info[2] = player_info[2].split(', ')
          else:
            # Normalize Data - Keep player position in array
            player_info[2] = [player_info[2]]

          player_obj = {
            "name": player_info[0],
            "team": player_info[1],
            "position": player_info[2]
          }

          players.append(player_obj)

        return players, team_name
    except TimeoutException as e:
        print("ERROR - Timed out waiting for page to load")
        self.closeBrowser()

  def getAllRosters(self):
    try:
        print('INFO - Attempting crawl to All Rosters Page')
        self.checkIsBrowserOpen()
        self.browser.get(f"{self.BASE_URL}rosters?leagueId={self.LEAGUE_ID}{self.YEAR}")
        WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='Nav__Primary__Branding Nav__Primary__Branding--espn']")))

        if self.checkIfAuthRequired():
          self.browser.get(f"{self.BASE_URL}rosters?leagueId={self.LEAGUE_ID}{self.YEAR}")
          WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='btn roster-btn btn--alt']")))

        team_links_elements = self.browser.find_elements_by_xpath("//a[@class='btn roster-btn btn--alt']")
        team_ids = []
        rosters = {}

        for team_link in team_links_elements:
          url = team_link.get_attribute("href")
          id = url.split('&teamId=')[1]
          team_ids.append(id)

        for team_id in team_ids:
          roster, team_name = self.getRoster(team_id)
          rosters[team_name] = roster

        print('INFO - SUCCESS! - All Rosters have been scraped.\n')
        return rosters
    except TimeoutException as e:
        error_msg = "ERROR - Timed out waiting for page to load"
        print(error_msg)
        self.closeBrowser()
        return self.returnErrorJson(error_msg, 504)
    except Exception as e:
        self.closeBrowser()
        print(f"ERROR - {e}")
        return self.returnErrorJson(e, 500)

  def getWeekScores(self):
    try:
        print('INFO - Attempting to Crawl League Scoreboard Page')
        self.checkIsBrowserOpen()
        self.browser.get(f"{self.BASE_URL}scoreboard?leagueId={self.LEAGUE_ID}{self.YEAR}&matchupPeriodId=1")
        WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='Nav__Primary__Branding Nav__Primary__Branding--espn']")))

        if self.checkIfAuthRequired():
          self.browser.get(f"{self.BASE_URL}scoreboard?leagueId={self.LEAGUE_ID}{self.YEAR}&matchupPeriodId=1")
          WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Scoreboard']")))

        week_dropdown_selector = self.browser.find_elements_by_class_name('dropdown__select')[0]
        category_elements = self.browser.find_elements_by_xpath("//tr[@class='Table2__header-row Table2__tr Table2__even']")[1].text.split('\n')
        
        weeks = week_dropdown_selector.text.split('\n')
        amount_of_weeks = len(weeks)
        scoreboard = {}
        categories = []

        for cat in category_elements:
          categories.append(strip_special_chars(cat))

        for index, week in enumerate(weeks):
          # Change Page to week
          Select(week_dropdown_selector).select_by_visible_text(week)
          week_number = index + 1
          weeks_score = {}
          scores = []
          teams_elements = self.browser.find_elements_by_xpath("//div[@class='ScoreCell__TeamName ScoreCell__TeamName--short truncate']")
          cats_score_elements = self.browser.find_elements_by_xpath("//div[@class='ScoreCell__Score h4 clr-gray-01 fw-bold tar ScoreCell_Score--scoreboard pl2']")
          scores_elements = self.browser.find_elements_by_class_name('Table2__tbody')

          # Get Week's score for each team
          for score in scores_elements:
            all_scores = score.text.split('\n')
            amount_of_cats = int(len(all_scores) / 2)
            scores.append(all_scores[:amount_of_cats])
            scores.append(all_scores[amount_of_cats:])

          for i in range(len(teams_elements)):
            team_name = teams_elements[i].text
            team_number = i + 1

            if len(cats_score_elements) == 0 or cats_score_elements[i].text == '':
              # Week has not been played yet 
              cats_score = [0,0,0]
            else:
              cats_score = cats_score_elements[i].text.split('-')

            # Find opponent
            if team_number % 2 == 0:
              opponent = teams_elements[i - 1]
            else:
              opponent = teams_elements[i + 1]
            
            # Build Team Score Object for Week
            score_for_week = {}
            for j in range(amount_of_cats):
              score_for_week[categories[j]] = scores[i][j]

            # Build team dictionary
            weeks_score[team_name] = {
              "scores": score_for_week,
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

        print('INFO - SUCCESS! - All Weekly Scores have been scraped.\n')
        return scoreboard
    except TimeoutException as e:
        error_msg = "ERROR - Timed out waiting for page to load"
        print(error_msg)
        self.closeBrowser()
        return self.returnErrorJson(error_msg, 504)
    except Exception as e:
        self.closeBrowser()
        print(f"ERROR - {e}")
        return self.returnErrorJson(e, 500)

  def getTransactionCount(self):
    try:
        print('INFO - Attempting to Crawl Transaction Count Page')
        self.checkIsBrowserOpen()
        self.browser.get(f"{self.BASE_URL}transactioncounter?leagueId={self.LEAGUE_ID}{self.YEAR}")
        WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='Nav__Primary__Branding Nav__Primary__Branding--espn']")))
        if self.checkIfAuthRequired():
          self.browser.get(f"{self.BASE_URL}transactioncounter?leagueId={self.LEAGUE_ID}{self.YEAR}")
          WebDriverWait(self.browser, self.TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Transaction Counter']")))

        team_elements = self.browser.find_elements_by_xpath("//tr[@class='Table2__tr Table2__tr--sm Table2__odd']")
        transactions = {}

        # Build teams dictionary with transaction counts
        for team in team_elements:
          team_vals = team.text.split('\n')
          transactions[team_vals[0]] = {
            "trade": int(team_vals[1]),
            "acq": int(team_vals[2]),
            "drop": int(team_vals[3]),
            "active": int(team_vals[4]),
            "ir": int(team_vals[5])
          }

        print('INFO - SUCCESS! - League Transactions have been scraped.\n')
        return transactions
    except TimeoutException as e:
        error_msg = "ERROR - Timed out waiting for page to load"
        print(error_msg)
        self.closeBrowser()
        return self.returnErrorJson(error_msg, 504)
    except Exception as e:
        self.closeBrowser()
        print(f"ERROR - {e}")
        return self.returnErrorJson(e, 500)


# Use for Local Testing
# start_time = datetime.datetime.now()
# options = {
#   'league_id': '6059',
#   'username': 'user',
#   'password': 'pw',
#   'headless': False,
#   'year': '2018'
# }
# espn_scraper = ESPNWebScraper(options)
# standings = espn_scraper.getLeagueStandings()
# scores = espn_scraper.getWeekScores()
# draft_recap = espn_scraper.getDraftRecap()
# rosters = espn_scraper.getAllRosters()
# transactions = espn_scraper.getTransactionCount()
# espn_scraper.closeBrowser()
# end_time = datetime.datetime.now()
# print(f"Crawl Completed: Total Time {str(end_time - start_time)}")