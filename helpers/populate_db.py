"""Arquivo de teste de inclusão"""

import sqlite3
conn = sqlite3.connect("../jumppo.db")

import sqlite3
conn = sqlite3.connect("../jumppo.db")

# for usuario_data in usuarios:
#     insert_cmd = "INSERT INTO usuario VALUES ({usuario_data})"
#     conn.execute(insert_cmd)


saltos = [
    "1, '10', '8', '7.3', '88.2', '12.5', True, 1, 1",
    "2, '22', '22', '22.3', '22.2', '22.5', True, 1, 1"
    ]

for salto_data in saltos:
    insert_cmd = f"INSERT INTO salto VALUES ({salto_data})"
    conn.execute(insert_cmd)

conn.commit()