# RedditScrape

Low-Orbital-Tractor-Beam designed to be a simple platform for creating Reddit-interaction projects in a modular and extensible way.

![Banner for Reddit Scraper](https://i.imgur.com/OAjhkqo.png)

## Aims

1. Create a bullet-proof Reddit connection and authentication module
2. Have a central codebase for creating ad-hoc and repeat scrapers
3. Create a module that other apps, espcially bots, can use to connect to Reddit
4. Add an API for remote use.
5. Build a modular system where a single, tested, pull-request could viably add an entire new feature.
6. Create a CLI, web, desktop, and API front-end for the system.

## Structure

```bash
..
├── RedditScrape
│   ├── __init__.py
|   ├── .env
│   ├── .gitignore
│   ├── LICENSE
│   ├── README.md
│   ├── main.py
│   └── src
│       ├── __init__.py
│       ├── auth.py
│       ├── data
│       │   └── settings.json
│       └── routing.py
├── data
```

## Installation

1. Clone the repo
2. Edit the .env file with your Reddit API credentials. The system currently uses the PRAW library, so you'll need to create a Reddit app and get your credentials from there. The .env file should look like this:

```env
APP_NAME=
CLIENT_ID=
REDDIT_SECRET=
REDIRECT_URI=
USERNAME=
PASSWORD=
```

## To-Do

- [ ] Update PRAW authentication to use the code flow.
- [ ] Create a CLI front-end.
- [ ] Allow specific scrape jobs to be defined in a .json or .yml file and simply run through the front-end.
- [ ] Bullet-proof app-wide rate-limiting.
- [ ] Create a link with the Golem bot as a prototype for generic future access.
