import pytest
import time
from unittest.mock import AsyncMock, MagicMock
from src.api_client import BlizzardAPIClient


@pytest.mark.asyncio
async def test_get_access_token():
    client = BlizzardAPIClient(client_id="test_id", client_secret="test_secret")

    client._session = AsyncMock()

    client._session.post = MagicMock()

    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"access_token": "test_token", "expires_in": 3600}
    mock_response.raise_for_status = lambda: None

    client._session.post.return_value.__aenter__.return_value = mock_response

    token = await client.get_access_token()
    assert token == "test_token"
    assert client._access_token == "test_token"
    client._session.post.assert_called_once()


@pytest.mark.asyncio
async def test_token_expiry():
    client = BlizzardAPIClient(client_id="test_id", client_secret="test_secret")
    client._access_token = "cached_token"
    client._token_expiry = time.time() + 10

    token = await client.get_access_token()
    assert token == "cached_token"
