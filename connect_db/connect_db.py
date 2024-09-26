import os
import sqlite3
import datetime

class ConnectDB():
    ''' Class that connect with the database '''
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join('.','connect_db','qr_code.db'),detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()
         
        def create_table_qr_info() -> None:
            ''' Function that creates a table in database '''
            self.cursor.execute(""" CREATE TABLE IF NOT EXISTS qr_info(
                            password TEXT PRIMARY KEY NOT NULL,
                            name_qrcode_img TEXT NOT NULL,
                            data_creation DATETIME NOT NULL)""")
        create_table_qr_info()

        def create_table_log_info() -> None:
            ''' Function that creates a table in database '''
            self.cursor.execute(""" CREATE TABLE IF NOT EXISTS log_info(
                            password TEXT NOT NULL,
                            access TEXT NOT NULL,
                            data_access DATETIME NOT NULL)""")
        create_table_log_info()
        
        def adapt_datetime_epoch(val) -> int:
            """Adapt datetime.datetime to Unix timestamp."""
            return int(val.timestamp())

        sqlite3.register_adapter(datetime.datetime, adapt_datetime_epoch)

        def convert_timestamp(val) -> datetime:
            """Convert Unix epoch timestamp to datetime.datetime object."""
            return datetime.datetime.fromtimestamp(val)

        sqlite3.register_converter("timestamp", convert_timestamp)


class ManipulateDB(ConnectDB):
    ''' Class that manilupate the tables of datasabe '''
    def insert_infos_qr_info_table(self,data:list) -> None:
        ''' Function that insert the infos in table

            Parameters:
                data (list): list of infos that will be insert in table

            Returns:
                None 
        '''
        self.cursor.execute(""" INSERT INTO qr_info (password, name_qrcode_img, data_creation) 
                            VALUES (?,?,?)""",data)
        self.conn.commit()


    def search_infos_qr_info_table(self) -> None:
        ''' Function that show all infos in table

            Returns:
                data (list) = list of tuples that contain all infos the table 
        '''
        self.cursor.execute(""" SELECT * FROM qr_info""")
        data  = self.cursor.fetchall()
        return data

    def delete_infos_qr_info_table(self,name_image:str) -> None:
        ''' Function that delete the info by name of qr code image

            Parameters:
                name_image (str): name of qr code image that the infos will be delete
            
            Returns:
                None
        '''

        self.cursor.execute(f""" DELETE FROM qr_info WHERE name_qrcode_img = "{name_image}" """)
        self.conn.commit()

    def insert_infos_log_info_table(self,data:list) -> None:
        ''' Function that insert the infos in table

            Parameters:
                data (list): list of infos that will be insert in log_info table

            Returns:
                None 
        '''
        self.cursor.execute(""" INSERT INTO log_info (password, access, data_access) 
                            VALUES (?,?,?)""",data)
        self.conn.commit()
    
    def search_infos_log_info_table(self) -> None:
        ''' Function that show all infos in table

            Returns:
                data (list) = list of tuples that contain all infos the log_info table 
        '''
        self.cursor.execute(""" SELECT * FROM log_info""")
        data  = self.cursor.fetchall()
        return data

    def close_db(self) -> None:
        ''' Function that close the connection of database

            Returns:
                None
        '''
        self.cursor.close()
        self.conn.close()
