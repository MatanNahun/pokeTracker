import re
from tempfile import _TemporaryFileWrapper
import pymysql
from fastapi import FastAPI, HTTPException, Response, status

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="poketracker",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor,
)


def get_heaviest_pokemon():
    try:
        with connection.cursor() as cursor:
            query = f"SELECT name, (weight) FROM pokemons WHERE weight = All (SELECT MAX(weight) FROM pokemons)"
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
    except:
        print("Error with getting heaviest pokeon")


def findByType(type):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT name FROM pokemons WHERE type = "{type}"'
            cursor.execute(query)
            result = cursor.fetchall()
            pokemonsNames = [pokemon["name"] for pokemon in result]
            print(pokemonsNames)
    except:
        print("Error with getting all pokeon with specific type")


def find_owners(pokemon, response: Response):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT pokemons_trainers.trainer FROM pokemons, pokemons_trainers WHERE pokemons.id = pokemons_trainers.id_pokemon AND pokemons.name = "{pokemon}"'
            cursor.execute(query)
            result = cursor.fetchall()
            trainersNames = [trainer["trainer"] for trainer in result]
            if len(trainersNames) == 0:
                # return "no owners found..."
                response.status_code = status.HTTP_400_BAD_REQUEST
                raise HTTPException(status_code=400, detail="No trainers found...")

            else:
                return trainersNames
    except Exception as e:
        return e


def find_roster(trainer):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT pokemons.name FROM pokemons_trainers, pokemons WHERE pokemons.id = pokemons_trainers.id_pokemon AND pokemons_trainers.trainer = "{trainer}"'
            cursor.execute(query)
            result = cursor.fetchall()
            pokemonsNames = [pokemon["name"] for pokemon in result]
            return pokemonsNames

    except:
        print("Error with getting all pokemons of this trainer")


max_owned_str = """
SELECT  max_trainers.name
FROM (
    SELECT count(*) AS num, pokemons.name
    FROM pokemons, pokemons_trainers
    WHERE pokemons.id = pokemons_trainers.id_pokemon 
    GROUP BY pokemons_trainers.id_pokemon
) max_trainers
WHERE max_trainers.num = (SELECT MAX(c.trainer_count) FROM (SELECT COUNT(*) AS trainer_count FROM pokemons_trainers GROUP BY id_pokemon) c)
"""


def find_max_owned_poke():
    try:
        with connection.cursor() as cursor:
            query = max_owned_str
            cursor.execute(query)
            result = cursor.fetchall()
            pokemonsNames = [pokemon["name"] for pokemon in result]
            print(pokemonsNames)

    except:
        print("Error with getting the max owned pokemon")


def insert_poke_types(poke_name, poke_types):

    for type in poke_types:
        try:
            with connection.cursor() as cursor:
                query = (
                    f"INSERT IGNORE INTO pokemon_types VALUES('{poke_name}', '{type}');"
                )
                cursor.execute(query)
                connection.commit()
        except:
            print(f"Failed to insert types for {poke_name}")


def get_poke_details(name):
    try:
        with connection.cursor() as cursor:
            query = (
                f"SELECT id, name, height, weight FROM pokemons WHERE name = '{name}';"
            )

            cursor.execute(query)
            result = cursor.fetchall()
            if cursor.rowcount != 0:
                return result[0]

    except:
        return f"Failed to get the details of {name}"


def insert_new_trainer(name, town):

    try:
        with connection.cursor() as cursor:
            query = f"INSERT IGNORE INTO trainers VALUES('{name}', '{town}');"
            cursor.execute(query)
            connection.commit()
            return f"Added {name} successfuly"
    except:
        return f"Failed to insert the trainer {name}"


def pokemons_by_type(type):

    try:
        with connection.cursor() as cursor:
            query = f"SELECT name FROM pokemon_types WHERE poke_type = '{type}';"
            cursor.execute(query)
            results = cursor.fetchall()
            return [result["name"] for result in results]
    except:
        print(f"Failed to get pokemons by type {type}")


def remove_pokemon_ownership(id_pokemon, trainer):

    try:
        with connection.cursor() as cursor:
            query = f"DELETE FROM pokemons_trainers WHERE id_pokemon = '{id_pokemon}' AND trainer = '{trainer}';"
            cursor.execute(query)
            connection.commit()
            if cursor.rowcount == 0:
                return f"the trainer: {trainer} or the id: {id_pokemon} does not exist"
            else:
                return f"the pokemon with id: {id_pokemon} of the trainer {trainer} remmoved succesfully"

    except:
        return f"failed to remove {trainer}'s ownership of {id_pokemon}"


def get_pokemon_id(pokemon_name):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT id FROM pokemons WHERE pokemons.name = "{pokemon_name}";'
            row_count = cursor.execute(query)
            result = cursor.fetchall()
            if row_count > 0:
                # print(result[0]["id"])
                return result[0]["id"]
            else:
                raise HTTPException(
                    status_code=404, detail="No such pokemon name in the database"
                )
    except TypeError as e:
        return e


def evolve(id_pokemon, pokemon_evolved_id, trainer):

    try:
        with connection.cursor() as cursor:
            query_exist = f"SELECT COUNT(*) as count FROM pokemons_trainers WHERE id_pokemon = {id_pokemon} AND trainer = '{trainer}';"
            cursor.execute(query_exist)
            result = cursor.fetchall()
            # print(result[0]["count"])

            if result[0]["count"] != 0:
                query = f"UPDATE pokemons_trainers SET id_pokemon = {pokemon_evolved_id} WHERE id_pokemon = {id_pokemon} AND trainer = '{trainer}';"
                cursor.execute(query)
                connection.commit()
            else:
                raise Exception(print(f"{trainer} does not have the desired pokemon"))
    except:
        return f"failed to evolve"


# get_heaviest_pokemon()
# findByType("grass")
# findOwners("gengar")
# findRoster("loga")

# find_max_owned_poke()

# get_pokemon_id("ditto")
evolve(5, 6, "Archie")
