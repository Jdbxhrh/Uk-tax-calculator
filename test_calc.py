import pytest 
from calc import calc_income_tax,calc_ni,calc_student_loan,tax_breakdown,calc_take_home,find_salary,calc_loan,calc_projection

def test_zero_income(): 
    assert calc_income_tax(0,False)==0 
    assert calc_ni(0)==0 

def test_take_home_35000(): 
    assert calc_take_home(35000,5,False,"None")==pytest.approx(27319.6,abs=1) 

def test_high_earner_england(): 
    assert calc_income_tax(125140,False)==pytest.approx(42516,abs=1) 

def test_scottish_pays_more_at_50000(): 
    assert calc_income_tax(50000,True)>calc_income_tax(50000,False) 

def test_student_loan(): 
    assert calc_student_loan(29385,"Plan 2")==0 
    assert calc_student_loan(39385,"Plan 2")==pytest.approx(900) 

def test_tax_breakdown_adds_up(): 
    rows=tax_breakdown(33250,False)
    assert sum(r[3] for r in rows)==pytest.approx(calc_income_tax(33250,False)) 

def test_find_salary_round_trip(): 
    salary=find_salary(2277,5,False,"None") 
    assert calc_take_home(salary,5,False,"None")/12==pytest.approx(2277,abs=0.01)

def test_loan_payment(): 
    monthly,total,interest=calc_loan(200000,5,25) 
    assert monthly==pytest.approx(1169,abs=1) 
    assert total-200000==pytest.approx(interest) 

def test_projection_rows(): 
    rows=calc_projection(35000,5,False,"None",3,2.5,10) 
    assert len(rows)==11  
    assert rows[0][1]==35000 

