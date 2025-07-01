import sqlite3
class db:
    def __init__(self):
        self.conn= sqlite3.connect("game.db")
        self.cur= self.conn.cursor()
        self.conn.commit
        self.create_table('players','id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL UNIQUE, password TEXT NOT NULL')
    def create_table(self,name,columns):
        query = f"CREATE TABLE IF NOT EXISTS {name} ({columns})"
        self.cur.execute(query)
        self.conn.commit()

    def query(self,table,*item,where_clause=None):
        if not item:
            select_columns = '1'
        else:
            select_columns = ",".join(items)
        sql_query = f'SELECT {select_columns} FROM {table}'
        if where_clause:
            sql_query += f" Where {where_clause}"
        sql_query += " LIMIT 1;"
        self.cur.execute(sql_query)
        result = self.cur.fetchone()
        return result is not None
    def insert(self,table,columns,values):
        if not columns or not values:
            raise ValueError("Number of columns must match number of values")
        if len(columns) != len(values):
            raise ValueError("Number of columns must equal number of values")
        insert_columns = ','.join(columns)
        placeholders = ','.join(['?'] * len(values))
        sql_query = f'INSERT INTO {table} ({insert_columns}) VALUES ({placeholders});'
        try:
            self.cur.execute(sql_query,values)
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
