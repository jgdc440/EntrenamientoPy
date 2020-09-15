# -*- coding: utf-8 -*-
import sqlite3
import hashlib

# Conexión a la base de datos
conn = sqlite3.connect(':memory:')

# Creo el curso
cursor = conn.cursor()

# Creo la tabla
cursor.execute("""CREATE TABLE currencies
                (ID integer primary key, name text, symbol text)""")

# Guardo los cambios
conn.commit()

cursor.execute("INSERT INTO currencies VALUES(1,'Peso (ARG)', '$')")
cursor.execute("INSERT INTO currencies VALUES(2,'Dólar', 'US$')")

# Revierto el cambio
conn.rollback()

# Consulto todas las monedas
query = "SELECT * FROM currencies"

# Busco el resultado
currency = cursor.execute(query).fetchall()

print(currency)

# Cierro la conexión a la base de datos
conn.close()

# Crear función
def md5sum(t):
    return hashlib.md5(t).hexdigest()

conn = sqlite3.connect(":memory:")
conn.create_function("md5", 1, md5sum)
cursor = conn.cursor()
cursor.execute("select md5(?)", (b"Jose G Duran",))
print(cursor.fetchone()[0])

# Cierro la conexión a la base de datos
conn.close()

class MySum:
    def __init__(self):
        self.count = 0

    def step(self, value):
        self.count += value

    def finalize(self):
        return self.count

conn = sqlite3.connect(":memory:")
conn. create_aggregate("mysum", 1, MySum)
cursor = conn.cursor()
cursor.execute("create table test(i)")
cursor.execute("insert into test(i) values (1)")
cursor.execute("insert into test(i) values (2)")
cursor.execute("select mysum(i) from test")
print(cursor.fetchone()[0])

# Cierro la conexión a la base de datos
conn.close()