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
    
    fig = px.sunburst(
        sun, 
        path=[
            'country', 
            'company', 
            'status'
        ], 
        values='count', 
        title='Sunburst chart for all countries',
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
        title='Number of starts per country'
    )

    fail_df = df[df['Status Mission'] == 'Failure']
    plot_map(fail_df, 'Status Mission', 'Number of Fails per country')

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

    fig = px.line(
        money, 
        x="year", 
        y="Rocket",
        title='Average money spent by year',
        width=800
    )

    st.plotly_chart(fig)

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
        title='Dynamic of top 5 companies by number of starts', 
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
        title='Leaders by launches for every year (countries)'
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
        title='Leaders by launches for every year (companies)',
        width=800
    )

    st.plotly_chart(fig)

    choice_company= st.selectbox('select company', df['Company Name'].unique())

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
        title='Launches per year for {}'.format(choice_company)
    )

    st.plotly_chart(fig)



    time_menu = ['year','month','hour','weekday']
    time_choice = st.selectbox('launch by time select', time_menu)
    
    if time_choice == time_menu[0] :


        ds = df['year'].value_counts().reset_index()

        ds.columns = [
            'year', 
            'count'
        ]

        fig = px.bar(
            ds, 
            x='year', 
            y="count", 
            orientation='v', 
            title='Missions number by year', 
            width=800
        )

        st.plotly_chart(fig)

    if time_choice == time_menu[1] :
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
            title='Missions number by month', 
            width=800
        )

        st.plotly_chart(fig)

    if time_choice == time_menu[2] :
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
            title='Missions number by hour', 
            width=800
        )

        st.plotly_chart(fig)

    if time_choice == time_menu[3] :
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
            title='Missions number by weekday', 
            width=800
        )

        st.plotly_chart(fig)



    choice_year = st.slider('select year',min_value=1957, max_value=2020)
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
        title='Number of starts for year', 
        width=800
    )

    st.plotly_chart(fig)

   

    data = df[df['Status Mission']=='Failure']
    data = data.groupby(['Company Name', 'year'])['Status Mission'].count().reset_index()

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
        title='Failures by year', 
        width=600
    )

    st.plotly_chart(fig)

    


    if st.button('space war between USA and USSR during cold war') :

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
            title='Number of launches', 
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
            title='USA vs USSR launches by year',
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
            title='USA vs USSR failures by year', 
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
            title='USA vs USSR: number of companies year by year',
            width=800
        )

        st.plotly_chart(fig)

       

  
        