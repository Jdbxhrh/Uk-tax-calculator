# UK Take-Home Pay Calculator

**Live app:** https://uk-tax-calculator-g2ehwpmnn46knulejsr9fd.streamlit.app/

A Python and Streamlit app that shows income tax, National Insurance and take-home pay for UK salaries.

## Features

- Take-home calculator with a tax band breakdown (England and Scotland) and student loan Plans 1, 2, 4, 5 and postgraduate
- Budget planner with a 50/30/20 check, and save and load as a JSON file
- Charts (with zoom and pan), reverse calculator and job comparison
- Savings goal, loan and mortgage calculator, and salary projection
- Self-employed, bonus, salary sacrifice and tax year comparison
- Pay converter (hourly, daily, weekly, monthly, yearly)
- Tax code checker, overtime and shift pay, and rent vs buy

## How to run

Install the requirements: `pip install -r requirements.txt`

Start the app: `python3 -m streamlit run app.py`

Run the tests: `python3 -m pytest`

## Project structure

- `app.py`: the Streamlit interface (banner, 16 tabs, charts and money boxes)
- `calc.py`: all the tax and money calculations
- `test_calc.py`: pytest tests for `calc.py`
- `requirements.txt`: streamlit, plotly, pytest

## Rates source

Tax, National Insurance and student loan rates come from GOV.UK and gov.scot for the 2025/26 and 2026/27 tax years.

## Limitations

- Pension is taken from pay before tax (net pay arrangement)
- Student loan plans can't be combined (for example Plan 2 with postgraduate)
- Bonuses, benefits and other income aren't included, apart from the bonus tab
- Self-employed uses Class 4 NI only
- Pay converter assumes 52 working weeks a year
- The tax code checker explains a code but doesn't change the other calculations
- Rent vs buy ignores stamp duty, fees and what a deposit could earn elsewhere
- Results are estimates, not financial or tax advice