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

def insert_poke_types(poke_name, poke_types):
    
    for type in poke_types:
        try:
            with connection.cursor() as cursor:
                query = f'INSERT IGNORE INTO pokemon_types VALUES(\'{poke_name}\', \'{type}\');'
                cursor.execute(query)
                connection.commit()
        except:
            print(f'Failed to insert types for {poke_name}')

def get_poke_details(name):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT id, name, height, weight FROM pokemons WHERE name = \'{name}\''
            cursor.execute(query)
            result = cursor.fetchall()
            print(result)
            return result[0]
    except:
        print(f'Failed to get the details of {name}')

get_poke_details('bulbasaur')
    
    
    

# get_heaviest_pokemon()
# findByType("grass")
# findOwners("gengar")
# findRoster("loga")

# find_max_owned_poke()

