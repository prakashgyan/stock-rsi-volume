import streamlit as st
from calculator import get_table
import pandas as pd
import numpy as np
import time

"""
# RSI CALCULAOR
"""
# st.header('RSI CALCULAOR')
st.sidebar.title('Select Parameters:')

option1 = st.sidebar.selectbox(
    'Period ',
    ['1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'], index=3, key='option1')
with st.sidebar.beta_container():
    option2_1 = 25
    option2_2 = 75
    option2_1 = st.sidebar.slider(
        'RSI Range :', 0, 99, 25, 1, key='option2_1')
    option2_2 = st.sidebar.slider(
        '', option2_1, 100, max(option2_1, 75), 1, key='option2_2')


# st.sidebar.markdown(f'#### {option2_1} - {option2_2}')
option3 = st.sidebar.slider(
    'Volume Ratio Trigger ', 1, 4, 3, 1, key='option3')
st.sidebar.markdown(f'##### Period: {option1}')
st.sidebar.markdown(f'##### RSI Range: [{option2_1} - {option2_2}]')
st.sidebar.markdown(f'##### VolRatio: {option3}')
st.sidebar.markdown(f'')

form_data = {
    'rsi_buy_sell': f'{option2_1},{option2_2}',
    'vol_ratio_trigger': option3,
    'period': option1
}
# st.write(f'Period : {option1} RSI Range : [{option2_1},{option2_2}]\tVolume Ratio Trigger : {option3}')
# my_bar = st.progress(0)
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1)

if st.sidebar.button('Calculate', key='run'):
    with st.spinner('Wait for it...'):
        # st.success('Done!')
        companies, timeofevent, paramets = get_table(form_data)
        st.markdown(f"<h5 style='text-align:center; color:red'>Time of Request : {timeofevent}</h5>", unsafe_allow_html=True)
        st.table(companies)
else:
    st.markdown("""
    #### Period : It is duration of stock Data to be considered for calculating RSI
    #### RSI Range : At what value to sell or Buy the stocks
    #### Volume Change Ratio : What ratio of volume change should trigger a Buy/Sell
    
    """)

