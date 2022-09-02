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

    st.subheader('ML을 활용한 우주사업 예측모델')

    
    df = pd.read_csv('data/space_mission.csv', thousands= ',')
 

    st.info('우주사업 예산을 선택하세요')
    rocket = st.slider('단위 $1M(=million)', min_value=100, max_value=10000,step= 100,)
    st.info('발사시기를 선택하세요')
    month= st.select_slider('월',options=[1,2,3,4,5,6,7,8,9,10,11,12])

    weekday=st.select_slider('요일',options= [0,1,2,3,4,5,6])

    hour=st.slider('시간',1,24)
    

    classifier = joblib.load('data/classifier.pkl')
    scaler = joblib.load('data/scaler.pkl')
    encoder = joblib.load('data/encoder.pkl')

    print([rocket,month,weekday,hour])
    input_data = np.array([rocket,month,weekday,hour])
    input_data = input_data.reshape(1,-1)
    scaled_data = scaler.fit_transform(input_data)
    data_pred = classifier.predict(scaled_data)
    data_pred = encoder.inverse_transform(data_pred)

    st.info('해당 조건에 따른 예측결과 확인')
    if st.button('예측결과 확인') :
        st.write('이 조건에 해당하는 우주사업은 {}으로 예측됩니다.'.format(data_pred))




