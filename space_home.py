import streamlit as st
from PIL import Image



def run_home() :
    
    row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
    with row0_1:
        st.title('Space Business EDA and ML Project')

    row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
    with row3_1:
        st.markdown("made by 제웅")
        st.markdown("used library : pandas, numpy, streamlit, matplotlib.pyplot, seaborn, joblib, iso3166, collections, plotly.express")
        st.markdown("[GitHub Repository](https://github.com/dogdnd/my_project)")


    st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Space_Shuttle_Columbia_launching.jpg/1024px-Space_Shuttle_Columbia_launching.jpg')
