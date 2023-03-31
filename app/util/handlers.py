import re

from aiogram import types
from loguru import logger
from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from .settings import *
from db.helpers_db import Database

class Place(StatesGroup):
    name = State()
    address = State()
    category = State()
    date = State()
    price = State()

class Get(StatesGroup):
    category = State()

class Del(StatesGroup):
    name = State()

db = Database(USER_DB, HOST_DB, PASSWORD_DB)
db.create_db()

@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state:FSMContext):
    logger.info(f'Start user {message.from_user.id}')
    await state.finish()
    await message.answer('Привет, я бот, который помогает сохранять интересные места 😘')

# ----------------------------------- Добавление ---------------------------------------------

@dp.message_handler(commands=['add'])
async def add_process(message: types.Message):
    logger.info(f'Add process start user {message.from_user.id}')
    await Place.name.set()
    await message.answer('Введи название места 😘')

@dp.message_handler(state=Place.name)
async def name_process(message: types.Message, state: FSMContext):
    logger.info(f'Add name {message.text} | user {message.from_user.id}')
    
    async with state.proxy() as data:
        data['name'] = message.text

    await Place.next()
    await message.answer('Введи адрес места 😘')

@dp.message_handler(state=Place.address)
async def adress_process(message: types.Message, state: FSMContext):
    logger.info(f'Add address {message.text} | user {message.from_user.id}')
    
    async with state.proxy() as data:
        data['address'] = message.text

    await Place.next()
    await message.answer('Введи категорию из данного списка:\n{}\n😘'.format(', '.join(categories)))

@dp.message_handler(lambda message: message.text not in categories, state=Place.category)
async def category_process_invalid(message: types.Message):
    logger.error(f'Wrong category | {message.text} | user {message.from_user.id}')
    return await message.answer('Давай по новой 😘\nВыбери категорию из данного списка:\n{}'.format(', '.join(categories)))

@dp.message_handler(lambda message: message.text == 'Мероприятие', state=Place.category)
async def category_process_event(message: types.Message, state:FSMContext):
    logger.info(f'Add category {message.text} | user {message.from_user.id}')

    async with state.proxy() as data:
        data['category'] = message.text

    await Place.next()
    return await message.answer('Введи дату мероприятия в формате \"дд.мм.гггг чч:мм\" или \"дд.мм.гггг\"😘')

@dp.message_handler(lambda message: message.text != 'Мероприятие', state=Place.category)
async def category_process_other(message: types.Message, state:FSMContext):
    logger.info(f'Add category {message.text} | user {message.from_user.id}')

    async with state.proxy() as data:
        data['category'] = message.text
    
    for i in range(2):
        await Place.next()
    return await message.answer('Введи цену или средний чек. Если посещение свободное, введи 0 😘')

@dp.message_handler(state=Place.date)
async def date_process(message: types.Message, state: FSMContext):

    date_lst = message.text.split()

    if len(date_lst) == 1:
        try:
            data_date = datetime.strptime(message.text, "%d.%m.%Y")
        except ValueError:
            logger.error(f'Add date {message.text} | user {message.from_user.id}')
            return await message.answer('Неверный формат даты. Введи дату в формате \"дд.мм.гггг чч:мм\" или \"дд.мм.гггг\"')
    else:
        try:
            data_date = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        except ValueError:
            logger.error(f'Add date {message.text} | user {message.from_user.id}')
            return await message.answer('Неверный формат даты. Введи дату в формате \"дд.мм.гггг чч:мм\" или \"дд.мм.гггг\"')
    
    if data_date < datetime.now():
        logger.error(f'Add date {message.text} | user {message.from_user.id}')
        return await message.answer('Хватит жить прошлым😘\nВведи свое настоящее будущее')

    logger.info(f'Add date {message.text} | user {message.from_user.id}')
    async with state.proxy() as data:
                data['date'] = data_date

    await Place.next()
    return await message.answer('Введи цену или средний чек. Если посещение свободное, введи 0 😘')

@dp.message_handler(state=Place.price)
async def price_process(message: types.Message, state: FSMContext):

    pattern = re.compile(r'^[\d]+[\.]?[\d]{0,2}$')

    if pattern.match(message.text):
        logger.info(f'Add price {message.text} | user {message.from_user.id}')
        async with state.proxy() as data:
            data['price'] = message.text
    else:
        logger.error(f'Add price {message.text} | user {message.from_user.id}')
        return await message.answer('Это не число...\nВведи число\nПример: 1024.12')


    db.insert_place(await state.get_data())
    await state.finish()
    return await message.answer('Всё, супер 😘')

# ----------------------------------- Поиск ---------------------------------------------

@dp.message_handler(commands=['get'])
async def get_place(message: types.Message):
    logger.info(f'Get places')
    await Get.category.set()
    await message.answer('Введи категорию места, в которое хочешь пойти 😘')

@dp.message_handler(state=Get.category)
async def get_process(message: types.Message, state: FSMContext):
    logger.info(f'Get category {message.text} | user {message.from_user.id}')
    
    out = db.extract_place(message.text)
    
    if len(out) == 0:
        return await message.answer('У вас ещё нет мест в этой категории 😘')

    result = ''
    if message.text == 'Мероприятие':
        for place in out:
            result += f'Место: {place[0]}\nАдрес: {place[1]}\nДата: {place[2]}\nЦена: {place[3]}\n\n'
    else:
        for place in out:
            result += f'Место: {place[0]}\nАдрес: {place[1]}\nЦена: {place[2]}\n\n'
                    
    logger.info(f'Show places | category {message.text} | user {message.from_user.id}')
    await state.finish()
    return await message.answer(f'Вот интересные места по данному запросу 😘\n\n{result}')

# ----------------------------------- Удаление ---------------------------------------------

@dp.message_handler(commands=['del'])
async def del_place(message: types.Message):
    logger.info(f'Delete place')
    await Del.name.set()
    await message.answer('Введи название места, которое хочешь удалить 😘')

@dp.message_handler(state=Del.name)
async def del_process(message: types.Message, state: FSMContext):
    
    dl = db.del_place(message.text)
    logger.info(dl)

    logger.info(f'Delete place {message.text} | user {message.from_user.id}')
    await state.finish()

    if len(dl) == 0:
        return await message.answer(f'Места {message.text} нет')
    return await message.answer(f'{message.text} удалено 😘')
