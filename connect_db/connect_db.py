import os
import sqlite3
import datetime

class ConnectDB():
    ''' Class that connect with the database '''
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join('.','connect_db','qr_code.db'),detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
         
        def create_table() -> None:
            ''' Function that creates a table in database '''
            self.cursor.execute(""" CREATE TABLE IF NOT EXISTS qr_info(
                            password TEXT PRIMARY KEY NOT NULL,
                            type_qrcode TEXT NOT NULL,
                            name_qrcode_img TEXT NOT NULL,
                            data_creation DATETIME NOT NULL)""")
        create_table()
        
        def adapt_datetime_epoch(val) -> int:
            """Adapt datetime.datetime to Unix timestamp."""
            return int(val.timestamp())

        sqlite3.register_adapter(datetime.datetime, adapt_datetime_epoch)

        def convert_timestamp(val) -> datetime:
            """Convert Unix epoch timestamp to datetime.datetime object."""
            return datetime.datetime.fromtimestamp(val)

        sqlite3.register_converter("timestamp", convert_timestamp)


class ManipulateDB(ConnectDB):
    ''' Class that manilupate the table of datasabe '''
    def insert_infos(self,data:list) -> None:
        ''' Function that insert the infos in table

            Parameters:
                data (list): list of infos that will be insert in table

            Returns:
                None 
        '''
        self.cursor.execute(""" INSERT INTO qr_info (password, type_qrcode, name_qrcode_img, data_creation) 
                            VALUES (?,?,?,?)""",data)
        self.conn.commit()


    def search_infos(self) -> None:
        ''' Function that show all infos in table

            Returns:
                data (list) = list of tuples that contain all infos the table 
        '''
        self.cursor.execute(""" SELECT * FROM qr_info """)
        data  = self.cursor.fetchall()
        return data

    def delete_infos(self,name_image:str) -> None:
        ''' Function that delete the info by name of qr code image

            Parameters:
                name_image (str): name of qr code image that the infos will be delete
            
            Returns:
                None
        '''

        self.cursor.execute(f""" DELETE FROM qr_info WHERE name_qrcode_img = "{name_image}" """)
        op = input('Confirm deletion? yes/no: ')
        if op.lower() == "yes":
            self.conn.commit()
            print('Deletion made!!')
        else:
            print('Deletion refused!!')

    def close_db(self) -> None:
        ''' Function that close the connection of database

            Returns:
                None
        '''
        self.cursor.close()
        self.conn.close()
