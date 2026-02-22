import pytest
import discord
from unittest.mock import AsyncMock, patch

from main import token


@pytest.mark.asyncio
async def test_token_command_embed():
    ctx = AsyncMock()

    with patch("main.get_token_price", new_callable=AsyncMock) as mock_get_price:
        mock_get_price.return_value = 200000

        await token(ctx)

        ctx.send.assert_called_once()
        args, kwargs = ctx.send.call_args
        assert isinstance(kwargs["embed"], discord.Embed)
        assert "200,000 gold" in kwargs["embed"].description
