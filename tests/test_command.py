import pytest
from unittest.mock import AsyncMock, patch

from src.commands import get_token_price

@pytest.mark.asyncio
async def test_get_token_price():
    mock_client = AsyncMock()
    mock_client.get_access_token.return_value = "test_token"

    mock_response = AsyncMock()
    mock_response.json.return_value = {"price": 1000000}
    mock_response.raise_for_status = lambda: None

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.return_value.__aenter__.return_value = mock_response

        price = await get_token_price(mock_client)

        assert price == 100.0