import sqlite3
class db:
    def __init__(self):
        self.conn= sqlite3.connect("game.db")
        self.cur= self.conn.cursor()
        self.conn.commit()
        self.create_table('players','id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT NOT NULL UNIQUE, password TEXT NOT NULL')
    def create_table(self,name,columns):
        query = f"CREATE TABLE IF NOT EXISTS {name} ({columns})"
        self.cur.execute(query)
        self.conn.commit()

    def exists(self,table,where_clause_template=None,params=None):
        sql_query = f'SELECT 1 FROM {table}'
        if where_clause_template:
            sql_query += f" Where {where_clause_template}"
        sql_query += " LIMIT 1;"
        try:
            self.cur.execute(sql_query,params if params is not None else ())
            result = self.cur.fetchone()
            return result is not None
        except sqlite3.Error as e:
            print(f"Database exists error: {e}") 
            # For a SELECT, rollback is not strictly necessary as no changes are made,
            # but it doesn't hurt and keeps pattern consistent.
            self.conn.rollback() 
            return False # Return False on error, as existence can't be confirmed
    def fetchone(self,table,columns,where_clause_template,params):
        select_columns = ','.join(columns)
        sql_query = f'SELECT {select_columns} FROM {table}'
        if where_clause_template:
            sql_query += f" WHERE {where_clause_template}"
        sql_query += " LIMIT 1;"
        try:
            self.cur.execute(sql_query,params if params is not None else ())
            result = self.cur.fetchone()

            if result:
                return dict(zip(columns,result))
            return None
        except sqlite3.Error as e:
            print(f"Database fetchone error: {e}")
            self.conn.rollback() # Rollback in case of an error during fetch
            return None
        
       
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
