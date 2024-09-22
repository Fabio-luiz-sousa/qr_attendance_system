import os
import sys
sys.path.insert(0,os.path.abspath(os.curdir))

import streamlit as st
from detect_qr_code.detect_qr_code import detect_qrcode

st.set_page_config(
    page_title = 'QR ATTENDANCE SYSTEM',
)
st.title('Welcome, check your access!')

frame_placeholder = st.empty()
stop_btn_pressed = st.button('Stop')
messsage = st

detect_qrcode(frame_placeholder,stop_btn_pressed,messsage)

