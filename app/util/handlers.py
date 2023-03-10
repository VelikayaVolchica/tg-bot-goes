from aiogram import types
from loguru import logger
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from .settings import bot, dp, categories 

class Place(StatesGroup):
    name = State()
    address = State()
    category = State()
    date = State()
    price = State()

@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state:FSMContext):
    logger.info(f'Start user {message.from_user.id}')
    await state.finish()
    await message.answer('Привет, я бот, который помогает сохранять интересные места 😘')

@dp.message_handler(commands=['add'])
async def add_process(message: types.Message):
    logger.info(f'Add process start user {message.from_user.id}')
    await Place.name.set()
    await message.reply('Введи название места 😘')

@dp.message_handler(state=Place.name)
async def name_process(message: types.Message, state: FSMContext):
    logger.info(f'Add name {message.text} | user {message.from_user.id}')
    
    async with state.proxy() as data:
        data['name'] = message.text

    await Place.next()
    await message.reply('Введи адрес места 😘')

@dp.message_handler(state=Place.address)
async def adress_process(message: types.Message, state: FSMContext):
    logger.info(f'Add address {message.text} | user {message.from_user.id}')
    
    async with state.proxy() as data:
        data['address'] = message.text

    await Place.next()
    await message.reply('Введи категорию из данного списка:\n{}\n😘'.format(', '.join(categories)))

@dp.message_handler(lambda message: message.text not in categories, state=Place.category)
async def category_process_invalid(message: types.Message):
    logger.error(f'Wrong category | {message.text} | user {message.from_user.id}')
    return await message.reply('Давай по новой 😘\nВыбери категорию из данного списка:\n{}'.format(', '.join(categories)))

@dp.message_handler(lambda message: message.text == 'Мероприятие', state=Place.category)
async def category_process_event(message: types.Message, state:FSMContext):
    logger.info(f'Add category {message.text} | user {message.from_user.id}')

    async with state.proxy() as data:
        data['category'] = message.text

    await Place.next()
    return await message.reply('Введи дату мероприятия 😘')

@dp.message_handler(lambda message: message.text != 'Мероприятие', state=Place.category)
async def category_process_other(message: types.Message, state:FSMContext):
    logger.info(f'Add category {message.text} | user {message.from_user.id}')

    async with state.proxy() as data:
        data['category'] = message.text
    
    for i in range(2):
        await Place.next()
    return await message.reply('Введи цену или средний чек. Если посещение свободное, введи 0 😘')

@dp.message_handler(state=Place.date)
async def date_process(message: types.Message, state: FSMContext):
    logger.info(f'Add date {message.text} | user {message.from_user.id}')

    async with state.proxy() as data:
        data['date'] = message.text

    await Place.next()
    return await message.reply('Введи цену или средний чек. Если посещение свободное, введи 0 😘')

@dp.message_handler(state=Place.price)
async def price_process(message: types.Message, state: FSMContext):
    logger.info(f'Add price {message.text} | user {message.from_user.id}')

    async with state.proxy() as data:
        data['price'] = message.text

    await state.finish()
    return await message.reply('Всё, супер 😘')

