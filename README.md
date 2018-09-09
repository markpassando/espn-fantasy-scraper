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

## Phase 1: Installation and Usage (mac)
Phase 1 is intended to work locally on a mac.
- Download and install browser drivers
 - Chrome - https://sites.google.com/a/chromium.org/chromedriver/downloads
- Place driver in /usr/local/bin
- Create `virtualenv espn`
- `pip install selenium`
- Start virtualenv `workon espn`
- Run with `python index.py`