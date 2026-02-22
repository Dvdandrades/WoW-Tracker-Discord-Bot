import pytest
import time
from unittest.mock import AsyncMock, patch
from src.api_client import BlizzardAPIClient


@pytest.mark.asyncio
async def test_get_access_token():
    client = BlizzardAPIClient(client_id="test_id", client_secret="test_secret")

    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"access_token": "test_token", "expires_in": 3600}
    mock_response.raise_for_status = lambda: None

    with patch("aiohttp.ClientSession.post") as mock_post:
        mock_post.return_value.__aenter__.return_value = mock_response

        token = await client.get_access_token()

        assert token == "test_token"
        assert client._access_token == "test_token"
        mock_post.assert_called_once()


@pytest.mark.asyncio
async def test_token_expiry():
    client = BlizzardAPIClient(client_id="test_id", client_secret="test_secret")
    client._access_token = "cached_token"
    client._token_expiry = time.time() + 10

    token = await client.get_access_token()
    assert token == "cached_token"


@pytest.mark.asyncio
async def test_get_character_summary():
    client = BlizzardAPIClient(client_id="test_id", client_secret="test_secret")

    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"name": "TestChar", "level": 80}
    mock_response.raise_for_status = lambda: None

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.return_value.__aenter__.return_value = mock_response

        character_info = await client.get_character_summary("test_realm", "test_char")

        assert character_info["name"] == "TestChar"
        assert character_info["level"] == 80
        mock_get.assert_called_once()
