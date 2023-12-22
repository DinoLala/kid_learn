import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
# from app.common.search import process_html, get_player,get_tournaments,get_norm_summary,get_norm
import streamlit as st
import time

import requests

st.set_page_config(layout="wide")
max1=int(st.sidebar.number_input('max_1',max_value=100.0,value=5.0,step=1.0 )  )
max2=int(st.sidebar.number_input('max_2',max_value=100.0,value=5.0,step=1.0 )  )

# st.header(':orange[Have fun solving puzzles with us !]')
 
col1,col2 = st.columns(2)
with col1:
    st.markdown(f"""
                <div> 
                        <h4 style="color:#7133FF;font-size:32px" >Do fun math with me!!
                        </div>""", unsafe_allow_html=True) 
with col2:
    st.image('app/data/lam.png',width=160)
st.header('')
            
import os

col1,col2 = st.columns(2)


import random
if 'counter' not in st.session_state: 
    st.session_state.counter = 0


def add_sub(max1,max2):
    # col2.image(photo,caption=photo)
    opt=random.randint(0, 1)
    r1 = random.randint(0, max1)
    r2 = random.randint(0, max1)
    if opt==0:
        with col1:
            
            st.markdown(f"""<div> 
                                <h4 style="color:#7133FF;font-size:60px" >{r1} +{r2} =?
                                </div>""", unsafe_allow_html=True) 


        r1_str="*" * (r1+r2)
        # r2_str="*" * r2

        with col2:
            st.title(f""":orange[{r1_str}] """)
            # st.markdown(f"""<div> 
            #                     <h4 style="color:#7133FF;font-size:60px" >{r1_str}  {r2_str} 
            #                     </div>""", unsafe_allow_html=True) 
    else :
        r11=max(r1,r2)
        r21=min(r1,r2)
        with col1:
            
            st.markdown(f"""<div> 
                                <h4 style="color:#7133FF;font-size:60px" >{r11} - {r21} = ?
                                </div>""", unsafe_allow_html=True) 


        r1_str="*" * (r11)
        r11_str="*" * (r11-r21)
        r21_str="x" * r21

        with col2:
            st.title(f""":orange[{r11_str}] :blue[{r21_str}] """)
            # st.markdown(f"""<div> 
            #                      <h4 style="color:#7133FF;font-size:60px" >{r11_str} {r21_str} </h4>
            #                     </div>""", unsafe_allow_html=True) 
           


    st.session_state.counter += 1
    if st.session_state.counter >= 1000:
        st.session_state.counter = 0 
    if opt==0:
        return r1+r2
    else :
        return r11-r21


     
button1 = st.button('new')
if st.session_state.get('button') != True:

    st.session_state['button'] = button1 # Saved the state
    
p = st.empty()
if st.session_state['button'] == True:
    ans =add_sub(max1,max2)

    time.sleep(2.5)

    text = f"Answer is: {ans}"
    p.write(text, end="\r")

    time.sleep(5)
    
    p.write("")

    time.sleep(2.5)
    # st.write("Your Answer is: ",  ans)
    # st.markdown(f"""<div> 
    #                     <h4 style="color:#FF5733;font-size:32px" >Answer is: {ans}
    #                     </div>""", unsafe_allow_html=True) 

    # if st.button('Check 2'):

    #     st.write("Do your logic here",ans)