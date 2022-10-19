from http import client, server
import pytest
from unittest.mock import patch as mock_patch
from fastapi.testclient import TestClient

from server import app

client = TestClient(app)
