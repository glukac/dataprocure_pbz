from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

_DATABASES = {
    'local': {
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'DB_HOSTNAME',
        'PORT': 5432
    }
}

_db = _DATABASES['local']


def postgresql_engine():
    engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
        user=_db['USER'],
        password=_db['PASSWORD'],
        host=_db['HOST'],
        port=_db['PORT'],
        database=_db['NAME'],
    )
    return create_engine(engine_string)

engine = postgresql_engine()

Session = sessionmaker(bind=engine)

Base = declarative_base()
