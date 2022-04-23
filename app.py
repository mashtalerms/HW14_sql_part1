from flask import Flask, jsonify
from utils import get_connection_sql, get_last_film_by_title, get_films_by_years, get_films_by_rating, get_films_by_genre, get_films_by_two_actors, get_films_and_shows_by_parameters

app = Flask(__name__)


@app.route("/movie/<title>")
def film_by_title(title):
    film = get_last_film_by_title(title)
    return jsonify(film)


@app.route("/movie/<int:year1>/to/<int:year2>")
def film_by_years(year1, year2):
    films = get_films_by_years(year1, year2)
    return jsonify(films)


@app.route("/rating/<rating>")
def film_by_rating(rating):
    films = get_films_by_rating(rating)
    return jsonify(films)


@app.route("/genre/<genre>")
def film_by_genre(genre):
    film = get_films_by_genre(genre)
    return jsonify(film)


app.run()


