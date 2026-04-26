# Movie Database App

A command-line movie manager that uses the OMDb API to fetch movie data and stores everything in a local SQLite database.

## Features

- **List movies** — view all stored movies with their year and IMDb rating
- **Add movie** — look up any title via the OMDb API and save it automatically (title, year, rating, poster)
- **Delete movie** — remove a movie from the database
- **Update rating** — manually override a movie's rating (1-10)
- **Stats** — average rating, median rating, best and worst movie(s)
- **Random movie** — pick a random movie from your collection
- **Search** — find movies by partial title match
- **Sort** — order by rating (best to worst or worst to best) or year (newest to oldest or oldest to newest)
- **Rating histogram** — export a PNG chart of the rating distribution
- **Generate website** — produce a static _static/index.html movie grid with posters

## Requirements

- Python 3.8+
- An OMDb API key (https://www.omdbapi.com/apikey.aspx) — free tier available

## Setup

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd My_Movie_App
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the API key**

   Create a `.env` file in the project root:

   ```
   OMDB_API_KEY=your_api_key_here
   ```

## Usage

```bash
python movies.py
```

The menu will guide you through all available options:

```
========== MOVIE DB ==========
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update rating
5. Stats
6. Random movie
7. Search movie
8. Sort by your choice
9. Create Rating Histogram
10. Generate website
================================
Select>
```

## Project Structure

```
My_Movie_App/
├── movies.py               # Main application and menu logic
├── movie_storage_sql.py    # SQLAlchemy data layer (SQLite)
├── movies.db               # SQLite database (auto-created on first run)
├── requirements.txt
├── .env                    # API key (not committed)
└── _static/
    ├── index_template.html # HTML template for the generated site
    ├── style.css           # Stylesheet for the generated site
    └── index.html          # Generated output (option 10)
```

## Tech Stack

| Library | Purpose |
|---|---|
| SQLAlchemy | ORM / SQLite database access |
| requests | OMDb API calls |
| python-dotenv | .env file loading |
| matplotlib | Rating histogram export |
