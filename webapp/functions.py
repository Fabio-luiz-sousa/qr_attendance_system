import os
import sys
sys.path.insert(0,os.path.abspath(os.curdir))

import streamlit as st
from detect_qr_code.detect_qr_code import detect_qrcode
from generate_qr_code.generete_qr_code import *
from connect_db.connect_db import ManipulateDB
import pandas as pd


def home():
    '''Function that create a home messages'''
    st.set_page_config(
    page_title = 'QR ATTENDANCE SYSTEM',
    )
    st.title('Welcome, check your access!')

def check_access():
    '''Function that check access'''
    if 'verification_done' not in st.session_state:
        st.session_state['verification_done'] = False
    if 'access_granted' not in st.session_state:
        st.session_state['access_granted'] = None
    frame_placeholder = st.empty()
    message = st
    if not st.session_state['verification_done']:
        access = detect_qrcode(frame_placeholder, message)
        st.session_state['access_granted'] = access
        st.session_state['verification_done'] = True

def option_search():
    '''Function that create a option search in tab settings'''
    btn = st.button('search all data')
    if btn:
        manipulate = ManipulateDB()
        data = manipulate.search_infos_qr_info_table()
        manipulate.close_db()
        df = pd.DataFrame(data,columns=['password','name_arcode_img','date_creation'])
        df['date_creation'] = pd.to_datetime(df['date_creation'],unit='s')
        st.dataframe(df)

def option_insert():
    '''Function that create a option insert in tab settings'''
    name_img = st.text_input(label='write a name o qr_code image')
    if len(name_img) > 0:
        password = create_password()
        qrcode_create(password,name_img)
        insert_qr_code_infos_db(password,name_img)
        st.success('data Inserted!')

def option_delete():
    '''Function that create a option delete in tab settings'''
    name_img = st.text_input(label='write a name o qr_code image for delete')
    if len(name_img) > 0:
        st.error('Are you sure ?')
        btn_yes = st.button('Yes')
        btn_no = st.button('No')
        if btn_yes:
            manipulate = ManipulateDB()
            manipulate.delete_infos_qr_info_table(name_img)
            manipulate.close_db()
            st.success('Successful deletion')
        elif btn_no:
            st.success('Exclusion denied')

def option_log():
    '''Function that create a option log in tab settings'''
    btn = st.button('search all log data')
    if btn:
        manipulate = ManipulateDB()
        data = manipulate.search_infos_log_info_table()
        manipulate.close_db()
        df = pd.DataFrame(data,columns=['password','access','date_access'])
        df['date_access'] = pd.to_datetime(df['date_access'],unit='s')
        st.dataframe(df)
    

