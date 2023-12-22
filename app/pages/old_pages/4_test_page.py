import pkgutil
from importlib import import_module
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from app.common.search import process_html, get_player,get_tournaments,get_norm_summary
import streamlit as st

import requests


st.set_page_config(layout="wide")

st.sidebar.header(':orange[USCF Norms sytem:]' )
st.sidebar.write('* Rating 2400: Life Senior Master (S)' )
st.sidebar.write('* Rating 2200: Life Master (M) ' )
st.sidebar.write('* Rating 2000 Candidate Master (C) ' )
st.sidebar.write('* Rating 1800: 1st Category (1)' )
st.sidebar.write('* Rating 1600: 2nd Category (2)' )
st.sidebar.write('* Rating 1400: 3rd Category (3)' )
st.sidebar.write('* Rating 1200: 4th Category (4)' )




st.write("# This works:")

h=process_html()

uscf_id=''
col10, col20= st.columns(2)
# favorite players ----
with col10:
    

    st.image("app/data/chess.png")
    # st.image("app/data/chess2.png")
    if "favorite_player" not in st.session_state:
        st.session_state["favorite_player"] = False

    if "show more" not in st.session_state:
        st.session_state["show more"] = False
    if "button3" not in st.session_state:
        st.session_state["button3"] = False

    if st.button("favorite_player"):
        
        st.session_state["favorite_player"] = not st.session_state["favorite_player"]

    if st.session_state["favorite_player"]:
        
        import json
        
        # save to file
        # with open("app/data/common_players.json", "w") as fp:
        #     json.dump(df_common_players , fp) 
        json_file_path = 'app/data/common_players.json'

        with open(json_file_path, 'r') as j:
            df_common_players = json.loads(j.read())
        
        for idx, row in df_common_players.items():
            constrained_height = 5
            with st.container():
                col1, col2,col3 = st.columns(3)
                col1.write(str(idx))
                col2.write(str(row))
                
                placeholder = col3.empty()
                show_more   = placeholder.button("show more", key=idx, type="primary")

                # if button pressed
                if show_more:

                    # rename button
                    # placeholder.button("less", key=str(idx)+"_")
                    
                    # do stuff
                    uscf_id=row
                    st.write("more info about player",uscf_id)
                    st.header(":orange[Player Summary !]")

                    with st.container():
                        # st.write("This is inside the container")
                        col1, col2, col3 = st.columns(3)
                        

                        dict_out=get_player(h,uscf_id)
                        with col1:
                            #    st.header("A cat")
                            st.write(dict_out['Name'])
                            # st.write('Gender:',dict_out['Gender'])
                            st.write('State:',dict_out['State'])
                            # if "none" not in dict_out['title_name']:
                            st.write('Current Title:',dict_out['title_name'])

                        with col2:
                            #    st.header("A dog")
                            # st.write('State:',dict_out['State'])
                            
                            st.write('Current USCF Rating:', dict_out['current_rating'])
                            st.write('Next month USCF Rating:', dict_out['nextmonth_rate'])
                        with col3:
                            #    st.header("An owl")
                            st.write('Overall Ranking:', dict_out['Over_Ranking'])
                            st.write('State Ranking:', dict_out['State_Ranking'])
                            st.write('Junior Ranking:', dict_out['Junior_Ranking'])


                    norm_df=get_norm_summary(h,uscf_id)
                    st.write(':orange[Lastest Norm:]')
                    if len(norm_df)==0:
                        st.write('This player has no norm yet!')
                    else:
                        norm_df=norm_df.sort_values(by=['level'])
                        norm_df.columns=['Norm','Norm count']
                        st.dataframe(norm_df.tail(1))
                    # st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
                    st.divider() 

                

                    
                


                    with col20:
                        html_tables=get_tournaments(h,uscf_id)
                        st.write(html_tables)
                        # st.dataframe(html_tables[['End_event_date','Event_name','reg Rtg Before/After']], width=1600, height=600)
                        
                    # st.write()
                    st.divider() 
        

    

        # if st.button("show more"):
        #     st.session_state["show more"] = not st.session_state["show more"]
    
    # if st.session_state["favorite_player"] and st.session_state["show more"]:
    #     if st.button("Button3"):
    #         st.session_state["button3"] = not st.session_state["button3"]
    # if st.session_state["show more"]:
    #     st.write("**Button2!!!**")
    # # common_players=st.button('Favorite Players')
    uscf_id=st.text_input('USCF_ID' ,value=uscf_id)

    
with col20:
    st.title(":orange[Happy player!!!]")
    st.title("")

    # st.title(":orange[This is for my beloved son. Have Funs !!!]")
    # col11, col21,col23 = st.columns(3)
    # with col21 :
    #     st.image("app/data/happy-dance-excited.gif")
    

h=process_html()

submited=st.button('Find player')
url = "https://new.uschess.org/players/search"
# st.write("check out this [link](%s)" % url)
st.write(":orange[Visit [website ](%s) for official player rating look up]" % url)

if submited and uscf_id !="":
# if submited :
    # st.write('uscf id ',uscf_id)

    st.divider() 
    st.header(":orange[Player Summary !]")

    with st.container():
        # st.write("This is inside the container")
        col1, col2, col3 = st.columns(3)
        

        dict_out=get_player(h,uscf_id)
        with col1:
            #    st.header("A cat")
            st.write(dict_out['Name'])
            # st.write('Gender:',dict_out['Gender'])
            st.write('State:',dict_out['State'])
            # if "none" not in dict_out['title_name']:
            st.write('Current Title:',dict_out['title_name'])

            
            
            
            #    st.image("https://static.streamlit.io/examples/cat.jpg")

        with col2:
            #    st.header("A dog")
            # st.write('State:',dict_out['State'])
            
            st.write('Current USCF Rating:', dict_out['current_rating'])
            st.write('Next month USCF Rating:', dict_out['nextmonth_rate'])
            
            #    st.image("https://static.streamlit.io/examples/dog.jpg")

        with col3:
            #    st.header("An owl")
            st.write('Overall Ranking:', dict_out['Over_Ranking'])
            st.write('State Ranking:', dict_out['State_Ranking'])
            st.write('Junior Ranking:', dict_out['Junior_Ranking'])


    norm_df=get_norm_summary(h,uscf_id)
    st.write(':orange[Lastest Norm:]')
    if len(norm_df)==0:
        st.write('This player has no norm yet!')
    else:
        norm_df=norm_df.sort_values(by=['level'])
        norm_df.columns=['Norm','Norm count']
        st.dataframe(norm_df.tail(1))
    # st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    st.divider() 

    st.header(":orange[Lastest Tournaments!]")
 

    html_tables=get_tournaments(h,uscf_id)
    # st.dataframe(html_tables[['End_event_date','Event_name','reg Rtg Before/After']], width=1600, height=600)
    st.dataframe(html_tables, width=1600, height=600)
    try:
        html_tables=html_tables.sort_values(by='End_event_date', ascending=True)
        html_tables['rating']=html_tables['reg Rtg Before/After'].apply(lambda x: x.split('=>')[-1].split('(')[0] if "ONL" not in x else '')
        df_temp=html_tables[['rating','End_event_date']].copy()
        df_temp=df_temp.loc[(df_temp['rating']!=' ') ]
        df_temp=df_temp.loc[(df_temp['rating']!='') ]
        # st.write(df_temp)
        df_temp['rating']=df_temp['rating'].astype('int')
        df_temp.index=df_temp['End_event_date']
    except:
        pass
  


    with col20:

        # How to set the graph size 
        
        try:
            two_subplot_fig = plt.figure(figsize=(6,6),facecolor='lightblue')
            plt.subplot(211)
            plt.plot(df_temp['End_event_date'] ,df_temp['rating'] , color='tab:blue', marker='.')
            plt.xticks(rotation=30)
            x_stick=[df_temp['End_event_date'][i] for i  in range(len(df_temp['End_event_date'])) if i%5 == 0 ]
            plt.xticks(x_stick)
            plt.grid()
            plt.title('Rating trend')
            st.pyplot(two_subplot_fig)


            # st.line_chart(df_temp['rating']    )
            # st.altair_chart(l_rate    )
        except:
            pass


