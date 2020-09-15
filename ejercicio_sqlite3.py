# -*- coding: utf-8 -*-
import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect(':memory:')

# Creo el curso
cursor = conn.cursor()

# Creo la tabla
cursor.execute("""CREATE TABLE table_1
                (ID integer primary key, name text)""")

cursor.execute("INSERT INTO table_1 VALUES(1,'prueba')")

conn.commit()

query = "SELECT * FROM table_1"
currencies = cursor.execute(query).fetchall()

print(currencies)

conn.close()

