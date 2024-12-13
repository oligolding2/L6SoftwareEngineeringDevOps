import sqlite3

conn = sqlite3.connect('static/database.db')

curs = conn.cursor()

def mortgage(curs,conn):
    curs.execute('''CREATE TABLE IF NOT EXISTS mortgage(
                [mortgage_id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
                [owner] TEXT NOT NULL,
                [location] TEXT NOT NULL,
                [value] TEXT NOT NULL,
                [inserted_by] TEXT NOT NULL)''')

    curs.execute('''INSERT INTO mortgage (owner,location,value,inserted_by) VALUES('Alan Smith','London','3650000','ogolding');''')
    curs.execute('''INSERT INTO mortgage (owner,location,value,inserted_by) VALUES('John Jones','Bristol','870000','ogolding');''')
    curs.execute('''INSERT INTO mortgage (owner,location,value,inserted_by) VALUES('William Williams','Cardiff','2845000','ogolding');''')            
    curs.execute('''INSERT INTO mortgage (owner,location,value,inserted_by) VALUES('Rachel Adams','Liverpool','198000','ogolding');''')
    curs.execute('''INSERT INTO mortgage (owner,location,value,inserted_by) VALUES('Claudia Johns','Kent','467000','ogolding');''')
    curs.execute('''INSERT INTO mortgage (owner,location,value,inserted_by) VALUES('David Howard','Bristol','349000','ogolding');''')
    curs.execute('''INSERT INTO mortgage (owner,location,value,inserted_by) VALUES('Stuart Long','Kent','75000','ogolding');''')
    curs.execute('''INSERT INTO mortgage (owner,location,value,inserted_by) VALUES('Vanessa Chudleigh','Cardiff','240000','ogolding');''')            
    curs.execute('''INSERT INTO mortgage (owner,location,value,inserted_by) VALUES('Isaac Monks','London','8940000','ogolding');''')
    curs.execute('''INSERT INTO mortgage (owner,location,value,inserted_by) VALUES('Frank Brittain','Glasgow','2676000','ogolding');''')
    conn.commit()
    print("Mortgage table created successfully")

def users(conn,curs):
    curs.execute('''CREATE TABLE IF NOT EXISTS users(
            [user_id] INTEGER NOT NULL PRIMARY KEY,
            [username] VARCHAR(255) NOT NULL,
            [password] VARCHAR(255) NOT NULL,
            [admin] INTEGER NOT NULL
            )''')
    
    curs.execute('''INSERT INTO users VALUES(?,'ogolding','creator123',1);''',(753783,))
    curs.execute('''INSERT INTO users VALUES(?,'lsmith','bot_676767',0);''',(4562562,))
    conn.commit()
    print("Users table created successfully")

mortgage(curs,conn)
users(conn,curs)