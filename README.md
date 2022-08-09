# RedditScrape
Low-Orbital-Tractor-Beam

## Aims

1. Create a bullet-proof Reddit connection and authentication module
2. Have a central codebase for creating ad-hoc and repeat scrapers
3. Create a module that my other apps, espcially my bots, can use to connect to Reddit

## Structure

```
..
├── RedditScrape
│   ├── .gitignore
│   ├── LICENSE
│   ├── README.md
│   ├── __init__.py
│   ├── main.py
│   └── src
│       ├── __init__.py
│       ├── auth.py
│       ├── data
│       │   ├── .env
│       │   └── settings.json
│       └── routing.py
├── data
```
