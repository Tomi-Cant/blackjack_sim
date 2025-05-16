import sqlite3 

def create_connection(db_file):
    #create a database connection to the SQLite database
    #return: Connection object or None
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.cursor
    except Exception as e:
        print(e)
    return conn

def create_table(conn,table, columns):
    col = ",".join(columns)
    sql = f'''CREATE TABLE IF NOT EXISTS {table}( id INTEGER PRIMARY KEY, {col});'''
    conn.execute(sql)
    
def insert_db(conn,table, columns,data,images=False):
    
    if images:
        sql=f'''INSERT INTO {table} {tuple(columns)} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''
        conn.execute(sql,data)
    else:
        sql=f'''INSERT INTO {table} {tuple(columns)} VALUES {tuple(data)};'''
        conn.execute(sql)
    conn.commit()

    
def select_db(conn,table,columns_and_data=None):
    if not columns_and_data==None:
        col = " AND ".join(columns_and_data)
        sql=f'''SELECT * FROM {table} WHERE {col}'''
        return conn.execute(sql)
    else:
        sql =f"SELECT * from {table}"
        return conn.execute(sql)
    
def update_db(conn,table,columns_and_data,where_to_update):
    col = ",".join(columns_and_data)
    sql = f"UPDATE {table} set {col} where {where_to_update}"
    conn.execute(sql)
    conn.commit()  
    
def delete_db(conn,table,column,what_to_remove,delete_all=False):
    if delete_all:
        sql=f'''DELETE FROM {table}'''
    else:
        sql=f'''DELETE FROM {table} WHERE {column} = "{what_to_remove}"'''
    conn.execute(sql)
    conn.commit()  
    
    
def get_columns(conn,table,start_index=0,end_index=0):
    #https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite
    sql=f'select * from {table}'
    cursor= conn.execute(sql)
    names= [description[0] for description in cursor.description]
    if end_index:
        return names[start_index:end_index]
    else:
        return names[start_index:]

def swap_item(conn,first_id,second_id,table,col='slot'):
    #chatgpt for the sql
       
        conn.execute("BEGIN TRANSACTION;")
        sql =f"""
        UPDATE {table} 
        SET {col} = CASE
                        WHEN {col} = ? THEN -1
                        WHEN {col} = ? THEN ?
                    END
        WHERE {col} IN (?, ?);
    
        """ # "transaction" makes it so all changes happen at once
    
        # try:
        conn.execute(sql, (first_id, second_id, first_id, first_id, second_id))  
            
        sql=f"""
            UPDATE {table}
            SET {col} = ?
            WHERE {col} = -1;
            """ 
        conn.execute(sql, (second_id,))
        conn.execute("COMMIT;")
        # except sqlite3.Error as e:
        # # Rollback in case of an error
        #     conn.rollback()
        #     print("An error occurred:", e)