from tempfile import _TemporaryFileWrapper
import pymysql

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


def find_owners(pokemon):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT pokemons_trainers.trainer FROM pokemons, pokemons_trainers WHERE pokemons.id = pokemons_trainers.id_pokemon AND pokemons.name = "{pokemon}"'
            cursor.execute(query)
            result = cursor.fetchall()
            trainersNames = [trainer["trainer"] for trainer in result]
            return trainersNames
    except:
        print("Error with getting all trainers of this pokemon")


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
            print(result)
            return result[0]
    except:
        print(f"Failed to get the details of {name}")


def insert_new_trainer(name, town):

    try:
        with connection.cursor() as cursor:
            query = f"INSERT IGNORE INTO trainers VALUES('{name}', '{town}');"
            cursor.execute(query)
            connection.commit()
    except:
        print(f"Failed to insert the trainer {name}")


def pokemons_by_type(type):

    try:
        with connection.cursor() as cursor:
            query = f"SELECT name FROM pokemon_types WHERE poke_type = '{type}';"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except:
        print(f"Failed to get pokemons by type {type}")


def remove_pokemon_ownership(id_pokemon, trainer):

    try:
        with connection.cursor() as cursor:
            query = f"DELETE FROM pokemons_trainers WHERE id_pokemon = '{id_pokemon}' AND trainer = '{trainer}';"
            cursor.execute(query)
            connection.commit()
    except:
        print(f"failed to remove {trainer}'s ownership of {id_pokemon}")


def get_pokemon_id(pokemon_name):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT id FROM pokemons WHERE pokemons.name = "{pokemon_name}";'
            cursor.execute(query)
            result = cursor.fetchall()
            print(result[0]["id"])
            return result[0]["id"]
    except:
        print(f"Failed to get {pokemon_name} id")


def evolve(id_pokemon, pokemon_evolved_id, trainer):

    try:
        with connection.cursor() as cursor:
            query = f"UPDATE pokemons_trainers SET id_pokemon = {pokemon_evolved_id} WHERE id_pokemon = {id_pokemon} AND trainer = '{trainer}';"
            cursor.execute(query)
            connection.commit()
    except:
        print(f"failed to remove")


# get_heaviest_pokemon()
# findByType("grass")
# findOwners("gengar")
# findRoster("loga")

# find_max_owned_poke()

# get_pokemon_id("ditto")
