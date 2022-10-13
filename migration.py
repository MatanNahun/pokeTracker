import json


with open("pokemonDBJson.json") as file:
    data = json.load(file)


def migration():

    return


def fill_trainers(pokemon_id, owned_by):
    
    for trainer in owned_by:
      
        try:
            with connection.cursor() as cursor:
               query = f'INSERT IGNORE INTO trainers VALUES({trainer["name"]}, {trainer["town"]})'
               cursor.execute(query)
               connection.commit()
        except:
           print("Failed to update trainers")

        try:
            with connection.cursor() as cursor:
                query = f'INSERT INTO trainers VALUES({pokemon_id}, {trainer["name"]}'
        except:
            print("Failed")
            
            