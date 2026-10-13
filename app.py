import streamlit as st
import plotly.graph_objects as go
from calc import calc_income_tax,calc_ni,calc_student_loan

st.set_page_config(page_title="UK Take-Home Pay Calculator",page_icon="💷",layout="centered")

st.title("UK Take-Home Pay Calculator")
st.caption("See your income tax, National Insurance and take-home pay.")

tab1,tab2=st.tabs(["Take-home calculator","Budget"])

with tab1:
    salary=st.number_input("Annual salary (£)",min_value=0,value=35000,step=1000)
    pension=st.slider("Pension contribution (%)",0,100,5)
    scottish=st.checkbox("Scottish taxpayer")
    plan=st.selectbox("Student loan",["None","Plan 1","Plan 2","Plan 4","Plan 5","Postgraduate"])

    pension_amount=salary*pension/100
    tax=calc_income_tax(salary-pension_amount,scottish)
    ni=calc_ni(salary)
    loan=calc_student_loan(salary,plan)
    take_home=salary-pension_amount-tax-ni-loan

    col1,col2=st.columns(2)
    col1.metric("Take-home per year",f"£{take_home:,.0f}")
    col2.metric("Take-home per month",f"£{take_home/12:,.0f}")
    col3,col4,col5=st.columns(3)
    col3.metric("Income tax",f"£{tax:,.0f}")
    col4.metric("National Insurance",f"£{ni:,.0f}")
    col5.metric("Pension",f"£{pension_amount:,.0f}")
    st.metric("Student loan",f"£{loan:,.0f}")

    fig=go.Figure(go.Pie(labels=["Take-home","Income tax","National Insurance","Pension","Student loan"],values=[take_home,tax,ni,pension_amount,loan],hole=0.5,marker_colors=["#1B5E3B","#C0392B","#E67E22","#7F8C8D","#2980B9"]))
    st.plotly_chart(fig,use_container_width=True)

with tab2:
    monthly=st.number_input("Monthly take-home (£)",min_value=0.0,value=float(round(take_home/12)),step=50.0)
    st.subheader("Essentials")
    rent=st.number_input("Rent (£)",min_value=0.0,step=10.0)
    food=st.number_input("Food (£)",min_value=0.0,step=10.0)
    st.subheader("Subscriptions")
    if "subs" not in st.session_state:
        st.session_state.subs=[]
    s1,s2=st.columns(2)
    sub_name=s1.text_input("Name (e.g. Netflix)")
    sub_cost=s2.number_input("Cost (£)",min_value=0.0,step=1.0)
    if st.button("+ Add subscription"):
        if sub_name:
            st.session_state.subs.append((sub_name,sub_cost))
    for i,(name,cost) in enumerate(st.session_state.subs):
        n1,n2=st.columns([4,1])
        n1.write(f"{name}: £{cost:,.2f}")
        if n2.button("Remove",key=f"rm{i}"):
            st.session_state.subs.pop(i)
            st.rerun()
    subs_total=sum(cost for name,cost in st.session_state.subs)
    spent=rent+food+subs_total
    left=monthly-spent
    c1,c2=st.columns(2)
    c1.metric("Spent",f"£{spent:,.2f}")
    c2.metric("Left over",f"£{left:,.2f}")

    budget_fig=go.Figure(go.Pie(labels=["Rent","Food","Subscriptions","Left over"],values=[rent,food,subs_total,max(left,0)],hole=0.5,marker_colors=["#C0392B","#E67E22","#2980B9","#1B5E3B"]))
    st.plotly_chart(budget_fig,use_container_width=True)