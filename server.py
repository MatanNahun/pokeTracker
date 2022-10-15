from fastapi import FastAPI, Request
import requests
import uvicorn

from main import get_poke_details, insert_poke_types

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

if __name__ == "__main__":
    uvicorn.run('server: app', host="0.0.0.0", port=8000, reload=True)