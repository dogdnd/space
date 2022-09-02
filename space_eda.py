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


def run_eda() :
    st.subheader('Space Mission EDA')
    df = pd.read_csv('data/space_mission.csv', thousands= ',')
    
    countries_dict = {
        'Russia' : 'Russian Federation',
        'New Mexico' : 'USA',
        "Yellow Sea": 'China',
        "Shahrud Missile Test Site": "Iran",
        "Pacific Missile Range Facility": 'USA',
        "Barents Sea": 'Russian Federation',
        "Gran Canaria": 'USA'
    }

    df['country'] = df['Location'].str.split(', ').str[-1].replace(countries_dict)

    sun = df.groupby(['country', 'Company Name', 'Status Mission'])['Datum'].count().reset_index()

    sun.columns = [
        'country', 
        'company', 
        'status', 
        'count'
    ]
    
    st.info('알고싶은 우주사업 관련 국가,기관을 클릭하면 하위항목으로 펼쳐집니다.')
    fig = px.sunburst(
        sun, 
        path=[
            'country', 
            'company', 
            'status'
        ], 
        values='count', 
        
        width=600,
        height=600
    )

    st.plotly_chart(fig)


    country_dict = dict()
    for c in countries:
        country_dict[c.name] = c.alpha3
        
    df['alpha3'] = df['country']
    df = df.replace(
        {
            "alpha3": country_dict
        }
    )
    df.loc[df['country'] == "North Korea", 'alpha3'] = "PRK"
    df.loc[df['country'] == "South Korea", 'alpha3'] = "KOR"

    def plot_map(dataframe, target_column, title, width=800, height=600):
        mapdf = dataframe.groupby(['country', 'alpha3'])[target_column].count().reset_index()
        fig = px.choropleth(
            mapdf, 
            locations="alpha3", 
            hover_name="country", 
            color=target_column, 
            projection="natural earth", 
            width=width, 
            height=height, 
            title=title
        )
        st.plotly_chart(fig)

    plot_map(
        dataframe=df, 
        target_column='Status Mission', 
        title='국가별 발사횟수를 색상으로 나타낸 맵'
    )

    fail_df = df[df['Status Mission'] == 'Failure']
    plot_map(fail_df, 'Status Mission', '국가별 실패횟수를 색상으로 나타낸 맵')

    data = df.groupby(['Company Name'])['Rocket'].sum().reset_index()
    data = data[data['Rocket'] > 0]

    data.columns = [
        'company', 
        'money'
    ]

  

    df['date'] = pd.to_datetime(df['Datum'])
    df['year'] = df['date'].apply(lambda datetime: datetime.year)
    df['month'] = df['date'].apply(lambda datetime: datetime.month)
    df['hour'] = df['date'].apply(lambda datetime: datetime.hour)
    df['weekday'] = df['date'].apply(lambda datetime: datetime.weekday())

    money = df.groupby(['Company Name'])['Rocket'].sum()
    starts = df['Company Name'].value_counts().reset_index()

    starts.columns = [
        'Company Name', 
        'count'
    ]

    av_money_df = pd.merge(money, starts, on='Company Name')
    av_money_df['avg'] = av_money_df['Rocket'] / av_money_df['count']
    av_money_df = av_money_df[av_money_df['avg']>0]
    av_money_df = av_money_df.reset_index()

    

    money = df[df['Rocket']>0]
    money = money.groupby(['year'])['Rocket'].mean().reset_index()



    ds = df.groupby(['Company Name'])['year'].nunique().reset_index()


    data = df.groupby(['Company Name', 'year'])['Status Mission'].count().reset_index()

    data.columns = [
        'company', 
        'year', 
        'starts'
    ]

    top5 = data.groupby(['company'])['starts'].sum().reset_index().sort_values('starts', ascending=False).head(5)['company'].tolist()
    data = data[data['company'].isin(top5)]

    fig = px.line(
        data, 
        x="year", 
        y="starts", 
        title='TOP 5 우주사업 기관들의 발사기록', 
        color='company'
    )

    st.plotly_chart(fig)


    
    ds = df.groupby(['year', 'country'])['Status Mission'].count().reset_index().sort_values(['year', 'Status Mission'], ascending=False)
    ds = pd.concat([group[1].head(1) for group in ds.groupby(['year'])])
    ds.columns = ['year', 'country', 'launches']

    fig = px.bar(
        ds, 
        x="year", 
        y="launches", 
        color='country', 
        title='년도별 최다 로켓발사(국가)'
    )

    st.plotly_chart(fig)


    ds = df.groupby(['year', 'Company Name'])['Status Mission'].count().reset_index().sort_values(['year', 'Status Mission'], ascending=False)
    ds = pd.concat([group[1].head(1) for group in ds.groupby(['year'])])
    ds.columns = ['year', 'company', 'launches']

    fig = px.bar(
        ds, 
        x="year", 
        y="launches", 
        color='company', 
        title='년도별 최다 로켓발사(기관)',
        width=800
    )

    st.plotly_chart(fig)


    st.info('기관별 발사현황 조회')

    choice_company= st.selectbox('기관 선택', df['Company Name'].unique())

    data = df[df['Company Name'] == choice_company]
    data = data.groupby(['year'])['Company Name'].count().reset_index()
    data = data[data['year'] < 2020]

    data.columns = [
        'year', 
        'launches'
    ]

    fig = px.line(
        data, 
        x="year", 
        y="launches", 
        title='{}의 년도별 발사현황'.format(choice_company)
    )

    st.plotly_chart(fig)



    st.info('시간대별 발사현황 확인')


    time_menu = ['month','hour','weekday']
    time_choice = st.selectbox('시간대 선택', time_menu)
    
    

    if time_choice == time_menu[0] :
        ds = df['month'].value_counts().reset_index()

        ds.columns = [
            'month', 
            'count'
        ]

        fig = px.bar(
            ds, 
            x='month',
            y="count", 
            orientation='v', 
            title='월별 발사현황 체크', 
            width=800
        )

        st.plotly_chart(fig)

    if time_choice == time_menu[1] :
        ds = df['hour'].value_counts().reset_index()

        ds.columns = [
            'hour', 
            'count'
        ]

        fig = px.bar(
            ds, 
            x='hour', 
            y="count", 
            orientation='v',
            title='시간별 발사현황 체크', 
            width=800
        )

        st.plotly_chart(fig)

    if time_choice == time_menu[2] :
        ds = df['weekday'].value_counts().reset_index()

        ds.columns = [
            'weekday', 
            'count'
        ]

        fig = px.bar(
            ds, 
            x='weekday', 
            y="count", 
            orientation='v',
            title='요일별 발사현황 체크', 
            width=800
        )

        st.plotly_chart(fig)




    st.info('최근 10년간 우주사업 기관별 발사 현황')
    choice_year = st.slider('select year',min_value=2010, max_value=2020)
    data = df.groupby(['Company Name', 'year'])['Status Mission'].count().reset_index()

    data.columns = [
        'company', 
        'year', 
        'starts'
    ]

    data = data[data['year']==choice_year]

    
    fig = px.bar(
        data, 
        x="company", 
        y="starts", 
        title='발사 현황', 
        width=800
    )

    st.plotly_chart(fig)



    st.info('냉전시기 미국과 소련의 우주전쟁')
    if st.checkbox('그래프 보기') :

        cold = df[df['year'] <= 1991]
        cold['country'].unique()
        cold.loc[cold['country'] == 'Kazakhstan', 'country'] = 'USSR'
        cold.loc[cold['country'] == 'Russian Federation', 'country'] = 'USSR'
        cold = cold[(cold['country'] == 'USSR') | (cold['country'] == 'USA')]

        
        
        
        
        ds = cold['country'].value_counts().reset_index()

        ds.columns = [
            'contry', 
            'count'
        ]

        fig = px.pie(
            ds, 
            names='contry', 
            values="count", 
            title='USA vs USSR 총 발사 현황', 
            width=500
        )

        st.plotly_chart(fig)

        ds = cold.groupby(['year', 'country'])['alpha3'].count().reset_index()
        ds.columns = ['year', 'country', 'launches']

        fig = px.bar(
            ds, 
            x="year", 
            y="launches", 
            color='country', 
            title='USA vs USSR 년도별 발사현황',
            width=800
        )
        st.plotly_chart(fig)


        ds = cold[cold['Status Mission'] == 'Failure']
        ds = ds.groupby(['year', 'country'])['alpha3'].count().reset_index()
        ds.columns = ['year', 'country', 'failures']

        fig = px.bar(
            ds, 
            x="year", 
            y="failures", 
            color='country', 
            title='USA vs USSR 년도별 실패현황', 
            width=800
        )

        st.plotly_chart(fig)

        

        ds = cold.groupby(['year', 'country'])['Company Name'].nunique().reset_index()
        ds.columns = ['year', 'country', 'companies']

        fig = px.bar(
            ds, 
            x="year", 
            y="companies", 
            color='country', 
            title='USA vs USSR 년도별 민간우주기관 보유현황',
            width=800
        )

        st.plotly_chart(fig)

       

  
        