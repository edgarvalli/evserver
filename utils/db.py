import re
from utils.tools import get_config
import mysql.connector as _mysql
import mysql.connector.errors as _mysql_errors


class mysql:

    @staticmethod
    def get_connection() -> _mysql.MySQLConnection:
        config = get_config()['mysql']

        try:
            sql = _mysql.connect(**config)
            return sql
        except KeyError as e:
            raise ValueError(e)


    @staticmethod
    def fetchone(query: str, args: tuple = ()) -> dict:
        sql = mysql.get_connection()
        cursor = sql.cursor(dictionary=True)
        cursor.execute(query, args)
        data = cursor.fetchone()
        cursor.close()
        sql.close()
        return data

    @staticmethod
    def fetchall(query: str, args: tuple = ()) -> list[dict]:
        sql = mysql.get_connection()
        cursor = sql.cursor(dictionary=True)
        cursor.execute(query, args)
        data = cursor.fetchall()
        cursor.close()
        sql.close()
        return data

    @staticmethod
    def commit(query: str, args: tuple = ()) -> dict:
        sql = mysql.get_connection()
        cursor = sql.cursor()
        cursor.execute(query, args)
        data = {"error": False, "message": "", "lastrowid": cursor.lastrowid}
        sql.commit()
        cursor.close()
        sql.close()
        return data

    @staticmethod
    def executemany(query: str, args: list[tuple] = []):
        sql = mysql.get_connection()
        cursor = sql.cursor()
        cursor.executemany(query, args)
        data = {"error": False, "message": "", "lastrowid": cursor.lastrowid}
        sql.commit()
        cursor.close()
        sql.close()
        return data
    
    @staticmethod
    def search(model: str, **kvargs) -> list[dict]:
        sql = mysql.get_connection()
        cursor = sql.cursor(dictionary=True)

        limit = kvargs.get('limit', 50)
        orderby = kvargs.get('orderby', None)
        fields = kvargs.get('fields','*')
        args_excluded = ['limit', 'orderby', 'fields']

        for arg in args_excluded:
            if arg in kvargs:
                del kvargs[arg]

        query = "SELECT {} FROM {}".format(fields, model)
        
        wheres = []

        for k,v in kvargs.items():
        
            if str(v).lower().startswith('startswith'):
                value = re.search(r'"(.*?)"', v)
                if value:
                    value = value[1]
                    wheres.append(f"{k} LIKE '{value}%'")

            elif str(v).lower().startswith('endswith'):
                value = re.search(r'"(.*?)"', v)
                if value:
                    value = value[1]
                    wheres.append(f"{k} LIKE '%{value}'")

            elif str(v).lower().startswith('contains'):
                value = re.search(r'"(.*?)"', v)
                if value:
                    value = value[1]
                    wheres.append(f"{k} LIKE '%{value}%'")
            else:
                try:
                    value = int(v)
                    wheres.append(f"{k} = {value}")
                except:
                    wheres.append(f"{k} = '{v}'")
        
        if len(wheres) > 0:
            wheres = " AND ".join(wheres)
            query += " WHERE " + wheres
        
        if orderby is not None:
            query += " ORDER BY " + orderby
        
        query += " LIMIT {}".format(limit)
        
        print(query)
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        sql.close()
        return data
    
    @staticmethod
    def save(model: str, **kvargs) -> dict:

        sql = mysql.get_connection()
        cursor = sql.cursor()

        fields = ", ".join(kvargs.keys())
        placeholders = " ,".join(["%s" for _ in kvargs.keys()])
        values = tuple([v for v in kvargs.values()])

        query = f"INSERT IGNORE INTO {model} ({fields}) VALUES ({placeholders})"
        cursor.execute(query, values)
        data = {"error": False, "message": "", "lastrowid": cursor.lastrowid}
        sql.commit()
        cursor.close()
        sql.close()

        return data