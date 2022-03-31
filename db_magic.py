from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Date

from settings import DATABASE
from read_data import read_games, read_toys

import datetime


def connection():
    drivername = DATABASE['drivername']
    user = DATABASE["username"]
    password = DATABASE["password"]
    host = DATABASE["host"]
    database_name = DATABASE["database"]
    engine = create_engine(
        f"{drivername}://{user}:{password}@{host}/{database_name}",
        echo=True, pool_size=10, max_overflow=15, pool_recycle=3600)

    return engine


def create_table(engine):

    metadata = MetaData()

    toys = Table('toys', metadata,
        Column('id', Integer(), primary_key=True),
        Column('toy_id', Integer(), nullable=False, unique=True),
        Column('name', String(200), nullable=False, unique=True),
        Column('status', String(200),  nullable=False),
        Column('status_updated', Date(),  nullable=False, default=datetime.date.today()),
    )

    games = Table('games', metadata,
        Column('id', Integer(), primary_key=True),
        Column('name', String(200), nullable=False, unique=True),
        Column('game_id', Integer(), nullable=False, unique=True),
        Column('date', Date(),  nullable=False),
    )

    toys_games = Table('toys_games', metadata,
        Column('id', Integer(), primary_key=True),
        Column('game_id', Integer(), nullable=False),
        Column('toy_id', Integer(), nullable=False),
        Column('note', Text(), nullable=False,),
    )

    metadata.create_all(engine)

    contentx = {
        'toys':toys,
        'games': games,
        'toys_games':toys_games,
    }

    return contentx


def insert_table_toys(engine, toys):
    informatins = read_toys()['toys']

    for elem in informatins:
        ins = toys.insert().values(
            toy_id=elem['id'],
            name=elem['name'],
            status=elem['status'],
            status_updated=elem['status_updated']
        )
        engine.connect().execute(ins)


def insert_table_games(engine, games):
    informatins = read_games()['games']

    for elem in informatins:
        ins = games.insert().values(
            game_id=elem['id'],
            name=elem['name'],
            date=elem['date']
        )
        engine.connect().execute(ins)


def insert_table_toys_games(engine, toys_games):
    informatins = read_toys()['toys']

    for elem in informatins:
        for game in elem['games']:
            ins = toys_games.insert().values(
                toy_id=elem['id'],
                game_id=game['id'],
                note=game['note']
            )
            engine.connect().execute(ins)



if __name__ == '__main__':
    # Подключение к Базе данных
    engine = connection()
    # Создаем в базе данных необходимые таблицы
    tables = create_table(engine)

    # Поочередно заполняем таблиц
    insert_table_toys(engine, tables['toys'])
    insert_table_games(engine, tables['games'])
    insert_table_toys_games(engine, tables['toys_games'])

