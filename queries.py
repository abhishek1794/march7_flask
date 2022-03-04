import sqlite3

def get_by_Name(Name):
    conn = sqlite3.connect('customer.db')
    cur = conn.cursor()
    statement = "SELECT * FROM customers WHERE Name = ?"
    cur.execute(statement, [Name])
    return cur.fetchone()