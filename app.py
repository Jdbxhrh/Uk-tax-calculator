import streamlit as st
import plotly.graph_objects as go
import json
import streamlit.components.v1 as components
from calc import calc_income_tax,calc_ni,calc_student_loan,tax_breakdown,calc_take_home,find_salary,calc_loan,calc_projection,calc_self_employed,calc_take_home_2025
st.set_page_config(page_title="UK Take-Home Pay Calculator",page_icon="💷",layout="wide")
st.markdown("<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');html,body,.stApp{font-family:'Inter',sans-serif;}</style>",unsafe_allow_html=True)
st.markdown("<style>div[data-baseweb='tab-list']{gap:8px 24px;flex-wrap:wrap;overflow:visible;border:1px solid rgba(128,128,128,0.4);border-radius:8px;padding:6px 16px;position:sticky;top:3.5rem;z-index:999;background-color:var(--background-color,#0E1117);}div[data-baseweb='tab-highlight'],div[data-baseweb='tab-border']{display:none;}button[data-baseweb='tab']{padding:10px 4px;}</style>",unsafe_allow_html=True)
st.markdown("<style>div.block-container{max-width:1100px;margin:auto;}</style>",unsafe_allow_html=True)
st.markdown("<style>.banner{background:linear-gradient(135deg,#1B5E3B,#134029);border-left:6px solid #7F8C8D;border-radius:8px;padding:28px 32px;margin-bottom:16px;}.banner-title{color:#FFFFFF;font-size:2rem;font-weight:600;line-height:1.2;}.banner-sub{color:rgba(255,255,255,0.8);font-size:1rem;margin-top:6px;}</style>",unsafe_allow_html=True)

components.html("""<script>
const d=window.parent.document;
if(!d.commaHook){
d.commaHook=true;
d.addEventListener('input',function(e){
const el=e.target;
if(el.tagName!=='INPUT'||el.type!=='text'||!e.isTrusted)return;
const raw=el.value.replace(/,/g,'');
if(raw===''||!/^\\d*\\.?\\d*$/.test(raw))return;
const parts=raw.split('.');
parts[0]=parts[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');
const out=parts.join('.');
if(out===el.value)return;
const pos=el.selectionStart;
const before=(el.value.slice(0,pos).match(/,/g)||[]).length;
const setter=Object.getOwnPropertyDescriptor(window.parent.HTMLInputElement.prototype,'value').set;
setter.call(el,out);
let n=pos-before,i=0;
while(i<out.length&&n>0){if(out[i]!==',')n--;i++;}
el.setSelectionRange(i,i);
el.dispatchEvent(new Event('input',{bubbles:true}));
},true);
}
</script>""",height=0)

def show_zoom(fig):
    fig.update_layout(dragmode="pan")
    st.plotly_chart(fig,use_container_width=True,config={"scrollZoom":True})

def fmt_commas(key):
    text=st.session_state[key].replace(",","")
    try:
        if "." in text:
            whole,dec=text.split(".",1)
            st.session_state[key]=f"{int(whole or 0):,}."+dec
        else:
            st.session_state[key]=f"{int(text):,}"
    except ValueError:
        pass

def money(label,default="",key=None,box=st):
    text=box.text_input(label,placeholder=default or "0.00",key=key,on_change=fmt_commas,args=(key,))
    try:
        return max(float((text or default).replace(",","")),0.0)
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
            st.session_state[key].append((name,float(cost.replace(",",""))))
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

st.markdown("<div class='banner'><div class='banner-title'>💷 UK Take-Home Pay Calculator</div><div class='banner-sub'>See your income tax, National Insurance and take-home pay.</div></div>",unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10,tab11,tab12,tab13,tab14,tab15,tab16=st.tabs(["Take-home calculator","Budget","Charts","Reverse","Compare","Savings","Loans","Projection","Self-employed","Bonus","Sacrifice","Tax year","Pay converter","Tax code","Overtime","Rent vs buy"])

with tab1:
    salary=money("Annual salary (£)","35,000",key="salary_money")
    pension=st.slider("Pension contribution (%)",0,100,5)
    scottish=st.checkbox("Scottish taxpayer")
    plan=st.selectbox("Student loan",["None","Plan 1","Plan 2","Plan 4","Plan 5","Postgraduate"])

    pension_amount=salary*pension/100
    tax=calc_income_tax(salary-pension_amount,scottish)
    ni=calc_ni(salary)
    loan=calc_student_loan(salary,plan)
    take_home=salary-pension_amount-tax-ni-loan

    col1,col2=st.columns(2)
    col1.metric("Take-home per year",f"£{take_home:,.0f}",border=True)
    col2.metric("Take-home per month",f"£{take_home/12:,.0f}",border=True)
    col3,col4,col5=st.columns(3)
    col3.metric("Income Tax",f"£{tax:,.0f}",border=True)
    col4.metric("National Insurance",f"£{ni:,.0f}",border=True)
    col5.metric("Pension",f"£{pension_amount:,.0f}",border=True)
    st.metric("Student loan",f"£{loan:,.0f}",border=True)
    fig=go.Figure(go.Pie(labels=["Take-home","Income tax","National Insurance","Pension","Student loan"],values=[take_home,tax,ni,pension_amount,loan],hole=0.5,marker_colors=["#1B5E3B","#C0392B","#E67E22","#7F8C8D","#2980B9"],hovertemplate="%{label}<br>£%{value:,.0f}<extra></extra>"))
    st.plotly_chart(fig,use_container_width=True)

    st.subheader("Income by tax band")
    rows=[]
    for name,amount,band_rate,band_tax in tax_breakdown(salary-pension_amount,scottish):
        if amount>0:
            rows.append({"Band":name,"Rate":f"{band_rate*100:.0f}%","Income in band":f"£{amount:,.0f}","Tax":f"£{band_tax:,.0f}"})
    if rows:
        st.table(rows)

with tab2:
    st.subheader("Save and load budget")
    budget_data={
        "monthly":st.session_state.get("budget_monthly",""),
        "rent":st.session_state.get("budget_rent",""),
        "food":st.session_state.get("budget_food",""),
        "bills":st.session_state.get("bills",[]),
        "subs":st.session_state.get("subs",[]),
        "transport":st.session_state.get("transport",[])
    }
    st.download_button(
        "Download budget",
        data=json.dumps(budget_data,indent=4),
        file_name="my_budget.json",
        mime="application/json"
    )
    uploaded=st.file_uploader("Upload a saved budget",type="json")
    if uploaded is not None:
        if st.button("Load budget"):
            try:
                loaded=json.load(uploaded)
                for key in ["budget_monthly","budget_rent","budget_food"]:
                    short=key.replace("budget_","")
                    st.session_state[key]=str(loaded.get(short,""))
                for key in ["bills","subs","transport"]:
                    st.session_state[key]=loaded.get(key,[])
                st.rerun()
            except (ValueError,TypeError,KeyError,AttributeError):
                st.error("Invalid budget file.")
    st.divider()
    monthly=money("Monthly take-home (£)",f"{round(take_home/12):,}",key="budget_monthly")
    st.subheader("Essentials")
    rent=money("Rent (£)",key="budget_rent")
    food=money("Food (£)",key="budget_food")
    bills_total=item_group("Bills","bills","Electric",False)
    subs_total=item_group("Subscriptions","subs","Netflix")
    transport_total=item_group("Transport","transport","Bus pass")
    spent=rent+food+subs_total+bills_total+transport_total
    left=monthly-spent
    c1,c2=st.columns(2)
    c1.metric("Spent",f"£{spent:,.2f}",border=True)
    c2.metric("Left over",f"£{left:,.2f}",border=True)
    budget_fig=go.Figure(go.Pie(labels=["Rent","Food","Subscriptions","Bills","Transport","Left over"],values=[rent,food,subs_total,bills_total,transport_total,max(left,0)],hole=0.5,marker_colors=["#C0392B","#E67E22","#2980B9","#8E44AD","#F1C40F","#1B5E3B"],hovertemplate="%{label}<br>£%{value:,.2f}<extra></extra>"))
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
    show_zoom(line_fig)

    st.subheader("Marginal tax rate")
    st.caption("Out of each extra £1 earned, how much goes in tax, NI and student loans. Ignores pension")
    marginal=[]
    for s in salaries:
        extra=calc_take_home(s+100,0,scottish,plan)-calc_take_home(s,0,scottish,plan)
        marginal.append((1-extra/100)*100)
    marg_fig=go.Figure(go.Scatter(x=salaries,y=marginal,line=dict(color="#C0392B")))
    marg_fig.update_layout(xaxis_title="Salary (£)",yaxis_title="Marginal rate (%)")
    show_zoom(marg_fig)

with tab4:
    st.subheader("Reverse calculator")
    st.caption("Uses the pension, Scottish and student loan settings from the first tab.")
    target=money("Target monthly take-home (£)","2,500",key="target_money")
    if target>0:
        needed=find_salary(target,pension,scottish,plan)
        st.metric("Salary needed per year",f"£{needed:,.0f}",border=True)
        st.write(f"That is £{needed/12:,.0f} gross per month.")

with tab5:
    st.subheader("Compare two jobs")
    st.caption("Uses the student loan setting from the first tab.")
    ca,cb=st.columns(2)
    sal_a=money("Job A salary (£)","35,000",key="sal_a_money",box=ca)
    pen_a=ca.slider("Job A pension (%)",0,100,5)
    sco_a=ca.checkbox("Job A Scottish taxpayer")
    sal_b=money("Job B salary (£)","40,000",key="sal_b_money",box=cb)
    pen_b=cb.slider("Job B pension (%)",0,100,5)
    sco_b=cb.checkbox("Job B Scottish taxpayer")
    take_a=calc_take_home(sal_a,pen_a,sco_a,plan)
    take_b=calc_take_home(sal_b,pen_b,sco_b,plan)
    ca.metric("Job A take-home per month",f"£{take_a/12:,.0f}",border=True)
    cb.metric("Job B take-home per month",f"£{take_b/12:,.0f}",border=True)
    diff=(take_b-take_a)/12
    if diff>=0:
        st.success(f"Job B pays £{diff:,.0f} more per month.")
    else:
        st.warning(f"Job B pays £{abs(diff):,.0f} less per month.")

with tab6:
    st.subheader("Savings goal")
    goal=money("Savings goal (£)","10,000",key="goal_money")
    deposit=money("Monthly deposit (£)","200",key="deposit_money")
    rate=st.slider("Interest rate per year (%)",0.0,10.0,4.0,0.1)
    months=0
    balance=0.0
    history=[0.0]
    paid=[0.0]
    while balance<goal and months<120000 and deposit>0:
        balance=balance*(1+rate/100/12)+deposit
        months+=1
        history.append(balance)
        paid.append(deposit*months)
    if deposit>0:
        st.metric("Time to reach goal",f"{months//12} years {months%12} months",border=True)
        sav_fig=go.Figure()
        sav_fig.add_scatter(x=list(range(len(history))),y=history,name="Balance",line=dict(color="#1B5E3B"))
        sav_fig.add_scatter(x=list(range(len(paid))),y=paid,name="Deposits only",line=dict(color="#7F8C8D",dash="dash"))
        sav_fig.update_layout(xaxis_title="Months",yaxis_title="£")
        show_zoom(sav_fig)

with tab7:
    st.subheader("Loan and mortgage calculator")
    loan_amount=money("Amount borrowed (£)","200,000",key="loan_money")
    loan_rate=st.slider("Interest rate per year (%)",0.0,15.0,5.0,0.1)
    loan_years=st.slider("Term (years)",1,40,25)
    if loan_amount>0:
        pay,total_paid,interest=calc_loan(loan_amount,loan_rate,loan_years)
        l1,l2,l3=st.columns(3)
        l1.metric("Monthly payment",f"£{pay:,.0f}",border=True)
        l2.metric("Total paid",f"£{total_paid:,.0f}",border=True)
        l3.metric("Total interest",f"£{interest:,.0f}",border=True)
        r=loan_rate/100/12
        bal=float(loan_amount)
        balances=[bal]
        for m in range(loan_years*12):
            bal=bal*(1+r)-pay
            balances.append(max(bal,0))
        loan_fig=go.Figure()
        loan_fig.add_scatter(x=[m/12 for m in range(len(balances))],y=balances,name="Balance left",line=dict(color="#C0392B"))
        loan_fig.update_layout(xaxis_title="Years",yaxis_title="£ left to pay")
        show_zoom(loan_fig)

with tab8:
    st.subheader("Salary projection")
    st.caption("Uses the pension, Scottish and student loan settings from the first tab.")
    proj_salary=money("Starting salary (£)","35,000",key="proj_money")
    raise_pct=st.slider("Yearly pay rise (%)",0.0,10.0,2.5,0.5)
    inflation=st.slider("Inflation per year (%)",0.0,10.0,2.5,0.5)
    proj_years=st.slider("Years to project",1,30,10)
    if proj_salary>0:
        proj=calc_projection(proj_salary,pension,scottish,plan,raise_pct,inflation,proj_years)
        last=proj[-1]
        p1,p2=st.columns(2)
        p1.metric(f"Take-home per month in year {proj_years}",f"£{last[2]/12:,.0f}",border=True)
        p2.metric("Same amount in today's money",f"£{last[3]/12:,.0f}",border=True)
        proj_fig=go.Figure()
        proj_fig.add_scatter(x=[row[0] for row in proj],y=[row[2]/12 for row in proj],name="Take-home",line=dict(color="#1B5E3B"))
        proj_fig.add_scatter(x=[row[0] for row in proj],y=[row[3]/12 for row in proj],name="In today's money",line=dict(color="#7F8C8D",dash="dash"))
        proj_fig.update_layout(xaxis_title="Years",yaxis_title="£ per month",legend=dict(orientation="h"))
        show_zoom(proj_fig)

with tab9:
    st.subheader("Self-employed")
    st.caption("Uses the Scottish and student loan settings from the first tab. Class 4 NI only, as Class 2 is now voluntary.")
    se_income=money("Income from self-employment (£)","50,000",key="se_income_money")
    se_expenses=money("Business expenses (£)","10,000",key="se_expenses_money")
    profit,se_tax,se_ni,se_loan,se_take=calc_self_employed(se_income,se_expenses,scottish,plan)
    s1,s2=st.columns(2)
    s1.metric("Profit",f"£{profit:,.0f}",border=True)
    s2.metric("Take-home per month",f"£{se_take/12:,.0f}",border=True)
    s3,s4,s5=st.columns(3)
    s3.metric("Income tax",f"£{se_tax:,.0f}",border=True)
    s4.metric("Class 4 NI",f"£{se_ni:,.0f}",border=True)
    s5.metric("Student loan",f"£{se_loan:,.0f}",border=True)

with tab10:
    st.subheader("Bonus calculator")
    st.caption("Uses the salary, pension, Scottish and student loan settings from the first tab. Pension is taken from the bonus too.")
    bonus=money("One-off bonus (£)","5,000",key="bonus_money")
    kept=calc_take_home(salary+bonus,pension,scottish,plan)-calc_take_home(salary,pension,scottish,plan)
    b1,b2=st.columns(2)
    b1.metric("You keep",f"£{kept:,.0f}",border=True)
    b2.metric("Share kept",f"{kept/bonus*100 if bonus>0 else 0:,.0f}%",border=True)
    st.write(f"£{bonus-kept:,.0f} of the bonus goes on tax, NI, pension and student loan.")

with tab11:
    st.subheader("Salary sacrifice vs normal pension")
    st.caption("Uses the salary, pension, Scottish and student loan settings from the first tab. Your pension pot is the same either way.")
    normal=calc_take_home(salary,pension,scottish,plan)
    sacrifice=calc_take_home(salary-salary*pension/100,0,scottish,plan)
    x1,x2=st.columns(2)
    x1.metric("Normal pension, per month",f"£{normal/12:,.0f}",border=True)
    x2.metric("Salary sacrifice, per month",f"£{sacrifice/12:,.0f}",border=True)
    st.metric("Extra you keep per year",f"£{sacrifice-normal:,.0f}",border=True)

with tab12:
    st.subheader("Tax year comparison")
    st.caption("Uses the salary, pension, Scottish and student loan settings from the first tab. 2025/26 against 2026/27.")
    old=calc_take_home_2025(salary,pension,scottish,plan)
    new=calc_take_home(salary,pension,scottish,plan)
    y1,y2=st.columns(2)
    y1.metric("2025/26 per month",f"£{old/12:,.0f}",border=True)
    y2.metric("2026/27 per month",f"£{new/12:,.0f}",border=True)
    st.metric("Difference per year",f"£{new-old:,.0f}",border=True)

with tab13:
    st.subheader("Pay converter")
    st.caption("Convert gross pay between hourly, daily, weekly, monthly and yearly amounts.")
    pay_amount=money("Pay amount (£)","15",key="pay_money")
    pay_period=st.selectbox("Pay period",["Hourly","Daily","Weekly","Monthly","Yearly"])
    hours_day=st.number_input("Hours worked per day",min_value=0.5,value=8.0,step=0.5)
    days_week=st.number_input("Days worked per week",min_value=1.0,max_value=7.0,value=5.0,step=0.5)
    hours_week=hours_day*days_week

    if pay_period=="Hourly":
        annual=pay_amount*hours_week*52
    elif pay_period=="Daily":
        annual=pay_amount*days_week*52
    elif pay_period=="Weekly":
        annual=pay_amount*52
    elif pay_period=="Monthly":
        annual=pay_amount*12
    else:
        annual=pay_amount

    hourly=annual/(hours_week*52)
    daily=annual/(days_week*52)
    weekly=annual/52
    per_month=annual/12

    st.subheader("Converted pay")
    k1,k2=st.columns(2)
    k1.metric("Hourly",f"£{hourly:,.2f}",border=True)
    k2.metric("Daily",f"£{daily:,.2f}",border=True)
    k3,k4=st.columns(2)
    k3.metric("Weekly",f"£{weekly:,.2f}",border=True)
    k4.metric("Monthly",f"£{per_month:,.2f}",border=True)
    st.metric("Yearly",f"£{annual:,.2f}",border=True)
    st.caption("Assumes 52 working weeks per year. Figures are before tax and deductions.")

with tab14:
    st.subheader("Tax code checker")
    st.caption("Type a tax code like 1257L to see what it means.")
    code=st.text_input("Tax code",placeholder="1257L").upper().replace(" ","")
    if code:
        text=code
        region="England or Northern Ireland"
        if text.startswith("S"):
            region="Scotland"
            text=text[1:]
        elif text.startswith("C"):
            region="Wales"
            text=text[1:]
        special={"BR":"Basic rate. All your income from this job is taxed at 20%, with no allowance.","D0":"Higher rate. All your income from this job is taxed at 40%.","D1":"Additional rate. All your income from this job is taxed at 45%.","NT":"No tax is taken from this income.","0T":"No tax-free allowance, so tax is taken from the first pound."}
        letters={"L":"Standard allowance.","M":"You receive Marriage Allowance from your partner.","N":"You gave some of your allowance to your partner.","T":"HMRC needs to review other items in your allowance."}
        if text in special:
            if region=="Scotland":
                st.info("Scottish BR and D codes use the Scottish rates, so check the exact rate on GOV.UK.")
            else:
                st.info(special[text])
        elif text[:-1].isdigit() and text[-1] in letters:
            allowance=int(text[:-1])*10
            a1,a2=st.columns(2)
            a1.metric("Tax-free allowance",f"£{allowance:,.0f}",border=True)
            a2.metric("Compared with standard £12,570",f"£{allowance-12570:,.0f}",border=True)
            st.write(f"{letters[text[-1]]} Region: {region}.")
        elif text.startswith("K") and text[1:].isdigit():
            extra=int(text[1:])*10
            st.metric("Added to your taxable income",f"£{extra:,.0f}",border=True)
            st.write(f"K codes mean you owe tax on benefits or untaxed income. Region: {region}.")
        else:
            st.warning("Code not recognised. Try 1257L, S1257L, BR, D0 or K475.")

with tab15:
    st.subheader("Overtime and shift pay")
    st.caption("Uses the salary, pension, Scottish and student loan settings from the first tab. Pension is taken from overtime too.")
    ot_rate=money("Basic hourly rate (£)","15",key="ot_rate_money")
    ot_hours=st.number_input("Overtime hours per week",min_value=0.0,value=5.0,step=0.5)
    ot_mult=st.selectbox("Overtime pay rate",["1x","1.25x","1.5x","2x"],index=2)
    shift_pm=money("Shift allowance per month (£)","0",key="shift_money")
    extra_gross=ot_rate*float(ot_mult[:-1])*ot_hours*52+shift_pm*12
    kept_ot=calc_take_home(salary+extra_gross,pension,scottish,plan)-calc_take_home(salary,pension,scottish,plan)
    o1,o2=st.columns(2)
    o1.metric("Extra gross per month",f"£{extra_gross/12:,.0f}",border=True)
    o2.metric("You keep per month",f"£{kept_ot/12:,.0f}",border=True)
    st.metric("Share kept",f"{kept_ot/extra_gross*100 if extra_gross>0 else 0:,.0f}%",border=True)

with tab16:
    st.subheader("Rent vs buy")
    st.caption("Compares the total cost of renting with buying over the years you stay. Ignores stamp duty, fees and what your deposit could earn elsewhere.")
    rent_pm=money("Monthly rent (£)","1,200",key="rvb_rent_money")
    price=money("House price (£)","250,000",key="rvb_price_money")
    dep_pct=st.slider("Deposit (%)",5,50,10)
    mort_rate=st.slider("Mortgage rate per year (%)",0.0,10.0,4.5,0.1)
    mort_years=st.slider("Mortgage term (years)",5,40,25)
    stay=st.slider("Years you stay",1,30,10)
    growth=st.slider("House price growth per year (%)",0.0,10.0,3.0,0.5)
    rent_rise=st.slider("Rent rise per year (%)",0.0,10.0,3.0,0.5)
    if price>0:
        deposit_amt=price*dep_pct/100
        borrowed=price-deposit_amt
        mort_pay=calc_loan(borrowed,mort_rate,mort_years)[0]
        months_paid=min(stay,mort_years)*12
        mr=mort_rate/100/12
        mort_bal=borrowed
        for m in range(months_paid):
            mort_bal=mort_bal*(1+mr)-mort_pay
        mort_bal=max(mort_bal,0)
        sale=price*(1+growth/100)**stay
        maintenance=price*0.01*stay
        buy_cost=deposit_amt+mort_pay*months_paid+maintenance-(sale-mort_bal)
        rent_cost=sum(rent_pm*12*(1+rent_rise/100)**y for y in range(stay))
        v1,v2=st.columns(2)
        v1.metric("Total rent",f"£{rent_cost:,.0f}",border=True)
        v2.metric("Net cost of buying",f"£{buy_cost:,.0f}",border=True)
        if buy_cost<rent_cost:
            st.success(f"Buying costs £{rent_cost-buy_cost:,.0f} less over {stay} years.")
        else:
            st.warning(f"Renting costs £{buy_cost-rent_cost:,.0f} less over {stay} years.")
        st.caption("Net cost of buying = deposit + mortgage payments + 1% a year upkeep, minus what is left after selling and paying off the mortgage.")