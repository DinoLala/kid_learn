import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

fruit_list=['apple','strawberry','banana','pineapple','pumkin','grape']

animal_list=['dog','cat','cow','flamingo','unicorn','pig','elephant','lion','giraffe','squirrel']

color_dict={'apple':'red'
            ,'strawberry':'red'
             ,'banana':'yellow'
              ,'pineapple':'yellow'
               ,'pumkin':'orange'
                ,'grape':'purple'

            
            }

taste_dict={'apple':'sweet'
            ,'strawberry':'sweet'
             ,'banana':'healthy'
              ,'pineapple':'healthy'
               ,'pumkin':'healthy'
                ,'grape':'sweet'

            
            }

eat_dict={'dog':['eats','bone'],
          'cat':['drinks','milk']
          ,'cow':['eats','grass']
          ,'flamingo':['eats','small fish']
          ,'unicorn':['likes','ice cream']
          ,'pig':['likes','tomato']
          ,'elephant':['likes','banana']
          ,'lion':['eats','meat']
          ,'giraffe':['eats','leaf']
          ,'squirrel':['eats','nuts']
          ,'bear':['likes','honney']
 
            }



def get_sentence(st,col1,col2,photo):
    # col1, col2= st.columns(2)
    
    word=photo.split('/')[-1].split('.')[0]
    if word in fruit_list:
        col2.image(photo,caption=photo)
        color=color_dict[word]
        taste=taste_dict[word]

        with col1:
            st.markdown(f"""<div> 
                                <h4 style="color:#FF6833;font-size:32px" > What is this?
                                </div>""", unsafe_allow_html=True) 
            time.sleep(2)
            st.markdown(f"""<div> 
                                <h4 style="color:#7133FF;font-size:32px" >This is a {color} {word}
                                </div>""", unsafe_allow_html=True) 

            time.sleep(2)
            st.markdown(f"""<div> 
                                <h4 style="color:#55FF33;font-size:32px" >{word} is {taste}
                                </div>""", unsafe_allow_html=True) 
            time.sleep(2)
            st.markdown(f"""<div> 
                                <h4 style="color:#FF33E6;font-size:32px" > I like {word}. Yummy!.
                                </div>""", unsafe_allow_html=True) 


    elif word in animal_list:
        col2.image(photo,caption=photo)
        # eat_dict[word]
        with col1:
            st.markdown(f"""<div> 
                                <h4 style="color:#FF6833;font-size:32px" > What is this?
                                </div>""", unsafe_allow_html=True) 
            time.sleep(2)
            st.markdown(f"""<div> 
                                <h4 style="color:#7133FF;font-size:32px" >This is a {word}
                                </div>""", unsafe_allow_html=True) 

            time.sleep(2)
            st.markdown(f"""<div> 
                                <h4 style="color:#FF6833;font-size:32px" > {word} {eat_dict[word][0]} {eat_dict[word][1]}.
                                </div>""", unsafe_allow_html=True) 

    # return 

