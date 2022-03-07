import sqlite3

# # Connect to database
# # conn = sqlite3.connect(':memory:')
# conn = sqlite3.connect('customer.db')

# # Create a cursor
# c = conn.cursor()

# # Create a Table
# c.execute("""CREATE TABLE customers (
#     ID INT PRIMARY KEY NOT NULL,
#     Name TEXT NOT NULL,
#     Age INT)""")

# c.execute("INSERT INTO customers VALUES(1, 'Abhishek', 28)")
# c.execute("INSERT INTO customers VALUES(2, 'Nithin', 27)")
# c.execute("INSERT INTO customers VALUES(4, 'Amit', 21)")
# print("Command executed successfully")


# # Commit the copmmand
# conn.commit()

# # # Close our Connection
# conn.close()

# # Many execution
# many_customers = [
#     (1, 'abc', 23),
#     (2,'pqr', 38),
#     (3, 'lmn', 44)
# ]

# c.execute("INSERT INTO customers VALUES (?,?,?)", many_customers)

# # Query the database
# c.execute("SELECT * FROM customers")
# #c.fetchone()
# #c.fetchmany(3)
# print(c.fetchall())

import pandas as pd
df = pd.read_csv('student_marks.csv')
print(df.head())
conn = sqlite3.connect('student.db')
df.to_sql('student_marks', conn, if_exists='replace', index=False)
print('successful')