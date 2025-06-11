import mysql.connector as MySQLDriver
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.errors import ProgrammingError, IntegrityError
from dataclasses import dataclass
from typing import Union, Optional, List, Dict, Tuple


def where_conditionals(conditionals: Dict = {}) -> str:
    where = []
    keys = conditionals.keys()
    for k in keys:
        try:
            v = int(conditionals[k])
            where.append(f"{k}={v}")
        except:
            v = conditionals[k]
            where.append(f"{k}='{v}'")

    return " and ".join(where)


@dataclass
class MySQLResponse:
    error: bool
    message: str
    data: Union[List[Dict], List[Tuple], Dict, None]
    insertedid: Optional[int] = 0


@dataclass
class MySQL:

    host: str
    password: str
    user: str
    database: str
    dictionary: Optional[bool] = True
    connection: Optional[
        Union[MySQLDriver.pooling.PooledMySQLConnection, MySQLConnectionAbstract]
    ] = None

    def connect(self):

        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = MySQLDriver.connect(
                    user=self.user,
                    host=self.host,
                    password=self.password,
                    database=self.database,
                )
        except MySQLDriver.errors.Error as e:
            raise e

    def close(self):
        if self.connection is not None:
            if self.connection.is_connected():
                self.connection.close()
                self.connection = None

    def cursor(self, dictionary=True) -> MySQLCursorAbstract:
        if self.connection is None:
            self.connect()

        if self.connection.is_connected():
            return self.connection.cursor(dictionary=dictionary)
        else:
            return None

    def setdb(self, dbname):
        self.connection.database = dbname

    def query(self, query, args=()) -> MySQLCursorAbstract:
        self.connect()
        cursor = self.connection.cursor(dictionary=self.dictionary)
        try:
            cursor.execute(query, args)
            return cursor

        except ProgrammingError as e:
            print("Ocurrio un error: " + e.msg)
            raise e
        except:
            cursor.close()
            raise "Ocurrio un error al ejecutar la sentencia"

    def insert(self, model: str, data: dict = {}) -> MySQLResponse:
        if not data:
            return MySQLResponse(
                error=True, message="No data provided for insert.", data=None
            )
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        query = f"INSERT INTO {model} ({columns}) VALUES ({placeholders})"
        try:
            cursor = self.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            inserted_id = cursor.lastrowid
            cursor.close()
            return MySQLResponse(
                error=False,
                message="Insert successful.",
                data=None,
                insertedid=inserted_id,
            )
        except Exception as e:
            return MySQLResponse(error=True, message=str(e), data=None)

    def dbexists(self, dbname: str) -> bool:
        query = "SHOW DATABASES"
        exists_cursor = self.cursor(dictionary=True)
        exists_cursor.execute(query)

        dbexists = False
        for db in exists_cursor.fetchall():
            if db["Database"] == dbname:
                dbexists = True
                break

        exists_cursor.close()

        return dbexists

    def commit(self, query, args=()) -> MySQLResponse:
        try:
            cursor = self.cursor()
            cursor.execute(query, args)
            self.connection.commit()
            response = MySQLResponse(
                error=False,
                message="Query ejecutado correctamente!!",
                data={},
                insertedid=cursor.lastrowid,
            )
            cursor.close()
            return response

        except IntegrityError as e:
            return MySQLResponse(error=True, message=e.msg, data={}, insertedid=e.args)

    def fetchall(
        self, model, fields: str = "*", conditionals: dict = None
    ) -> MySQLResponse:
        query = "SELECT {} FROM {} ".format(fields, model)

        if conditionals is not None:
            query += "WHERE {}".format(where_conditionals(conditionals))

        cursor = self.query(query)
        return MySQLResponse(error=False, message="", data=cursor.fetchall())

    def fetchone(
        self, model, fields: str = "*", conditionals: dict = None
    ) -> MySQLResponse:

        query = "SELECT {} FROM {} ".format(fields, model)

        if conditionals is not None:
            query += "WHERE {}".format(where_conditionals(conditionals))

        cursor = self.query(query)

        return MySQLResponse(error=False, message="", data=cursor.fetchone())
