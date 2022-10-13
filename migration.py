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
        sql_insert_to_pokemon_table = f'INSERT INTO pokemons VALUES({pokemon["id"]}, "{pokemon["name"]}", "{pokemon["type"]}", {pokemon["height"]}, {pokemon["weight"]} );'
        print(sql_insert_to_pokemon_table)

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_insert_to_pokemon_table)
                connection.commit()
        except:
            print("Failed to update pokemons")

        fill_trainers(pokemon["id"], pokemon["ownedBy"])



#migration()

