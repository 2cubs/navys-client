import sqlite3


class DB:

    _path = 'navys.db'

    def __init__(self):
        try:
            self._connection = sqlite3.connect(self._path)
        except Exception as e:
            print(e)

    def insert(self, table, **kwargs):

        fields, values = list(kwargs.keys()), list(kwargs.values())
        fields = ','.join(fields)
        placeholders = ','.join(['?' for _ in values])
        query = f'INSERT INTO {table}({fields}) VALUES({placeholders})'

        try:
            cursor = self._connection.cursor()
            cursor.execute(query, values)
            self._connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(e)

    def select(self, table, **kwargs):

        query = f'SELECT * FROM {table}'

        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(e)

    def update(self, table, pk, **kwargs):

        fields, values = list(kwargs.keys()), list(kwargs.values())
        fields = ','.join([f'{field}=?' for field in fields])
        where = f'{self.get_primary_key(table)}={pk}'
        query = f'UPDATE {table} SET {fields} WHERE {where}'

        try:
            cursor = self._connection.cursor()
            cursor.execute(query, values)
            self._connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(e)


    def delete(self, table, **kwargs):

        fields, values = list(kwargs.keys()), list(kwargs.values())
        where = ' AND '.join([f'{field}=?' for field in fields])
        query = f'DELETE FROM {table} WHERE {where}'

        try:
            cursor = self._connection.cursor()
            cursor.execute(query, values)
            self._connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(e)

    def _get_table_info(self, table):

        query = f'PRAGMA table_info({table})'

        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(e)

    def get_primary_key(self, table):
        table_info = self._get_table_info(table)
        for col in table_info:
            if col['pk'] == 1:
                return col['name']

    def get_columns(self, table):
        return [key['name'] for key in self._get_table_info(table)]
