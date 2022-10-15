from fastapi import FastAPI
import requests
import uvicorn

from main import find_owners, find_roster, get_poke_details, insert_new_trainer, insert_poke_types, pokemons_by_type, remove_pokemon_ownership

app = FastAPI()


@app.get("/pokemon/{name}")
async def get_pokemon(name):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
    pokemon_types_raw = response.json()["types"]
    pokemon_types = [pokemon["type"]["name"] for pokemon in pokemon_types_raw]

    insert_poke_types(name, pokemon_types)
    pokemon_details = get_poke_details(name)
    pokemon_details['types'] = pokemon_types

    return pokemon_details


@app.get("/pokemons-by-trainer/{trainer}")
def get_pokemons_by_trainer(trainer):
    pokemons = find_roster(trainer)
    
    return pokemons


@app.get("/trainers-by-pokemon/{pokemon}")
def get_trainers_by_pokemon(pokemon):
    trainers = find_owners(pokemon)
    
    return trainers


@app.post("/addTrainer/{name}/{town}")
def add_trainer(name, town):
    
    insert_new_trainer(name, town)


@app.get("/pokemons-by-type/{type}")
def get_pokemon_by_type(type):
    pokemons = pokemons_by_type(type)
    
    return pokemons


@app.delete("/deletePokemeon/{id_pokemon}/{trainer}")
def delete_pokemon(id_pokemon, trainer):
    
    remove_pokemon_ownership(id_pokemon, trainer)

if __name__ == "__main__":
    uvicorn.run('server:app', host="0.0.0.0", port=8000, reload=True)