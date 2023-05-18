"""Ao executar este arquivo uma tabela será criada em SQLlite"""

import sqlite3


conn = sqlite3.connect("../jumppo.db")


columns = [
    "id INTEGER PRIMARY KEY",
    "parent_id INTEGER FOREIGN KEY",
    "altura_salto VARCHAR",
    "tempo_voo NUMERIC(10,2)",
    "forca_media NUMERIC(10,2)",
    "potencia_media NUMERIC(10,2)",
     "veloc_media NUMERIC(10,2)",
     "ativo BOLLEAN",

    ]
create_table_cmd = f"CREATE TABLE salto ({','.join(columns)})"
conn.execute(create_table_cmd)