import os
import sqlite3
import datetime

# classe que conecta no banco de dados
class ConectaDB():
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join('.','connect_db','qr_code.db'),detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()

        def create_table() -> None:
            self.cursor.execute(""" CREATE TABLE IF NOT EXISTS qr_info(
                            password TEXT PRIMARY KEY NOT NULL,
                            tipo_qrcode TEXT NOT NULL,
                            nome_qrcode_img TEXT NOT NULL,
                            data_criacao DATETIME NOT NULL)""")
        create_table()
        
        def adapt_datetime_epoch(val):
            """Adapt datetime.datetime to Unix timestamp."""
            return int(val.timestamp())

        sqlite3.register_adapter(datetime.datetime, adapt_datetime_epoch)

        def convert_timestamp(val):
            """Convert Unix epoch timestamp to datetime.datetime object."""
            return datetime.datetime.fromtimestamp(val)

        sqlite3.register_converter("timestamp", convert_timestamp)

# classe que manipula a tabela no banco de dados
class ManilupaDB(ConectaDB):
    def inserir_infos(self,data:list) -> None:
        self.cursor.execute(""" INSERT INTO qr_info (password, tipo_qrcode, nome_qrcode_img, data_criacao) 
                            VALUES (?,?,?,?)""",data)
        self.conn.commit()
    def consultar_infos(self):
        self.cursor.execute(""" SELECT * FROM qr_info """)
        data  = self.cursor.fetchall()
        print(data)
    def fecha_db(self):
        self.cursor.close()
        self.conn.close()
