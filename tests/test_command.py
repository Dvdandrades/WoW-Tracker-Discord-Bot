import pytest
from unittest.mock import AsyncMock

from src.commands import get_token_price, get_character_info


@pytest.mark.asyncio
async def test_get_token_price():
    mock_client = AsyncMock()
    mock_client.request.return_value = {"price": 1000000}

    price = await get_token_price(mock_client)
    assert price == 100.0


@pytest.mark.asyncio
async def test_get_character_info():
    mock_client = AsyncMock()

    summary_data = {
        "name": "TestCharacter",
        "level": 80,
        "race": {"name": "Human"},
        "character_class": {"name": "Warrior"},
        "active_spec": {"name": "Arms"},
        "equipped_item_level": 130,
        "faction": {"name": "Alliance"}
    }
    
    media_data = {
        "assets": [{"key": "avatar", "value": "http://example.com/image.png"}]
    }
    
    stats_data = {
        "health": 10000,
        "stamina": 500,
        "melee_crit": {"value": 5.2},
        "melee_haste": {"value": 4.8},
        "mastery": {"value": 6.1},
        "versatility": 3.9
    }

    mock_client.request.side_effect = [summary_data, media_data, stats_data]

    character_data = "TestCharacter-TestRealm"
    info = await get_character_info(mock_client, character_data)

    assert info["name"] == "TestCharacter"
    assert info["level"] == 80
    assert info["stats"]["crit"] == "5.20%"