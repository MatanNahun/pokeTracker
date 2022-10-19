from tkinter.messagebox import NO
from fastapi import FastAPI
import requests
import uvicorn

from main import (
    evolve,
    find_owners,
    find_roster,
    get_poke_details,
    get_pokemon_id,
    insert_new_trainer,
    insert_poke_types,
    pokemons_by_type,
    remove_pokemon_ownership,
)

app = FastAPI()

# get trainers by pokemons in query
@app.get("/trainers")
def get_trainers_by_pokemon(pokemon):
    trainers = find_owners(pokemon)

    return trainers


# add trainer by trainer name and town name in query
@app.post("/trainers")
def add_trainer(name, town):

    return insert_new_trainer(name, town)


# get pokemons by trainers or type in query
@app.get("/pokemons")
def get_pokemon_by_type(trainer=None, type=None, name=None):
    if trainer is not None:
        return find_roster(trainer)

    elif type is not None:
        return pokemons_by_type(type)

    elif name is not None:
        try:
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
            response.raise_for_status()
        except:
            return f"{name} does not exist"
        pokemon_types_raw = response.json()["types"]
        pokemon_types = [pokemon["type"]["name"] for pokemon in pokemon_types_raw]

        insert_poke_types(name, pokemon_types)
        pokemon_details = get_poke_details(name)
        pokemon_details["types"] = pokemon_types

        return pokemon_details

    else:
        return "requires exactly one parameter"


@app.delete("/pokemons")
def delete_pokemon(id_pokemon, trainer):

    return remove_pokemon_ownership(id_pokemon, trainer)


@app.put("/pokemons/evolve")
def evolve_pokemon(id_pokemon, trainer):

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{id_pokemon}")
    pokemon_name_to_evolve = response.json()["name"]
    evolution_chain_url = response.json()["evolution_chain"]["url"]
    response = requests.get(evolution_chain_url)

    evolution_chain = response.json()["chain"]

    while True:
        try:
            if pokemon_name_to_evolve == evolution_chain["species"]["name"]:
                if evolution_chain["evolves_to"] != []:
                    evolved_pokemon_name = evolution_chain["evolves_to"][0]["species"][
                        "name"
                    ]
                    evolved_pokemon_id = get_pokemon_id(evolved_pokemon_name)
                    if evolved_pokemon_id != -1:
                        evolve(id_pokemon, evolved_pokemon_id, trainer)
                        return f"{pokemon_name_to_evolve} evolved to {evolved_pokemon_name}"
                    else:
                        return f"{evolved_pokemon_name} is unkown"
                else:
                    return f"cannot evolve {pokemon_name_to_evolve} further"
        except:
            return "failed to evolve in server"

        evolution_chain = evolution_chain["evolves_to"][0]


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
