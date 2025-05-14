import os

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv


# Initialize Bot instance with a default parse mode which will be passed to all API calls
load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher(storage=MemoryStorage())