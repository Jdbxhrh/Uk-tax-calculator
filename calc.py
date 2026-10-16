def calc_income_tax(taxable,scottish):
    allowance=12570
    if taxable>100000:
        allowance=max(0,12570-(taxable-100000)/2)
    income=max(0,taxable-allowance)
    if scottish:
        bands=[(3967,0.19),(16956,0.20),(31092,0.21),(62430,0.42),(125140,0.45),(float("inf"),0.48)]
    else:
        bands=[(37700,0.20),(125140,0.40),(float("inf"),0.45)]
    total=0
    lower=0
    for limit,rate in bands:
        if income>lower:
            total+=(min(income,limit)-lower)*rate
        lower=limit
    return total


def calc_ni(salary):
    main=max(min(salary,50270)-12570,0)
    upper=max(salary-50270,0)
    return main*0.08+upper*0.02


def calc_student_loan(salary,plan):
    plans={"Plan 1":(26900,0.09),"Plan 2":(29385,0.09),"Plan 4":(33795,0.09),"Plan 5":(25000,0.09),"Postgraduate":(21000,0.06)}
    if plan=="None":
        return 0
    threshold,rate=plans[plan]
    return max(salary-threshold,0)*rate


def tax_breakdown(taxable,scottish):
    allowance=12570
    if taxable>100000:
        allowance=max(0,12570-(taxable-100000)/2)
    income=max(0,taxable-allowance)
    if scottish:
        bands=[("Starter",3967,0.19),("Basic",16956,0.20),("Intermediate",31092,0.21),("Higher",62430,0.42),("Advanced",125140,0.45),("Top",float("inf"),0.48)]
    else:
        bands=[("Basic",37700,0.20),("Higher",125140,0.40),("Additional",float("inf"),0.45)]
    rows=[("Personal Allowance",min(taxable,allowance),0.0,0.0)]
    lower=0
    for name,limit,rate in bands:
        amount=max(min(income,limit)-lower,0)
        rows.append((name,amount,rate,amount*rate))
        lower=limit
    return rows 

def calc_take_home(salary,pension,scottish,plan):
    pension_amount=salary*pension/100
    tax=calc_income_tax(salary-pension_amount,scottish)
    ni=calc_ni(salary)
    loan=calc_student_loan(salary,plan)
    return salary-pension_amount-tax-ni-loan 

def find_salary(target_monthly,pension,scottish,plan):
    low=0
    high=10000000
    for i in range(60):
        mid=(low+high)/2
        if calc_take_home(mid,pension,scottish,plan)/12<target_monthly:
            low=mid
        else:
            high=mid
    return high 

def calc_loan(amount,rate,years):
    n=years*12
    r=rate/100/12
    if r==0:
        monthly=amount/n
    else:
        monthly=amount*r/(1-(1+r)**-n)
    total=monthly*n
    return monthly,total,total-amount 

def calc_projection(salary,pension,scottish,plan,raise_pct,inflation,years): 
    rows=[] 
    for y in range(years+1): 
        sal=salary*(1+raise_pct/100)**y 
        take=calc_take_home(sal,pension,scottish,plan) 
        real=take/(1+inflation/100)**y 
        rows.append((y,sal,take,real)) 
    return rows 


def calc_self_employed(income,expenses,scottish,plan):
    profit=max(income-expenses,0) 
    tax=calc_income_tax(profit,scottish) 
    ni=max(min(profit,50270)-12570,0)*0.06+max(profit-50270,0)*0.02 
    loan=calc_student_loan(profit,plan) 
    return profit,tax,ni,loan,profit-tax-ni-loan 

def calc_take_home_2025(salary,pension,scottish,plan): 
    pension_amount=salary*pension/100 
    taxable=salary-pension_amount 
    allowance=12570 
    if taxable>100000: 
        allowance=max(0,12570-(taxable-100000)/2) 
    income=max(0,taxable-allowance) 
    if scottish: 
        bands=[(2827,0.19),(14921,0.20),(31092,0.21),(62430,0.42),(125140,0.45),(float("inf"),0.48)] 
    else: 
        bands=[(37700,0.20),(125140,0.40),(float("inf"),0.45)] 
    tax=0 
    lower=0 
    for limit,band_rate in bands: 
        if income>lower: 
            tax+=(min(income,limit)-lower)*band_rate 
        lower=limit 
    ni=calc_ni(salary) 
    plans={"Plan 1":(26065,0.09),"Plan 2":(28470,0.09),"Plan 4":(32745,0.09),"Plan 5":(25000,0.09),"Postgraduate":(21000,0.06)}
    loan=0
    if plan!="None": 
        threshold,loan_rate=plans[plan]
        loan=max(salary-threshold,0)*loan_rate 
    return salary-pension_amount-tax-ni-loan 
 
        