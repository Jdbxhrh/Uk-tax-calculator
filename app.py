import streamlit as st
import plotly.graph_objects as go
from calc import calc_income_tax,calc_ni,calc_student_loan,tax_breakdown,calc_take_home,find_salary
st.set_page_config(page_title="UK Take-Home Pay Calculator",page_icon="💷",layout="centered")

def money(label,default=""):
    text=st.text_input(label,value=default,placeholder="0.00")
    try:
        return max(float(text.replace(",","")),0.0)
    except ValueError:
        return 0.0

def item_group(title,key,hint,show_title=True):
    if show_title:
        st.subheader(title)
    if key not in st.session_state:
        st.session_state[key]=[]
    label=title if not show_title else "Name"
    with st.form(key+"form",clear_on_submit=True):
        g1,g2=st.columns(2)
        name=g1.text_input(label+" (e.g. "+hint+")")
        cost=g2.text_input("Cost (£)",placeholder="0.00")
        added=st.form_submit_button("+ Add")
    if added and name:
        try:
            st.session_state[key].append((name,float(cost)))
            st.rerun()
        except ValueError:
            st.warning("Enter the cost as a number, like 12.99")
    for i,(n,c) in enumerate(st.session_state[key]):
        n1,n2=st.columns([4,1])
        n1.write(f"{n}: £{c:,.2f}")
        if n2.button("Remove",key=f"{key}_rm{i}"):
            st.session_state[key].pop(i)
            st.rerun()
    return sum(c for n,c in st.session_state[key])

st.title("UK Take-Home Pay Calculator")
st.caption("See your income tax, National Insurance and take-home pay.")

tab1,tab2,tab3,tab4,tab5,tab6=st.tabs(["Take-home calculator","Budget","Charts","Reverse","Compare","Savings"])

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

    st.subheader("Income by tax band")
    rows=[]
    for name,amount,band_rate,band_tax in tax_breakdown(salary-pension_amount,scottish):
        if amount>0:
            rows.append({"Band":name,"Rate":f"{band_rate*100:.0f}%","Income in band":f"£{amount:,.0f}","Tax":f"£{band_tax:,.0f}"})
    if rows:
        st.table(rows)

with tab2:
    monthly=money("Monthly take-home (£)",str(round(take_home/12)))
    st.subheader("Essentials")
    rent=money("Rent (£)")
    food=money("Food (£)")
    bills_total=item_group("Bills","bills","Electric",False)
    subs_total=item_group("Subscriptions","subs","Netflix")
    transport_total=item_group("Transport","transport","Bus pass")
    spent=rent+food+subs_total+bills_total+transport_total
    left=monthly-spent
    c1,c2=st.columns(2)
    c1.metric("Spent",f"£{spent:,.2f}")
    c2.metric("Left over",f"£{left:,.2f}")

    budget_fig=go.Figure(go.Pie(labels=["Rent","Food","Subscriptions","Bills","Transport","Left over"],values=[rent,food,subs_total,bills_total,transport_total,max(left,0)],hole=0.5,marker_colors=["#C0392B","#E67E22","#2980B9","#8E44AD","#F1C40F","#1B5E3B"]))
    st.plotly_chart(budget_fig,use_container_width=True) 
    st.subheader("50/30/20 check") 
    if monthly>0: 
        needs=rent+food+bills_total+transport_total
        wants=subs_total 
        saved=max(left,0) 
        st.write(f"Needs: {needs/monthly*100:,.0f}% (aim for 50%)") 
        st.write(f"Wants: {wants/monthly*100:,.0f}% (aim for 30%)") 
        st.write(f"Savings: {saved/monthly*100:,.0f}% (aim for 20%)")

with tab3:
    st.subheader("Salary vs take-home")
    st.caption("Uses the pension, Scottish and student loan settings from the first tab")
    salaries=list(range(20000,150001,1000))
    takes=[calc_take_home(s,pension,scottish,plan) for s in salaries]
    line_fig=go.Figure()
    line_fig.add_trace(go.Scatter(x=salaries,y=salaries,name="Gross salary",line=dict(color="#7F8C8D",dash="dash")))
    line_fig.add_trace(go.Scatter(x=salaries,y=takes,name="Take-home",line=dict(color="#1B5E3B")))
    line_fig.update_layout(xaxis_title="Salary (£)",yaxis_title="£ per year",legend=dict(orientation="h"))
    st.plotly_chart(line_fig,use_container_width=True)

    st.subheader("Marginal tax rate")
    st.caption("Out of each extra £1 earned, how much goes in tax, NI and student loans. Ignores pension")
    marginal=[]
    for s in salaries:
        extra=calc_take_home(s+100,0,scottish,plan)-calc_take_home(s,0,scottish,plan)
        marginal.append((1-extra/100)*100)
    marg_fig=go.Figure(go.Scatter(x=salaries,y=marginal,line=dict(color="#C0392B")))
    marg_fig.update_layout(xaxis_title="Salary (£)",yaxis_title="Marginal rate (%)")
    st.plotly_chart(marg_fig,use_container_width=True)

with tab4:
    st.subheader("Reverse calculator")
    st.caption("Uses the pension, Scottish and student loan settings from the first tab.")
    target=money("Target monthly take-home (£)","2500")
    if target>0:
        needed=find_salary(target,pension,scottish,plan)
        st.metric("Salary needed per year",f"£{needed:,.0f}")
        st.write(f"That is £{needed/12:,.0f} gross per month.")

with tab5:
    st.subheader("Compare two jobs")
    st.caption("Uses the student loan setting from the first tab.")
    ca,cb=st.columns(2)
    sal_a=ca.number_input("Job A salary (£)",min_value=0,value=35000,step=1000)
    pen_a=ca.slider("Job A pension (%)",0,100,5)
    sco_a=ca.checkbox("Job A Scottish taxpayer")
    sal_b=cb.number_input("Job B salary (£)",min_value=0,value=40000,step=1000)
    pen_b=cb.slider("Job B pension (%)",0,100,5)
    sco_b=cb.checkbox("Job B Scottish taxpayer")
    take_a=calc_take_home(sal_a,pen_a,sco_a,plan)
    take_b=calc_take_home(sal_b,pen_b,sco_b,plan)
    ca.metric("Job A take-home per month",f"£{take_a/12:,.0f}")
    cb.metric("Job B take-home per month",f"£{take_b/12:,.0f}")
    diff=(take_b-take_a)/12
    if diff>=0:
        st.success(f"Job B pays £{diff:,.0f} more per month.")
    else:
        st.warning(f"Job B pays £{abs(diff):,.0f} less per month.")

with tab6:
    st.subheader("Savings goal")
    goal=st.number_input("Savings goal (£)",min_value=0,value=10000,step=500)
    deposit=st.number_input("Monthly deposit (£)",min_value=0,value=200,step=10)
    rate=st.slider("Interest rate per year (%)",0.0,10.0,4.0,0.1)
    months=0
    balance=0.0
    history=[0.0]
    paid=[0.0]
    while balance<goal and months<1200 and deposit>0:
        balance=balance*(1+rate/100/12)+deposit
        months+=1
        history.append(balance)
        paid.append(deposit*months)
    if deposit>0:
        st.metric("Time to reach goal",f"{months//12} years {months%12} months")
        sav_fig=go.Figure()
        sav_fig.add_scatter(x=list(range(len(history))),y=history,name="Balance")
        sav_fig.add_scatter(x=list(range(len(paid))),y=paid,name="Deposits only")
        sav_fig.update_layout(xaxis_title="Months",yaxis_title="£")
        st.plotly_chart(sav_fig,use_container_width=True)