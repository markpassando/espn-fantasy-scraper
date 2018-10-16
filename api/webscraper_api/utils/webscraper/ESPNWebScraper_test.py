import pytest
from ESPNWebScraper import ESPNWebScraper

@pytest.fixture(scope='class')
def ScraperInstance(request):
    '''Returns a Scrapper Instance of a completed 2018 league'''
    options = {
      'league_id': '6059',
      'username': 'mpassando',
      'password': 'ScrapeMeBaby1MoreTime',
      'year': '2018',
      'headless': False
    }
    request.cls.instance = ESPNWebScraper(options)

@pytest.mark.usefixtures('ScraperInstance')
class TestESPNWebScraper:
    def test_getLeagueStandings(self):
        standings = self.instance.getLeagueStandings()
        self.instance.closeBrowser()
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

    def test_getWeekScores(self):
        scores = self.instance.getWeekScores()
        self.instance.closeBrowser()
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

    def test_getDraftRecap(self):
        draft = self.instance.getDraftRecap()
        self.instance.closeBrowser()
        assert len(draft) == 156, "Should be 156 players drafted"
        # Check the 9th Pick
        # NOTE: This data changes with the player. Lebron Played on CLE in 2018 but displays lakers.
        assert draft[8]['draft_position'] == 9, "Should be the 9th pick"
        assert draft[8]['draft_round'] == 1, "Should be 1st round"
        assert draft[8]['draft_team'] == 'Banana Boat', "Should have the correct team"
        assert draft[8]['name'] == 'LeBron James', "Should be LeBron James"
        assert draft[8]['position'] == 'SF', "Should have proper player Position"
        assert draft[8]['team'] == 'LAL', "Should have proper Team"

    def test_getAllRosters(self):
        rosters = self.instance.getAllRosters()
        self.instance.closeBrowser()
        assert len(rosters) == 12, "Should be 12 teams"
        assert len(rosters['RIPPIN PIPPENS']) == 14, "Should have 14 players including IR slot"
        assert rosters['RIPPIN PIPPENS'][3]['name'] == 'Kevin Durant', "Should be Kevin Durant"
        assert rosters['RIPPIN PIPPENS'][3]['team'] == 'GS', "Should be Golden State"
        KD_position = rosters['RIPPIN PIPPENS'][3]['position']
        assert len(KD_position) == 2, "Kevin Durant should play 2 positions"
        assert 'SF' in KD_position, "Kevin Durant should play SF"
        assert 'PF' in KD_position, "Kevin Durant should play PF"
        assert len(rosters['RIPPIN PIPPENS'][7]['position']), "Enes Kanter should play 1 position"
        assert 'C' in rosters['RIPPIN PIPPENS'][7]['position'], "Kanter should play C"

    def test_getTransactionCount(self):
        transactions = self.instance.getTransactionCount()
        self.instance.closeBrowser()
        assert len(transactions) == 12, "Should have 12 teams"
        assert transactions['Charlie Sanders']['acq'] == 5, "Check acq"
        assert transactions['Charlie Sanders']['active'] == 582, "Check active"
        assert transactions['Charlie Sanders']['drop'] == 93, "Check drop"
        assert transactions['Charlie Sanders']['ir'] == 7, "Check ir"
        assert transactions['Charlie Sanders']['trade'] == 0, "Check trade"
