import os
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN', default='')
categories = ['Покушац', 'Парк', 'Мероприятие', 'Музей', 'Магазин', 'С друзьями']

bot = Bot(token = API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)