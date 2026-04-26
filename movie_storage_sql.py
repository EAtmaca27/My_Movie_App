from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist.
# 'poster' column stores the OMDB poster URL for each movie.
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT
        )
    """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        # Added 'poster' to the SELECT so it is included in the returned dict
        result = connection.execute(
            text("SELECT title, year, rating, poster FROM movies")
        )
        movies = result.fetchall()

    # row[0]=title, row[1]=year, row[2]=rating, row[3]=poster
    return {
        row[0]: {"year": row[1], "rating": row[2], "poster": row[3]}
        for row in movies
    }


def add_movie(title, year, rating, poster=None):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            # 'poster' is optional — defaults to None if not provided
            connection.execute(
                text(
                    "INSERT INTO movies (title, year, rating, poster) "
                    "VALUES (:title, :year, :rating, :poster)"
                ),
                {"title": title, "year": year, "rating": rating, "poster": poster},
            )
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("DELETE FROM movies WHERE title = :title"),
                {"title": title},
            )
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("UPDATE movies SET rating = :rating WHERE title = :title"),
                {"title": title, "rating": rating},
            )
            connection.commit()
            print(f"Rating for movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
