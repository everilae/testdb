from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import sessionmaker, relationship, column_property, \
    backref, configure_mappers, aliased, mapper, joinedload, contains_eager
from sqlalchemy import create_engine, table, column, func, case, and_, or_, \
    not_, select, join, outerjoin, exists, bindparam, literal, \
    literal_column, text
from sqlalchemy import Table as _Table, Column, ForeignKey, Integer, \
    SmallInteger, Float, Boolean, String, Unicode, Text, UnicodeText, Date, \
    Time, DateTime, Numeric, Index, MetaData
from sqlalchemy import VARCHAR, INTEGER
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.url import URL as _URL

import re as _re
import secrets as _secrets

_CAMEL_TO_SNAKE = _re.compile(r'(?<=[a-z])([A-Z])')

try:
    input = raw_input

except NameError:
    pass

_POSTGRES_DATABASE = None
_POSTGRES_USER = 'postgres'
_POSTGRES_PORT = (5432, 54321)
_POSTGRES_IMAGE = 'postgres:12-alpine'

_MYSQL_DATABASE = 'mysli'
_MYSQL_USER = 'mysli'
_MYSQL_PORT = (3306, 33060)
_MYSQL_IMAGE = 'mysql/mysql-server:latest'

_MSSQL_DATABASE = None
_MSSQL_USER = 'sa'
_MSSQL_PORT = (1433, 14333)
_MSSQL_IMAGE = 'mcr.microsoft.com/mssql/server:2017-latest'
_MSSQL_DRIVER = 'ODBC Driver 17 for SQL Server'

def _dummy_env(_username, _password, _database):
    return {}

def _postgres_env(_username, password, _database):
    return {
        'POSTGRES_PASSWORD': password,
    }

def _mysql_env(username, password, database):
    return {
        'MYSQL_ROOT_PASSWORD': password,
        'MYSQL_USER': username,
        'MYSQL_PASSWORD': password,
        'MYSQL_DATABASE': database,
    }

def _mssql_env(_username, password, _database):
    return {
        'ACCEPT_EULA': 'Y',
        'SA_PASSWORD': password,
    }

_DBS = [
    ('SQLite', 'sqlite',
     None, None, None, None,
     None, None),

    ('Postgresql (psycopg2)', 'postgresql',
     _POSTGRES_DATABASE, _POSTGRES_USER, _POSTGRES_PORT, _POSTGRES_IMAGE,
     None, _postgres_env),

    ('MySQL (connector)', 'mysql+mysqlconnector',
     _MYSQL_DATABASE, _MYSQL_USER, _MYSQL_PORT, _MYSQL_IMAGE,
     None, _mysql_env),

    ('MySQL (pymysql)', 'mysql+pymysql',
     _MYSQL_DATABASE, _MYSQL_USER, _MYSQL_PORT, _MYSQL_IMAGE,
     None, _mysql_env),

    ('MySQL (MySQLdb)', 'mysql+mysqldb',
     _MYSQL_DATABASE, _MYSQL_USER, _MYSQL_PORT, _MYSQL_IMAGE,
     None, _mysql_env),

    ('MS SQL Server (pymssql)', 'mssql+pymssql',
     _MSSQL_DATABASE, _MSSQL_USER, _MSSQL_PORT, _MSSQL_IMAGE,
     {'charset': 'utf8'}, _mssql_env),

    ('MS SQL Server (pytds)', 'mssql+pytds',
     _MSSQL_DATABASE, _MSSQL_USER, _MSSQL_PORT, _MSSQL_IMAGE,
     None, _mssql_env),

    ('MS SQL Server (pyodbc)', 'mssql+pyodbc',
     _MSSQL_DATABASE, _MSSQL_USER, _MSSQL_PORT, _MSSQL_IMAGE,
     {'driver': _MSSQL_DRIVER}, _mssql_env),
]

def _format_db_menu(dbs):
    menu = '\n'.join([f' [{k}] {desc}' for k, (desc, *_rest) in enumerate(dbs)])
    return f'Choose database backend (default SQLite):\n{menu}\n>>> '

def _drivername_to_name(drivername):
    return drivername.split('+')[0]

def _start_container(image, name, ports, env=None):
    import docker
    container_port, host_port = ports
    ports = {f'{container_port}/tcp': host_port}
    client = docker.from_env()
    client.containers.run(image, name=name, detach=True, ports=ports,
                          environment=env)
    return 'localhost', host_port

def _create_engine():
    image = None
    args = None
    hostname = None
    port = None
    password = None

    choice = int(input(_format_db_menu(_DBS)) or '0')
    (_, drivername,
     database, username, ports, image,
     query, env_factory) = _DBS[choice]

    if image:
        password = _secrets.token_urlsafe()
        name = 'testdb-' + _drivername_to_name(drivername)
        hostname, port = _start_container(
            image, name, ports, env=env_factory(username, password, database))

        print(f'Superuser password: {password}')

    echo = input('Echo? [Y/n] >>> ').lower() in {'', 'y'}
    echo_pool = input('Echo pool? [y/N] >>> ').lower() in {'y'}

    url = _URL(drivername, username=username, password=password,
               host=hostname, port=port, query=query, database=database)
    return create_engine(url, echo=echo, echo_pool=echo_pool)

engine = _create_engine()
Base = declarative_base()
Base.metadata.bind = engine
metadata = Base.metadata
Session = sessionmaker()
# Common names for a session (both scoped and not so)
DBSession = session = Session()


class Model(Base):
    '''
    A bare minimum implementation for a Flask-SQLAlchemy compatible base. The
    end goal is to be able to run most code snippets with as little
    modifications as possible.
    '''

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return _CAMEL_TO_SNAKE.sub(
            lambda m: '_{}'.format(m.group(1)), cls.__name__).lower()


def make_table(spec):
    tbl_cols = spec.strip().split()
    return table(tbl_cols[0], *(column(c) for c in tbl_cols[1:]))


def Table(*args, **kwgs):
    if len(args) < 2 or not isinstance(args[1], MetaData):
        args = args[:1] + (metadata,) + args[1:]
    return _Table(*args, **kwgs)
