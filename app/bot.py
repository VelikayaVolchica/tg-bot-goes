import sys

from aiogram.utils import executor
from loguru import logger

from util.settings import dp
from util.handlers import *

if __name__ == '__main__':
    logger.remove()
    logger.add(
        sys.__stdout__,
        format='[{time:YYYY-MM-DD:mm:ss}] {level} | {message}',
        level='TRACE',
        colorize=True
    )

    executor.start_polling(dp, skip_updates=True)