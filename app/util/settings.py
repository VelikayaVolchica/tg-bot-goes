import os
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN', default='')
USER_DB = os.getenv('USER_DB', default='')
PASSWORD_DB = os.getenv('PASSWORD_DB', default='')
HOST_DB = os.getenv('HOST_DB', default='')

categories = ['Покушац', 'Парк', 'Мероприятие', 'Музей', 'Магазин', 'С друзьями']

bot = Bot(token = API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)