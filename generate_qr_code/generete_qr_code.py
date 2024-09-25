import qrcode
import random
import string
import datetime

import os
import sys
sys.path.insert(0,os.path.abspath(os.curdir))
from connect_db.connect_db import ManipulateDB

def create_password() -> str:
    ''' Function that create a random password for qr code 

        Returns:
            password (str): return the password created
    '''
    characters = string.digits+string.ascii_letters+string.ascii_lowercase+string.punctuation
    password = ''.join(random.choices(characters,k=15))
    return password

def qrcode_create(password:str,name_image:str) -> None:
    ''' Function that create the image of qr code

        Parameters:
            password (str): password created in the function create_password
            name_imag (str): name of qr code image
        
        Returns:
            None

    '''
    qr = qrcode.make(password)
    qr.save(f'./qr_code_imgs/{name_image}.png')

def insert_qr_code_infos_db(password:str,type_qrcode:str,name_image:str) -> None:
    ''' Function that insert qr code infos in the table of database

        Returns:
            None
    '''
    manipulation = ManipulateDB()
    manipulation.insert_infos(data=[password,type_qrcode,name_image,datetime.datetime.now()])
    manipulation.close_db()

password = create_password()
qrcode_create(password,'user')
insert_qr_code_infos_db(password,'user','user')
