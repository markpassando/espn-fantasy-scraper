import pytest
from ESPNWebScraper import ESPNWebScraper

@pytest.fixture
def ScraperInstance():
    '''Returns a Wallet instance with a zero balance'''
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
    assert len(standings) == 12, "There should be 12 teams"
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