DB_NAME = 'goes'

TABLES = {}

TABLES['places'] = """
    CREATE TABLE IF NOT EXISTS places(
    id_place SMALLINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name_place VARCHAR(255) NOT NULL,
    address_place VARCHAR(255) NOT NULL,
    category VARCHAR(20) NOT NULL,
    date_time DATETIME,
    price DECIMAL(10,2) NOT NULL
);
"""