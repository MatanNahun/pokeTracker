from http import client, server
from urllib import response
import pytest
from unittest.mock import patch as mock_patch
from fastapi.testclient import TestClient

from server import app

client = TestClient(app)


def test_get_trainers_correct_poke_name():
    response = client.get("/trainers?pokemon=bulbasaur")
    assert response.status_code == 200


def test_get_trainers_incorrect_poke_name():
    response = client.get("/trainers?pokemon=ditoooor")
    assert response.status_code == 400



def test_get_pokemons_by_type():
    response = client.get("http://127.0.0.1:8000/pokemons?type=normal")
    assert "eevee" in response.json()
    assert "charizard" not in response.json()
    assert response.status_code == 201

def test_get_venusaur():
    response = client.get("/pokemons?name=venusaur")
    result = response.json()
    assert response.status_code == 201
    assert result == {
    "id": 3,
    "name": "venusaur",
    "height": 20,
    "weight": 1000,
    "types": [
        "grass",
        "poison"
    ]
}

def test_get_pokemon_by_type_poison():
    response = client.get("/pokemons?type=poison")
    result = response.json()
    assert response.status_code == 201
    assert 'venusaur' in result


def test_get_pokemon_by_type_grass():
    response = client.get("/pokemons?type=grass")
    result = response.json()
    assert response.status_code == 201
    assert 'venusaur' in result


def test_get_pokemons_of_drasna():
    response = client.get("/pokemons?trainer=drasna")
    result = response.json()
    assert response.status_code == 201
    assert result == ["wartortle", "caterpie", "beedrill", "arbok",
        "clefairy", "wigglytuff", "persian", 
        "growlithe", "machamp", "golem", "dodrio", 
        "hypno", "cubone", "eevee", "kabutops"] 


def test_get_trainers_of_charmander():
    response = client.get("/trainers?pokemon=charmander")
    result = response.json()
    assert response.status_code == 200
    assert result == [
        "Giovanni",
        "Jasmine",
        "Whitney"] 

