import os
import sys
sys.path.insert(0,os.path.abspath(os.curdir))

import streamlit as st
from detect_qr_code.detect_qr_code import detect_qrcode

st.set_page_config(
    page_title = 'QR ATTENDANCE SYSTEM',
)
st.title('Welcome, check your access!')

def check_access():

    frame_placeholder = st.empty()
    stop_btn_pressed = st.button('Stop')
    messsage = st
    access = detect_qrcode(frame_placeholder,stop_btn_pressed,messsage)
    return access
  
access = check_access()

def settings():
    st.markdown("Make your changes!!")

tab_option = ['Settings']
if access:
    tab = st.tabs(tab_option)
    settings()
else:
    st.error('Invalid Credentials!!!')





