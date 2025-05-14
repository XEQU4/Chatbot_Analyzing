import pytest
from aiogram import Bot


@pytest.mark.asyncio
async def test_bot_token_loading():
    from app.config import config

    assert config.TOKEN, "BOT_TOKEN should not be empty"
    bot = Bot(token=config.TOKEN)
    assert bot.token == config.TOKEN
