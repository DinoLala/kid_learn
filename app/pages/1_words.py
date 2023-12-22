import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
# from app.common.search import process_html, get_player,get_tournaments,get_norm_summary,get_norm
import streamlit as st


import requests

st.set_page_config(layout="wide")

# st.header(':orange[Have fun solving puzzles with us !]')
 
col1,col2 = st.columns(2)
with col1:
    st.markdown(f"""<div> 
                        <h4 style="color:#7133FF;font-size:32px" >Read and Write with me!!
                        </div>""", unsafe_allow_html=True) 
with col2:
    st.image('app/data/lam.png',width=160)
st.header('')
            
import os

col1,col2 = st.columns(2)



if 'counter' not in st.session_state: 
    st.session_state.counter = 0
def showPhoto(photo):
    # col2.image(photo,caption=photo)
    with col2:
        st.image(photo)
        st.write('image source: google image')

    # col1.write(f"Index as a session_state attribute: {st.session_state.counter}")
    word=photo.split('/')[-1].split('.')[0]
    # col1.title(f':orange[{word}]')
    with col1:
        st.markdown(f"""<div> 
                    <h4 style="color:#FF5733;font-size:100px" >{word} 
                    </div>""", unsafe_allow_html=True)
    # if 'ww' in photo:
    #     col1.subheader(f"White to move and win")
    # elif "wd" in photo:
    #     col1.subheader(f"White to move and draw")

    
    ## Increments the counter to get next photo
    st.session_state.counter += 1
    if st.session_state.counter >= len(pathsImages):
        st.session_state.counter = 0

# Get list of images in folder
# folderWithImages = r"images"
folderWithImages = r"app/data/puzzles"
folderWithImages = r"app/data/words"
pathsImages = [os.path.join(folderWithImages,f) for f in os.listdir(folderWithImages)]

# col1.subheader("List of images in folder")

# col1.write(pathsImages)

# Select photo a send it to button
photo = pathsImages[st.session_state.counter]
show_btn = col1.button("Next Word ⏭️",on_click=showPhoto,args=([photo]))
