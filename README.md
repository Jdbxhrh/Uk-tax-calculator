# Uk Take-home Pay Calculator  

Live app: https://uk-tax-calculator-g2ehwpmnn46knulejsr9fd.streamlit.app/ 

A Python and Streamlit app that shows income tax, National Insurance and take-home pay for UK salaries.  

## Features 
- Take-home calculator with tax band breakdown (England and Scotland) 
- Budget planner with 50/30/20 check, CSV export, and save/load to JSON 
- Charts, reverse calculator and job comparison 
- Self-Employed, bonus, salary sacrifice and tax year comparison  
- Pay converter (hourly ,daily ,weekly ,monthly ,yearly) 

## How to run: 
Install the requirements: `pip install -r requirements.txt` 
Start the app: `python3 -m streamlit run app.py` 

## Rates Source: 
Tax, National Insurance and Student Loan rates come from GOV.UK for the 2025/26 and 2026/27 tax years. 

## Limitations: 
- Pension is taken from pay before tax (net pay arrangement) 
- Student loan plans can't be conbined (for example Plan 2 with Postgradute) 
- Bonuses, benefits and other income aren't included, apart from the bonus tab 
- Self-Employed uses Class 4 NI only 
- Pay converter assumes 52 working weeks a year3