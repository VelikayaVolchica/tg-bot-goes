DB_NAME = 'goes'

TABLES = {}

# Исправить id_category на TINYINT и связать с другой таблицей
TABLES['places'] = """
    CREATE TABLE IF NOT EXISTS places(
    id_place SMALLINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name_place VARCHAR(255) NOT NULL,
    address_place VARCHAR(255) NOT NULL,
    id_category VARCHAR(20) NOT NULL,
    date_time DATETIME,
    price DECIMAL(8, 2) NOT NULL
);
"""

TABLES['categories'] = """
    CREATE TABLE IF NOT EXISTS categories(
    id_category TINYINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(20)
);
"""