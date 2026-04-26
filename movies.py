import os
import random

import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv

import movie_storage_sql as storage

load_dotenv()
api_key = os.getenv("OMDB_API_KEY")


def total_movies(movies):
    """
    Return the total movies in the 'movies' dict

    :param movies: dict of movies from the database
    :return: total_movie_count
    """
    total_movie_count = len(movies)
    return f"{total_movie_count} movies in total"


def list_all_movies_and_total_movies():
    """
    Prints all movies and all their info

    :return: None
    """
    movies = storage.list_movies()
    print(total_movies(movies))
    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']:.2f}")


def add_movie():
    """
    Option to add a movie to the database.
    Asks for user input, validates title (non-empty, not duplicate),
    year (valid integer in range), and rating (float between 1-10).

    :return: None
    """
    movies = storage.list_movies()

    # --- TITLE ---
    while True:
        # remove leading and trailing spaces
        title = input("Name of the movie: ").strip()

        if title == "":
            print("Title cannot be empty!")
            return

        # CHECK if movie already exists
        if title in movies:
            print("This movie already exists!")
            return

        break  # title is valid

    # --- FETCH FROM API ---
    api_url = f"https://www.omdbapi.com/?apikey={api_key}&t={title}"
    try:
        # timeout=5 avoids hanging forever if the API is unreachable
        response = requests.get(api_url, timeout=5)
        data = response.json()
    except requests.exceptions.ConnectionError:
        print("No internet connection. Please check your network.")
        return
    except requests.exceptions.Timeout:
        print("The request timed out. The API might be down.")
        return
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred: {e}")
        return

    # API returns "Response": "False" when the movie title is not found
    if data.get("Response") == "False":
        print(f"Movie '{title}' not found. Please check the title.")
        return

    movie_title = data["Title"]
    year = int(data["Year"])

    raw_rating = data.get("imdbRating", "N/A")
    if raw_rating == "N/A":
        print(f"'{movie_title}' has no IMDb rating yet.")
        return

    rating = float(raw_rating)

    # Fetch the poster URL returned by the API (can be "N/A" if unavailable)
    poster_image = data.get("Poster")

    # Pass poster_image to storage so it is saved in the database
    storage.add_movie(movie_title, year, rating, poster_image)
    print(f"Movie '{movie_title}' ({year}) added with IMDb rating {rating:.1f}!")


def delete_movie():
    """
    Delete a movie from the database, if it exists.

    :return: None
    """
    movies = storage.list_movies()

    title = input("Which movie do you want to delete: ").strip()

    if title not in movies:
        print(f"Movie '{title}' does not exist!")
        return

    storage.delete_movie(title)


def update_movie_rating():
    """
    Update the rating of a movie, if it exists in the database.

    :return: None
    """
    movies = storage.list_movies()

    title = input("Which movie do you want to rerate: ").strip()

    if title not in movies:
        print(f"'{title}' does not exist in the list.")
        return

    while True:
        try:
            new_rating = float(input("What is the new rating? "))
            if not (1 <= new_rating <= 10):
                print("Rating must be between 1 and 10")
                continue
        except ValueError:
            print("Invalid rating!")
            continue

        storage.update_movie(title, new_rating)
        return


def print_random_movie():
    """
    Print 1 random movie and its rating.

    :return: None
    """
    movies = storage.list_movies()
    title, data = random.choice(list(movies.items()))
    print(f"---- Random movie ----\n"
          f"Title: {title}\n"
          f"Rating: {data['rating']:.2f}\n"
          f"Year of Release: {data['year']}")


def search_for_movies():
    """
    Search the database for movies, prints every movie
    and its info if the search term is found in the movie title.

    :return: None
    """
    movies = storage.list_movies()
    user_search_input = input("Search term: ")
    found = False
    for title, data in movies.items():
        if user_search_input.lower() in title.lower():
            print(f"{title} ({data['year']}): {data['rating']:.2f}")
            found = True
    if not found:
        print("No movies found!")


def get_priority():
    """
    Ask user how to sort movies, then call movies_sorted_by
    with the chosen key and order.

    :return: None
    """
    while True:
        print("Sort by: ")
        print("1. Rating ---> Best to Worst")
        print("2. Rating ---> Worst to Best")
        print("3. Year ---> Newest to Oldest")
        print("4. Year ---> Oldest to Newest")

        priority = input("What do you want to sort by? ")

        if priority == "1":
            print()
            movies_sorted_by("rating", True, "best to worst")
            return
        elif priority == "2":
            print()
            movies_sorted_by("rating", False, "worst to best")
            return
        elif priority == "3":
            print()
            movies_sorted_by("year", True, "newest to oldest")
            return
        elif priority == "4":
            print()
            movies_sorted_by("year", False, "oldest to newest")
            return
        else:
            print()
            print("Invalid choice, try again!")


def movies_sorted_by(key, reverse, description):
    """
    Prints movies from the database sorted by the given key and order.

    :param key: 'rating' or 'year'
    :param reverse: True for descending, False for ascending
    :param description: human-readable description of the sort order
    :return: None
    """
    movies = storage.list_movies()
    sorted_movies = sorted(
        movies.items(), key=lambda x: x[1][key], reverse=reverse
    )

    print(f"Movies from {description}:")
    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']:.2f}")


def generate_website():
    """
    Reads the HTML template, replaces __TEMPLATE_MOVIE_GRID__ with a
    generated <li> block for each movie (poster, title, year), and
    writes the result to _static/index.html.

    :return: None
    """
    movies = storage.list_movies()

    # Build one <li> entry per movie using the CSS classes from style.css
    movie_items = []
    for title, data in movies.items():
        poster = data.get("poster") or ""

        # Use empty src if poster is missing or "N/A"
        if poster == "N/A":
            poster = ""

        movie_items.append(
            f'<li>\n'
            f'    <div class="movie">\n'
            f'        <img class="movie-poster" src="{poster}" '
            f'alt="{title} poster">\n'
            f'        <div class="movie-title">{title}</div>\n'
            f'        <div class="movie-year">{data["year"]}</div>\n'
            f'    </div>\n'
            f'</li>'
        )

    # Join all movie entries into one string for the grid placeholder
    movie_grid_html = "\n        ".join(movie_items)

    # Read the template file
    with open("_static/index_template.html", "r") as template_file:
        template = template_file.read()

    # Replace both placeholders with the generated content
    output = template.replace("__TEMPLATE_TITLE__", "My Movie App")
    output = output.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    # Write the final HTML to _static/index.html
    with open("_static/index.html", "w") as output_file:
        output_file.write(output)

    print("Website generated: _static/index.html")


def create_rating_histogram():
    """
    Ask user for a file name and save a histogram of the ratings.

    :return: None
    """
    movies = storage.list_movies()
    ratings = [data["rating"] for _, data in movies.items()]

    file_name = input("Save histogram as (e.g. ratings.png): ").strip()

    plt.figure()
    plt.hist(ratings, bins=50, edgecolor='black')
    plt.title("Movie-Rating Histogram")
    plt.xlabel("Rating")
    plt.ylabel("Number of Movies")
    plt.savefig(file_name)
    plt.close()


def print_stats():
    """
    Prints average rating, median rating,
    best movie(s) with rating and worst movie(s) with rating.

    :return: None
    """
    movies = storage.list_movies()
    ratings = sorted(data["rating"] for _, data in movies.items())

    average = sum(ratings) / len(ratings)
    print(f"Average rating: {average:.2f}")

    mid = len(ratings) / 2
    if mid % 2 != 0:
        median = ratings[int(mid - 0.5)]
    else:
        median = (ratings[int(mid)] + ratings[int(mid) + 1]) / 2
    print(f"Median rating: {median:.2f}")

    best_rating = max(ratings)
    best = [t for t, d in movies.items() if d["rating"] == best_rating]
    print(f"Best movie(s) ({best_rating:.2f}): {', '.join(best)}")

    worst_rating = min(ratings)
    worst = [t for t, d in movies.items() if d["rating"] == worst_rating]
    print(f"Worst movie(s) ({worst_rating:.2f}): {', '.join(worst)}")


def main():
    """
    Main loop — displays the menu and routes user input
    to the appropriate function.

    :return: None
    """
    while True:
        print("\n========== MOVIE DB ==========")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update rating")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Sort by your choice")
        print("9. Create Rating Histogram")
        print("10. Generate website")
        print("================================")
        choice = input("Select> ").strip()

        if choice == "0":
            print("Good-bye!")
            break
        elif choice == "1":
            list_all_movies_and_total_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            update_movie_rating()
        elif choice == "5":
            print_stats()
        elif choice == "6":
            print_random_movie()
        elif choice == "7":
            search_for_movies()
        elif choice == "8":
            get_priority()
        elif choice == "9":
            create_rating_histogram()
        elif choice == "10":
            generate_website()
        else:
            print("Invalid choice, try again.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
