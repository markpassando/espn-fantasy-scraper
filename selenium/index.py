import re
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
user = ""
pwd = ""

# Helpers TODO: put in utils.py
def strip_special_chars(string):
  return re.sub('[^A-Za-z0-9]+', '', string)

driver = webdriver.ChromeOptions()
# driver.add_argument(" — incognito")
browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=driver)
browser.get("http://fantasy.espn.com/basketball/league/standings?leagueId=6059")
timeout = 30

def getLeagueStandings ():
  try:
      WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='Nav__Primary__Branding Nav__Primary__Branding--espn']")))

      teams_elements = browser.find_elements_by_xpath("//tr[@class='Table2__tr Table2__tr--md Table2__odd']")
      header = browser.find_elements_by_xpath("//tr[@class='Table2__header-row Table2__tr Table2__even']")
      # print(header)

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
          "games_behind": team_vals[5],
          "season_stats": {}
        }

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

      # print(titles)
  except TimeoutException:
      print("Timed out waiting for page to load")
      browser.quit()

# Get Scores
def getWeekScores ():
  browser.get("http://fantasy.espn.com/basketball/league/scoreboard?leagueId=6059&matchupPeriodId=1")
  try:
      WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='Nav__Primary__Branding Nav__Primary__Branding--espn']")))
      teams_elements = browser.find_elements_by_xpath("//div[@class='ScoreCell__TeamName ScoreCell__TeamName--short truncate']")
      cats_score_elements = browser.find_elements_by_xpath("//div[@class='ScoreCell__Score h4 clr-gray-01 fw-bold tar ScoreCell_Score--scoreboard pl2']")
      scores_elements = browser.find_elements_by_class_name('Table2__tbody')
      week_dropdown_selector = browser.find_elements_by_class_name('dropdown__select')[0]

      weeks = week_dropdown_selector.text.split('\n')

      weeks_score = {}
      scores = []

      # Get Week's score for each team
      for score in scores_elements:
        all_scores = score.text.split('\n')
        amount_of_cats = int(len(all_scores) / 2)
        scores.append(all_scores[:amount_of_cats])
        scores.append(all_scores[amount_of_cats:])

      for i in range(len(teams_elements)):
        team_name = teams_elements[i].text
        team_number = i + 1
        cats_score = cats_score_elements[i].text.split('-')

        # Find opponent
        if team_number % 2 == 0:
          opponent = teams_elements[i - 1]
        else:
          opponent = teams_elements[i + 1]
        
        weeks_score[team_name] = {
          "scores": scores[i],
          "opponent": opponent.text,
          "cats_won": int(cats_score[0]),
          "cats_lost": int(cats_score[1]),
          "cats_tied": int(cats_score[2])
        }

      print('done')
      browser.quit()
  except TimeoutException:
      print("Timed out waiting for page to load")
      browser.quit()

# getLeagueStandings()
getWeekScores()