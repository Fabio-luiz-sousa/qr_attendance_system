import os
import sys
sys.path.insert(0,os.path.abspath(os.curdir))

import streamlit as st
from detect_qr_code.detect_qr_code import detect_qrcode
from connect_db.connect_db import ManipulateDB
import pandas as pd

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

check_access()

def option_search():
    btn = st.button('search all data')
    if btn:
        manipulate = ManipulateDB()
        data = manipulate.search_infos()
        manipulate.close_db()
        df = pd.DataFrame(data,columns=['password','name_arcode_img','date_creation'])
        df['date_creation'] = pd.to_datetime(df['date_creation'],unit='s')
        st.dataframe(df)

def settings():
    '''Function that configure the tab after the authorized access'''
    manipulate = ManipulateDB()
    st.markdown("Choice one option!")
    st.tabs(['Settings'])
    options = st.radio('Options',['Search','Insert','Delete','Log'])
    match options:
        case 'Search':
            option_search()
        case 'Insert':
            ...
        case 'Delete':
            ...
        case 'Log':
            ...

    
if st.session_state['verification_done'] and st.session_state['access_granted']:
    st.success('Credentials Accepted!!')
    settings()
else:
    st.error('Invalid Credentials!!!')







