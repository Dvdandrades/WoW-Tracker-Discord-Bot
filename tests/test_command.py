import pytest
from unittest.mock import AsyncMock, patch

from src.commands import get_token_price, get_character_info


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


@pytest.mark.asyncio
async def test_get_character_info():
    mock_client = AsyncMock()
    mock_client.get_character_summary.return_value = {
        "name": "TestCharacter",
        "level": 80,
        "race": {"name": "Human"},
        "character_class": {"name": "Warrior"},
        "active_spec": {"name": "Arms"},
        "equipped_item_level": 130,
        "faction": {"name": "Alliance"},
    }

    character_data = "TestCharacter-TestRealm"
    info = await get_character_info(mock_client, character_data)

    assert info["name"] == "TestCharacter"
    assert info["level"] == 80
    assert info["class"] == "Warrior"
