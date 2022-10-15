import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="poketracker",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor,
)

# if connection.open:
#     print("the connection is opened")

# returns the heaviest pokemon
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


def findOwners(pokemon):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT pokemons_trainers.trainer FROM pokemons, pokemons_trainers WHERE pokemons.id = pokemons_trainers.id_pokemon AND pokemons.name = "{pokemon}"'
            cursor.execute(query)
            result = cursor.fetchall()
            trainersNames = [trainer["trainer"] for trainer in result]
            print(trainersNames)
    except:
        print("Error with getting all trainers of this pokemon")


def findRoster(trainer):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT pokemons.name FROM pokemons_trainers, pokemons WHERE pokemons.id = pokemons_trainers.id_pokemon AND pokemons_trainers.trainer = "{trainer}"'
            cursor.execute(query)
            result = cursor.fetchall()
            pokemonsNames = [pokemon["name"] for pokemon in result]
            print(pokemonsNames)

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


# get_heaviest_pokemon()
# findByType("grass")
# findOwners("gengar")
# findRoster("loga")

# find_max_owned_poke()
