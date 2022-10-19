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
