import sqlite3

db= sqlite3.connect('/Users/kat/OneDrive - Solent University/database assignment/part_1.db')

cursor= db.cursor()

shopper_id = input("Please enter your shopper ID number: \n")
sql_query= "SELECT shopper_id\
             FROM shoppers\
             WHERE shopper_id=?"
cursor.execute(sql_query, (shopper_id,))
shopper_id_row = cursor.fetchone()
if shopper_id_row:
    shopper_id_id = shopper_id_row[0]
    print("Customer {0} has logged on".format(shopper_id))
else:
    print("No customer found with that id")
db.close()
