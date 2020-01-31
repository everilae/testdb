# testdb

Test tool for various DBMS, and [SQLAlchemy](https://www.sqlalchemy.org/)

# Installing

With all the extras:

```bash
pip install 'git+https://github.com/everilae/testdb.git#egg=testdb[postgres,mysql,mssql]'
```

Docker is required to run PostgreSQL, MySQL, and SQL Server. The tool will launch a container after selecting the backend, if needed. [Microsoft ODBC Driver 17 for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15) is required for SQL Server and PyODBC.

# Usage

```python
In [1]: from testdb import *
Choose database backend (default SQLite):
 [0] SQLite
 [1] Postgresql (psycopg2)
 [2] MySQL (connector)
 [3] MySQL (pymysql)
 [4] MySQL (MySQLdb)
 [5] MS SQL Server (pymssql)
 [6] MS SQL Server (pytds)
 [7] MS SQL Server (pyodbc)
>>> 0
Echo? [Y/n] >>> y
Echo pool? [y/N] >>> n

In [2]: engine
Out[2]: Engine(sqlite://)

In [3]: engine.execute('select 1').fetchone()
2020-01-31 15:41:05,469 INFO sqlalchemy.engine.base.Engine SELECT CAST('test plain returns' AS VARCHAR(60)) AS anon_1
2020-01-31 15:41:05,469 INFO sqlalchemy.engine.base.Engine ()
2020-01-31 15:41:05,471 INFO sqlalchemy.engine.base.Engine SELECT CAST('test unicode returns' AS VARCHAR(60)) AS anon_1
2020-01-31 15:41:05,471 INFO sqlalchemy.engine.base.Engine ()
2020-01-31 15:41:05,471 INFO sqlalchemy.engine.base.Engine select 1
2020-01-31 15:41:05,471 INFO sqlalchemy.engine.base.Engine ()
Out[3]: (1,)

In [4]: class Foo(Base):
   ...:     __tablename__ = 'foo'
   ...:     id = Column(Integer, primary_key=True)
   ...:     data = Column(String)
   ...:

In [5]: metadata.create_all()
2020-01-31 15:41:38,235 INFO sqlalchemy.engine.base.Engine PRAGMA main.table_info("foo")
2020-01-31 15:41:38,235 INFO sqlalchemy.engine.base.Engine ()
2020-01-31 15:41:38,236 INFO sqlalchemy.engine.base.Engine PRAGMA temp.table_info("foo")
2020-01-31 15:41:38,236 INFO sqlalchemy.engine.base.Engine ()
2020-01-31 15:41:38,237 INFO sqlalchemy.engine.base.Engine 
CREATE TABLE foo (
        id INTEGER NOT NULL, 
        data VARCHAR, 
        PRIMARY KEY (id)
)


2020-01-31 15:41:38,237 INFO sqlalchemy.engine.base.Engine ()
2020-01-31 15:41:38,237 INFO sqlalchemy.engine.base.Engine COMMIT

In [6]: session.query(Foo).all()
2020-01-31 15:41:46,172 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
2020-01-31 15:41:46,173 INFO sqlalchemy.engine.base.Engine SELECT foo.id AS foo_id, foo.data AS foo_data 
FROM foo
2020-01-31 15:41:46,173 INFO sqlalchemy.engine.base.Engine ()
Out[6]: []
```
