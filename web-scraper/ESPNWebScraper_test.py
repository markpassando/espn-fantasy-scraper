import pytest
from ESPNWebScraper import ESPNWebScraper

@pytest.fixture
def ScraperInstance():
    '''Returns a complete league Scrapper Instance'''
    options = {
      'league_id': '6059',
      'username': 'REQUIRES USERNAME',
      'password': 'REQUIRES PASSWORD',
      'year': '2018',
      'headless': False
    }
    return ESPNWebScraper(options)

def test_getLeagueStandings(ScraperInstance):
    standings = ScraperInstance.getLeagueStandings()
    ScraperInstance.closeBrowser()
    assert len(standings) == 12, "Should be 12 teams"
    assert 'Banana Boat' in standings, "Banana Boat Team should exist"
    assert standings['No Curry No Worry']['wins'] == 12, "Check wins"
    assert standings['No Curry No Worry']['losses'] == 8, "Check loses"
    assert standings['No Curry No Worry']['ties'] == 0, "Check ties"
    assert len(standings['No Curry No Worry']['season_stats']) == 10, "Season stats should have 10 fields"
    assert standings['Albert Kim and The NY Rangers']['season_stats']['3PM'] == '805', "Check 3PM"
    assert standings['Albert Kim and The NY Rangers']['season_stats']['AST'] == '2801', "Check AST"
    assert standings['Albert Kim and The NY Rangers']['season_stats']['BLK'] == '499', "Check BLK"
    assert standings['Albert Kim and The NY Rangers']['season_stats']['FG'] == '.481', "Check FG"
    assert standings['Albert Kim and The NY Rangers']['season_stats']['FT'] == '.741', "Check FT"
    assert standings['Albert Kim and The NY Rangers']['season_stats']['PTS'] == '11886', "Check PTS"
    assert standings['Albert Kim and The NY Rangers']['season_stats']['REB'] == '4928', "Check REB"
    assert standings['Albert Kim and The NY Rangers']['season_stats']['STL'] == '737', "Check STL"
    assert standings['Albert Kim and The NY Rangers']['season_stats']['TO'] == '1575', "Check TO"
    assert standings['Albert Kim and The NY Rangers']['season_stats']['transactions'] == 2, "Check transactions"

def test_getWeekScores(ScraperInstance):
    scores = ScraperInstance.getWeekScores()
    ScraperInstance.closeBrowser()
    assert len(scores) == 23, "There are 23 games in the 2018 season"
    # Check the week
    assert scores['week20']['week'] == 20, "Find week 20"
    assert scores['week17']['date'] == "Week 17 (Feb 5 - 11)", "Check date"
    assert len(scores['week1']['scores']) == 12, "Should be 12 teams"
    # Check Team
    assert scores['week6']['scores']['Walker, Charlotte Rangr']['opponent'] == 'Albert Kim and The NY Rangers', "Check opponent"
    assert scores['week6']['scores']['Walker, Charlotte Rangr']['cats_won'] == 6, "Check cats_won"
    assert scores['week6']['scores']['Walker, Charlotte Rangr']['cats_lost'] == 3, "Check cats_lost"
    assert scores['week6']['scores']['Walker, Charlotte Rangr']['cats_tied'] == 0, "Check cats_tied"
    assert len(scores['week6']['scores']['Walker, Charlotte Rangr']['scores']) == 9, "Should be 9 categories"
    # Check box score
    assert scores['week23']['scores']['The Unibrowmber']['scores']['3PM'] == '48', "Check 3PM"
    assert scores['week23']['scores']['The Unibrowmber']['scores']['AST'] == '155', "Check AST"
    assert scores['week23']['scores']['The Unibrowmber']['scores']['BLK'] == '38', "Check BLK"
    assert scores['week23']['scores']['The Unibrowmber']['scores']['FG'] == '0.462', "Check FG"
    assert scores['week23']['scores']['The Unibrowmber']['scores']['FT'] == '0.829', "Check FT"
    assert scores['week23']['scores']['The Unibrowmber']['scores']['PTS'] == '651', "Check PTS"
    assert scores['week23']['scores']['The Unibrowmber']['scores']['REB'] == '289', "Check REB"
    assert scores['week23']['scores']['The Unibrowmber']['scores']['STL'] == '51', "Check STL"
    assert scores['week23']['scores']['The Unibrowmber']['scores']['TO'] == '66', "Check TO"
