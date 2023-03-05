import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

file_ini = pathlib.Path(__file__).joinpath('config.ini')
config = configparser.ConfigParser()
config.read('config.ini')

username = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
database_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')
port = config.get('DB', 'PORT')

url = f'postgresql://{username}:{password}@{domain}:{port}/{database_name}'

engine = create_engine(url, echo=False)
DBSession = sessionmaker(bind=engine)
session = DBSession()
