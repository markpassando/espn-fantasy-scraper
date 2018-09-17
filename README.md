# espn-fantasy-scraper
*Phase 1* - Version 0.1.0


## Phases
### Phase 1: (Current)
- Create webscraper to scrape all possible useful stats from a NBA ESPN Fantasy League and return normalized data that is accessible using team name as a key. No sensitive data is scraped.
- Dynamically scrape league data, accounts for varying league player size, scrapes any amount of categories.
- Intended to work locally via a python script.
### Phase 2:
- Build a Django REST API to interact with the webscraper. The webscraper will now sit behind an API endpoint.
### Phase 3:
- 1A: Build React Redux dashboard application for users to interact with league data.
- 1B: Create Bot to automatically set Fantasy lineup.
### Phase 4:
- Add auth to web app and allow users to save dashboard data.
- Collect stats from each scraped league and allow users to compare against.

## Installation and Usage (mac) - Phase 1: 
Phase 1 is intended to work locally on a mac.
- **Pre-reqs for Python**
  - Install virtualenv - `pip install virtualenv`
- **Pre-reqs for Selenium**
  - Download and install browser drivers, currently using Chrome for development, will soon support headless browser PhantomJS for speed.
  - Chrome - https://sites.google.com/a/chromium.org/chromedriver/downloads
  - Place driver in /usr/local/bin
- **Create a Python env**
  - Inside the root directory of this application.
  - Create virtualenv - `python3 -m venv env`
  - Activate the virtualenv - `source env/bin/activate`
  - Install dependecies - `pip install -r requirements.txt`

## Usage
The crawling script is located in `selenium/index.py`

`cd selenium`

### Arguments
- `-i` or `--league_id` = Add your league ID
- `-u` or `--username` = Add your username or email to ESPN Fantasy
- `-p` or `--password` = Add your password to ESPN Fantasy
- `--file` - Creates a json file with scraped data. (Will be default if neither `--file` or `--print` are passed)
- `--print` - Prints the return scraped data.

### Simple Demo Usage

Default settings will scrape public league "6059" and create a json file of scraped data.

`python index.py`

### Real Example Usage

`python index.py --league_id 2345 --username mark --password LeBronJames! --file --print`

This will scrape the league `2345` with user `mark`, print to console and create a json file.

Please ensure that your password is correct. If your league setting is public, you do not have to pass any credentials.

## License
[GNU General Public License v3.0](LICENSE.md)