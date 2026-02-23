import pytest
import discord
from unittest.mock import AsyncMock, patch, MagicMock

from main import token, pj
from src.commands import CharacterInfo


@pytest.mark.asyncio
async def test_token_command_embed():
    ctx = AsyncMock()

    with patch("main.get_token_price", new_callable=AsyncMock) as mock_get_price:
        mock_get_price.return_value = 200000

        await token.callback(ctx)

        ctx.send.assert_called_once()
        args, kwargs = ctx.send.call_args
        assert isinstance(kwargs["embed"], discord.Embed)
        assert "200,000 gold" in kwargs["embed"].description


@pytest.mark.asyncio
async def test_character_info_command_embed():
    ctx = AsyncMock()

    ctx.typing = MagicMock()
    typing_mock = MagicMock()
    typing_mock.__aenter__ = AsyncMock()
    typing_mock.__aexit__ = AsyncMock()

    ctx.typing.return_value = typing_mock

    character_data = "name-realm"

    with patch("main.get_character_info", new_callable=AsyncMock) as mock_get_info:
        mock_get_info.return_value = CharacterInfo(
            name="testCharacter",
            level=60,
            race="Human",
            character_class="Warrior",
            spec="Arms",
            ilvl=130,
            faction="Alliance",
        )

        await pj.callback(ctx, character_data=character_data)

        ctx.send.assert_called_once()
        args, kwargs = ctx.send.call_args
        assert isinstance(kwargs["embed"], discord.Embed)
        assert kwargs["embed"].title == "testCharacter"
        assert kwargs["embed"].color == discord.Color.blue()
