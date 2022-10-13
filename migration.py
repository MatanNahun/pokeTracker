import json
import pymysql

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


def migration():
    for pokemon in data:
        sql_insert_to_pokemon_table = f'INSERT INTO pokemons VALUES({pokemon["id"]}, "{pokemon["name"]}", "{pokemon["type"]}", {pokemon["height"]}, {pokemon["weight"]} )'
        print(sql_insert_to_pokemon_table)

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_insert_to_pokemon_table)
                connection.commit()
        except:
            print("error")


migration()
# a comment i added
# matan comment i added
