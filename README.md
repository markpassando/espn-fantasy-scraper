# espn-fantasy-scraper
*Phase 1* - Version 1.0.0

## About
ESPN Fantasy Scraper is a web scraper that captures all possible useful stats from a NBA ESPN Fantasy League. It returns normalized JSON data that is accessible using a team name as a key. No sensitive data is scraped. 

## Phases
### Phase 1: (Complete 9/18/2018) 
- Dynamically scrape league data, accounts for varying league player size, scrapes any amount of categories.
- The `ESPNWebScraper.py` are contained endpoints, the `TerminalWrapper` is an terminal interface to interact with the web scraper.
- Can create JSON files or print the data to the console.
- Supports regular browser and headless browser mode.
### Phase 2: (In Progress) 
- Build a Django REST API Wrapper to interact with the web scraper.
### Phase 3:
- 1A: Build React Redux dashboard application for users to interact with league data.
- 1B: Create Bot to automatically set Fantasy lineup.
### Phase 4:
- Add auth to web app and allow users to save dashboard data.
- Collect stats from each scraped league and allow users to compare against global stats.

## Installation and Usage (mac) - Phase 1: 
Phase 1 is intended to work locally on a mac.
- **Pre-reqs for ESPN Fantasy League**
  - Must be an ESPN Fantasy League
  - Must be a Head to Head League (some endpoints support Roto.)
  - Must be a Categories League (some endpoints support Points)
  - Must have an even amount of teams (Some endpoints support odd teams)
- **Pre-reqs for Python**
  - Install Python 3.6X, this project uses Python 3.6.5
  - Install virtualenv - `pip install virtualenv`
- **Pre-reqs for Selenium**
  - Download and install browser drivers, currently using Chrome.
  - Chrome - https://sites.google.com/a/chromium.org/chromedriver/downloads
  - Place driver in /usr/local/bin
- **Create a Python env**
  - Inside the root directory of this application.
  - Create virtualenv - `python3 -m venv env`
  - Activate the virtualenv - `source env/bin/activate`
  - Install dependecies - `pip install -r requirements.txt`

## TerminalWrapper Usage
- activate the virtualenv `source env/bin/activate`
- The crawling script is located in `web-scraper/`, `cd web-scraper`

### Optional Arguments
- `-i` or `--league_id` = Add your league ID
- `-u` or `--username` = Add your username or email to ESPN Fantasy
- `-p` or `--password` = Add your password to ESPN Fantasy
- `--file` - Creates a json file with scraped data. (Will be default if neither `--file` or `--print` are passed)
- `--print` - Prints the return scraped data.
- `--headless` - Uses a Headless Chromebrowser (Default is a regular browser)

### Quick Demo Usage

For a Quick Demo, Default settings will scrape public league "6059" and create json files of scraped data.

`python TerminalWrapper.py`

### Real TerminalWrapper Usage

`python TerminalWrapper.py --league_id 2345 --username mark --password LeBronJames! --file --print --headless`

This will scrape the league `2345` with user `mark`, print to console and create a json file. 

Please ensure that your password is correct. If your league setting is public, you do not have to pass any credentials.

## License
[GNU General Public License v3.0](LICENSE.md)