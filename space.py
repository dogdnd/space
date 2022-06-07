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


from space_eda import run_eda
from space_ml import run_ml
from space_home import run_home
import joblib




def main() :

    menu = ['HOME','EDA','ML']
    choice = st.sidebar.selectbox('메뉴', menu)
    if choice == menu[0] :
        run_home()
    
    elif choice == menu[1] :
        run_eda()

    elif choice == menu[2] :
        run_ml()


    

if __name__ == '__main__' :
    main()


