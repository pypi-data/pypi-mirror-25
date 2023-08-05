from sqlian.standard import Database

from .engines import Engine


class SQLite3Database(Database):
    dbapi2_module_name = 'sqlite3'
    engine_class = Engine
