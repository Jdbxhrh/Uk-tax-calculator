import streamlit as st

st.set_page_config(page_title="UK Take-Home Pay Calcuator", page_icon="💷", layout="centered") 

st.title("UK Take-Home Pay Calculator") 
st.caption("See your income tax, National Insurance and take-home pay.") 

salary = st.number_input("Annual Salary (£), min_value=0, value=35000, step=1000") 
pension = st.slider("Pension contribution (%)", 0, 100, 5) 

st.write(f"You entered £{salary}")