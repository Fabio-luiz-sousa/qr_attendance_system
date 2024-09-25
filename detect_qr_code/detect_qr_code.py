import cv2
import numpy as np
from pyzbar.pyzbar import decode
import streamlit as st
import os
import sys
sys.path.insert(0,os.path.abspath(os.curdir))
from connect_db.connect_db import ManipulateDB

def get_password_info_qrcode_db() -> list:
    ''' Function that get all password in the table of database 

        Returns:
            authorized_users_password (list): list that contain all passwords
    '''
    authorized_users_password = list()
    manipulation = ManipulateDB()
    data = manipulation.search_infos()
    manipulation.close_db()
    for i in range(len(data)):
        authorized_users_password.append(data[i][0])
        

    return authorized_users_password



def detect_qrcode(frame_placeholder:st._DeltaGenerator,btn:bool,message:st) -> None:
    '''Function that detect a qr code by webcam

        Parameters:
            frame_palceholder (st.DeltaGenerator): streamlit object for show webcam in the webapp
            btn (bool): boolean value that indicate if btn was pressed or not in web app
            meassege (st): streamlit module for show message when the webcam was closed
            
        Returns:
           access (bool) = value that say if access is authorized
    '''
    authorized_users_password = get_password_info_qrcode_db()
    cap = cv2.VideoCapture(0)

    while True:
        teste = False
        ret,frame = cap.read()
        if not ret:
            message.write('THE VIDEO CAPTURE HAS ENDED!!')
            break
        qr_info = decode(frame)
        if len(qr_info)>0:
            data,rect,poly = qr_info[0].data,qr_info[0].rect,qr_info[0].polygon
            frame = cv2.rectangle(frame,(rect.left,rect.top),(rect.left+rect.width,rect.top+rect.height),(0,255,0),5)
            frame = cv2.polylines(frame,[np.array(poly)],True,(255,0,0),5)
            if data.decode() in authorized_users_password:
                cv2.putText(frame,'ACCESS GRANTED',(rect.left,rect.top-15),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
                access = True
                return access
                
            else:
                cv2.putText(frame,'ACCESS DENIED',(rect.left,rect.top-15),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
                access = False
                return access

        frame_placeholder.image(frame,channels='BGR')
        if cv2.waitKey(1) & 0xFF == ord('q') or btn or teste:
            break
        
    cap.release()
    cv2.destroyAllWindows()