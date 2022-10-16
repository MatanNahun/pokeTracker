import json
import pymysql
import requests

from main import insert_poke_types

with open("pokemonDBJson.json") as file:
    data = json.load(file)


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="poketracker",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor,
)


def fill_trainers(pokemon_id, owned_by):

    for trainer in owned_by:

        try:
            with connection.cursor() as cursor:
                query = f'INSERT IGNORE INTO trainers VALUES("{trainer["name"]}", "{trainer["town"]}");'
                cursor.execute(query)
                connection.commit()
        except:
            print("Failed to update trainers")

        try:
            with connection.cursor() as cursor:
                query = f'INSERT INTO pokemons_trainers VALUES({pokemon_id}, "{trainer["name"]}");'
                cursor.execute(query)
                connection.commit()
        except:
            print("Failed to update pokemons_trainers")


def migration():
    for pokemon in data:
        sql_insert_to_pokemon_table = f'INSERT INTO pokemons VALUES({pokemon["id"]}, "{pokemon["name"]}", {pokemon["height"]}, {pokemon["weight"]} );'
        print(sql_insert_to_pokemon_table)

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_insert_to_pokemon_table)
                connection.commit()
        except:
            print("Failed to update pokemons")

        fill_trainers(pokemon["id"], pokemon["ownedBy"])


def update_types():
    pokemons_query = "SELECT name FROM pokemons;"

    try:
        with connection.cursor() as cursor:
            cursor.execute(pokemons_query)
            names = cursor.fetchall()

            for item in names:
                name = item["name"]
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
                pokemon_types_raw = response.json()["types"]
                pokemon_types = [
                    pokemon["type"]["name"] for pokemon in pokemon_types_raw
                ]
                insert_poke_types(name, pokemon_types)
    except:
        print("Failed to query pokemon names")


# migration()
update_types()
