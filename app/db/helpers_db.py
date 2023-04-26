from loguru import logger
from mysql.connector import connect, Error

from .settings_db import *

class Database:
    def __init__(self, user:str, host:str, password:str) -> None:
            self.user = user
            self.host = host
            self.password = password

    def create_db(self) -> None:
        """
        Инициализируются база данных и таблицы
        """
        try:
            with connect(
                user = self.user,
                host = self.host,
                password = self.password
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET 'utf8'")
                    logger.info(f'Create database {DB_NAME}')
        except Error as e:
            logger.error(f'Error connect database: {e}')

        try:
            with connect(
                user = self.user,
                host = self.host,
                password = self.password,
                database = DB_NAME,
            ) as connection:
                with connection.cursor() as cursor:
                    for table in TABLES:
                        cursor.execute(TABLES[table])
                        logger.info(f'Create table {table}')
        except Error as e:
            logger.error(f'Error add table database: {e}')
                

    def insert_place(self, data:dict) -> None:
        """
        Добавление новой записи в таблицу
        """
        if 'date' not in data:
            data['date'] = None

        push_data = []
        for key in ('name', 'address', 'category', 'date', 'price'):
            push_data.append(data[key])

        try:
            with connect(
                user = self.user,
                host = self.host,
                password = self.password,
                database = DB_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    logger.info(push_data)
                    cursor.execute(f"""INSERT INTO places (
                                name_place, address_place, category, date_time, price)
                                VALUES (%s, %s, %s, %s, %s)
                                """, push_data)
                    logger.info(f'Insert row {cursor.fetchall()}')
                connection.commit()
        except Error as e:
            logger.error(f'Error connect database: {e}')

    def extract_place(self, ctg):
        """
        Извлечение записей из таблицы
        """
        try:
            with connect(
                user = self.user,
                host = self.host,
                password = self.password,
                database = DB_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    if ctg == 'Мероприятие':
                        cursor.execute(f"""SELECT 
                        name_place, address_place, date_time, price
                        FROM places
                        WHERE category = '{ctg}'
                        ORDER BY price
                        """)
                    else:
                        cursor.execute(f"""SELECT 
                        name_place, address_place, price
                        FROM places
                        WHERE category = '{ctg}'
                        ORDER BY price
                        """)
                    logger.info(f'Extract values {ctg}')
                    res = cursor.fetchall()
                    
                    return res

        except Error as e:
            logger.error(f'Error connect database: {e}')

    def del_place(self, name):
        """
        Удаление записи из таблицы
        """
        try:
            with connect(
                user = self.user,
                host = self.host,
                password = self.password,
                database = DB_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(f""" SELECT * FROM places
                    WHERE name_place = '{name}'
                    """)
                    res = cursor.fetchall()    

                with connection.cursor() as cursor:
                    cursor.execute(f""" DELETE FROM places
                    WHERE name_place = '{name}'
                    """)
                    logger.info(f'Delete value {name}')
                connection.commit()

                return res

        except Error as e:
            logger.error(f'Error connect database: {e}')

