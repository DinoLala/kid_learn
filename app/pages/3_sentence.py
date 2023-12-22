import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
# from app.common.search import process_html, get_player,get_tournaments,get_norm_summary,get_norm
from app.common.read import get_sentence
import streamlit as st
import time

import requests

st.set_page_config(layout="wide")

 
col1,col2 = st.columns(2)
with col1:
    st.markdown(f"""<div> 
                        <h4 style="color:#7133FF;font-size:32px" >Read with me!!
                        </div>""", unsafe_allow_html=True) 
with col2:
    st.image('app/data/lam.png',width=160)
st.header('')
            
import os

col1,col2 = st.columns(2)

p = st.empty()
import random
if 'counter' not in st.session_state: 
    st.session_state.counter = 0


def sentence(photo):
    # col2.image(photo,caption=photo)
    # word=photo.split('/')[-1].split('.')[0]
    if st.session_state.counter %2 ==0:
        get_sentence(st,col1,col2,photo)

    
    st.session_state.counter += 1
    if st.session_state.counter >= len(pathsImages):
        st.session_state.counter = 0 
 
# Get list of images in folder
# folderWithImages = r"images"
folderWithImages = r"app/data/sentence"
pathsImages = [os.path.join(folderWithImages,f) for f in os.listdir(folderWithImages)]
random.shuffle(pathsImages)
# col1.subheader("List of images in folder")

# col1.write(pathsImages)

# Select photo a send it to button
photo = pathsImages[st.session_state.counter]

button1 = col1.button("Next ⏭️",on_click=sentence,args=([photo]))


