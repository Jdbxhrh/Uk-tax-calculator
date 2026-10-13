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