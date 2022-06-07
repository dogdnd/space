import plotly.express as px
import streamlit as st
from iso3166 import countries


import matplotlib
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
from collections import OrderedDict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib


def run_ml() :
    df = pd.read_csv('data/space_mission.csv', thousands= ',')
 


    rocket = st.slider('budget', min_value=100000, max_value=10000000,step= 10000,)
    month= st.select_slider('month',options=[1,2,3,4,5,6,7,8,9,10,11,12])
    weekday=st.select_slider('weekday',options= [0,1,2,3,4,5,6])
    hour=st.slider('hour',1,24)
    

    classifier = joblib.load('data/classifier.pkl')
    scaler = joblib.load('data/scaler.pkl')
    encoder = joblib.load('data/encoder.pkl')

    print([rocket,month,weekday,hour])
    input_data = np.array([rocket,month,weekday,hour])
    input_data = input_data.reshape(1,-1)
    scaled_data = scaler.fit_transform(input_data)
    data_pred = classifier.predict(scaled_data)
    data_pred = encoder.inverse_transform(data_pred)

    st.write('this space mission is expected {}'.format(data_pred))




