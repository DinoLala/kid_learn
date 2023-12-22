import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd


import streamlit as st


# st.subheader('For more information, please visit US Chess official website')

# st.header(':orange[Having Fun learning with pricess LAM!!]')
st.markdown(f"""<div> 
                    <h4 style="color:#FF5733;font-size:48px" >Having Fun learning with pricess LAM!!
                    </div>""", unsafe_allow_html=True)   
# with col2:
#     st.image('./app/data/nhan.jpeg')

# url = "https://new.uschess.org/"
# # st.write("check out this [link](%s)" % url)
# st.write(":orange[For more information, please visit US Chess official [website ](%s)]" % url)

# maca_tournament = "http://www.masschess.org/Events/chess-event-calendar.aspx"
# st.write(":orange[For MACA [Tournaments ](%s)]" % maca_tournament)