import sqlite3
import json


def get_connection_sql(sqlite_query):
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        sqlite_query = sqlite_query
        result = cur.execute(sqlite_query)
        return result.fetchall()


def get_last_film_by_title(title):
    sqlite_query = f"""
            SELECT `title`, `country`, MAX(`release_year`), `listed_in`, `description`
            FROM netflix
            WHERE `title` LIKE '%{title}%'
            LIMIT 1
    """
    result = get_connection_sql(sqlite_query)
    film_dict = {}
    for film in result:
        film_dict['title'] = film[0]
        film_dict['country'] = film[1]
        film_dict['release_year'] = film[2]
        film_dict['listed_in'] = film[3]
        film_dict['description'] = film[4].strip('\n')
    return film_dict


def get_films_by_years(first, second):
    sqlite_query = f"""
                SELECT `title`, `release_year`
                FROM netflix
                WHERE `release_year` BETWEEN '{first}' AND '{second}'
                LIMIT 100
        """
    result = get_connection_sql(sqlite_query)
    return result


def get_films_by_rating(rating):

    rating_dict = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }

    sqlite_query = f"""
                SELECT `title`, `rating`, `description`
                FROM netflix
                WHERE `rating` IN {rating_dict[rating]}
                LIMIT 100
        """
    result = get_connection_sql(sqlite_query)
    return result


def get_films_by_genre(genre):

    sqlite_query = f"""
                SELECT `title`, `description`, `release_year`
                FROM netflix
                WHERE `listed_in` LIKE '%{genre}%'
                ORDER BY `release_year` DESC
                LIMIT 10
        """
    result = get_connection_sql(sqlite_query)
    return result


def get_films_by_two_actors(first_name, second_name):

    sqlite_query = f"""
                SELECT `cast`
                FROM netflix
                WHERE `cast` != ""
                AND `cast` LIKE "%{first_name}%"
                AND `cast` LIKE "%{second_name}%"
        """

    result = get_connection_sql(sqlite_query)

    str_of_actors = ""
    list_of_actors = []

    for actor in result:
        str_of_actors += actor[0] + ","
    list_of_all_actors = str_of_actors.split(',')

    for actor in list_of_all_actors:
        if actor != first_name and actor != " " + second_name:
            list_of_actors.append(actor)
    actors_dict = {}
    for actor in list_of_actors:
        if actor not in actors_dict.keys():
            actors_dict[actor] = 1
        else:
            actors_dict[actor] += 1

    needed_actors = []
    for actor in actors_dict.items():
        if actor[1] >= 2:
            needed_actors.append(actor[0])

    return needed_actors


def get_films_and_shows_by_parameters(type, year, genre):
    sqlite_query = f"""
                    SELECT `title`, `description`
                    FROM netflix
                    WHERE `type` = "{type}"
                    AND `release_year` = {year}
                    AND `listed_in` LIKE "%{genre}%"
            """

    result = get_connection_sql(sqlite_query)
    with open('films_by_parameters.json', 'w', encoding='UTF-8') as fp:
        json.dump(result, fp)
    return "Все в этом файле - films_by_parameters.json"

