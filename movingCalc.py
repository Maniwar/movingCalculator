import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(layout="wide")

# Helper function to calculate annual expenses
def calculate_annual_expenses(monthly_payment, annual_property_tax, state_tax_rate, monthly_common_expenses, spending_increase_percentage):
    annual_house_payment = monthly_payment * 12
    total_property_tax = annual_property_tax
    total_state_tax = (annual_house_payment + total_property_tax) * (state_tax_rate / 100)
    annual_common_expenses = monthly_common_expenses * 12
    new_common_expenses = annual_common_expenses * (1 + spending_increase_percentage / 100)
    total_annual_expenses = annual_house_payment + total_property_tax + total_state_tax + new_common_expenses
    return total_annual_expenses, annual_house_payment, total_property_tax, total_state_tax, annual_common_expenses, new_common_expenses

# Function to create a downloadable Excel file
def create_excel_report(results_df, breakdown_df, detailed_calculations):
    try:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            results_df.to_excel(writer, index=False, sheet_name='Results')
            breakdown_df.to_excel(writer, index=False, sheet_name='Breakdown')
            workbook = writer.book
            detailed_worksheet = workbook.add_worksheet('Detailed Calculations')
            row = 0
            for section, calculations in detailed_calculations.items():
                detailed_worksheet.write(row, 0, section)
                row += 1
                for calc in calculations:
                    detailed_worksheet.write(row, 0, calc)
                    row += 1
                row += 1
        output.seek(0)
        return output
    except Exception as e:
        st.error(f"Error creating Excel report: {e}")
        return None

# Function to display inputs
def display_inputs():
    col1, col2 = st.columns(2)
    with col1:
        st.header('Current Situation')
        current_salary = st.number_input('Net annual salary ($)', min_value=0, step=1000, format='%d', key='current_salary')
        current_monthly_house_payment = st.number_input('Monthly house payment ($)', min_value=0, step=100, format='%d', key='current_monthly_house_payment')
        current_annual_property_tax = st.number_input('Annual property tax ($)', min_value=0, step=100, format='%d', key='current_annual_property_tax')
        current_state_tax_rate = st.number_input('State tax rate (%)', min_value=0.0, max_value=100.0, step=0.01, format='%.2f', key='current_state_tax_rate')
        current_monthly_common_expenses = st.number_input('Current monthly household and utility expenses ($)', min_value=0, step=100, format='%d', key='current_monthly_common_expenses')
    with col2:
        st.header('New Situation')
        new_monthly_house_payment = st.number_input('Monthly house payment ($)', min_value=0, step=100, format='%d', key='new_monthly_house_payment')
        new_annual_property_tax = st.number_input('Annual property tax ($)', min_value=0, step=100, format='%d', key='new_annual_property_tax')
        new_state_tax_rate = st.number_input('State tax rate (%)', min_value=0.0, max_value=100.0, step=0.01, format='%.2f', key='new_state_tax_rate')
        spending_increase_percentage = st.number_input('Increase in spending (%)', min_value=0.0, max_value=100.0, step=0.01, format='%.2f', key='spending_increase_percentage')
    return current_salary, current_monthly_house_payment, current_annual_property_tax, current_state_tax_rate, current_monthly_common_expenses, new_monthly_house_payment, new_annual_property_tax, new_state_tax_rate, spending_increase_percentage

# Function to display results
def display_results(current_annual_expenses, new_annual_expenses, additional_expenses):
    results_data = {
        'Description': ['Current Annual Expenses', 'New Annual Expenses', 'Additional Expenses'],
        'Amount ($)': [f'{current_annual_expenses:,.2f}', f'{new_annual_expenses:,.2f}', f'{additional_expenses:,.2f}']
    }
    results_df = pd.DataFrame(results_data)
    st.table(results_df)
    return results_df

# Function to display breakdown of additional expenses
def display_breakdown(new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_common_expenses):
    st.subheader('Breakdown of Additional Expenses')
    breakdown_data = {
        'Description': ['New Annual House Payment', 'New Annual Property Tax', 'New Annual State Tax', 'New Annual Common Expenses'],
        'Amount ($)': [f'{new_annual_house_payment:,.2f}', f'{new_total_property_tax:,.2f}', f'{new_total_state_tax:,.2f}', f'{new_common_expenses:,.2f}']
    }
    breakdown_df = pd.DataFrame(breakdown_data)
    st.table(breakdown_df)
    return breakdown_df

# Function to display detailed calculations
def display_detailed_calculations(current_monthly_house_payment, current_annual_house_payment, current_total_property_tax, current_total_state_tax, current_annual_expenses, current_annual_common_expenses,
                                  new_monthly_house_payment, new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_common_expenses, new_annual_expenses, current_state_tax_rate, spending_increase_percentage, new_state_tax_rate, current_monthly_common_expenses):
    st.subheader('Detailed Calculations')
    detailed_calculations = {
        'Calculation Steps': [
            f' - Current Annual House Payment: {current_monthly_house_payment} * 12 = ${current_annual_house_payment:,.2f}',
            f' - Current Annual Property Tax: ${current_total_property_tax:,.2f}',
            f' - Current Annual State Tax: (${current_annual_house_payment:,.2f} + ${current_total_property_tax:,.2f}) * {current_state_tax_rate / 100:.2f} = ${current_total_state_tax:,.2f}',
            f' - Current Total Annual Expenses: ${current_annual_house_payment:,.2f} + ${current_total_property_tax:,.2f} + ${current_total_state_tax:,.2f} + ${current_annual_common_expenses:,.2f} = ${current_annual_expenses:,.2f}',
            f' - New Annual House Payment: {new_monthly_house_payment} * 12 = ${new_annual_house_payment:,.2f}',
            f' - New Annual Property Tax: ${new_total_property_tax:,.2f}',
            f' - New Annual State Tax: (${new_annual_house_payment:,.2f} + ${new_total_property_tax:,.2f}) * {new_state_tax_rate / 100:.2f} = ${new_total_state_tax:,.2f}',
            f' - New Annual Common Expenses: ${current_monthly_common_expenses} * 12 * (1 + {spending_increase_percentage / 100:.2f}) = ${new_common_expenses:,.2f}',
            f' - New Total Annual Expenses: ${new_annual_house_payment:,.2f} + ${new_total_property_tax:,.2f} + ${new_total_state_tax:,.2f} + ${new_common_expenses:,.2f} = ${new_annual_expenses:,.2f}'
        ]
    }
    for calc in detailed_calculations['Calculation Steps']:
        st.write(calc)
    return detailed_calculations

# Function to display charts
def display_charts(current_annual_house_payment, current_total_property_tax, current_total_state_tax, current_annual_common_expenses,
                   new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_common_expenses):
    st.subheader('Comparison of Current and New Annual Expenses')
    expense_comparison_data = {
        'Category': ['House Payment', 'Property Tax', 'State Tax', 'Common Expenses'],
        'Current Annual ($)': [current_annual_house_payment, current_total_property_tax, current_total_state_tax, current_annual_common_expenses],
        'New Annual ($)': [new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_common_expenses]
    }
    expense_comparison_df = pd.DataFrame(expense_comparison_data)
    fig = px.bar(expense_comparison_df, x='Category', y=['Current Annual ($)', 'New Annual ($)'], barmode='group', title='Comparison of Current and New Annual Expenses by Category')
    st.plotly_chart(fig)

    st.subheader('Proportion of Each Category in New Annual Expenses')
    new_expense_proportion_data = {
        'Category': ['House Payment', 'Property Tax', 'State Tax', 'Common Expenses'],
        'New Annual ($)': [new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_common_expenses]
    }
    new_expense_proportion_df = pd.DataFrame(new_expense_proportion_data)
    fig = px.pie(new_expense_proportion_df, values='New Annual ($)', names='Category', title='Proportion of Each Category in New Annual Expenses')
    st.plotly_chart(fig)

# Main function to run the app
def main():
    st.title('Salary Comparison and Raise Calculator')
    
    current_salary, current_monthly_house_payment, current_annual_property_tax, current_state_tax_rate, current_monthly_common_expenses, new_monthly_house_payment, new_annual_property_tax, new_state_tax_rate, spending_increase_percentage = display_inputs()

    if st.button('Calculate Required Salary'):
        current_annual_expenses, current_annual_house_payment, current_total_property_tax, current_total_state_tax, current_annual_common_expenses, _ = calculate_annual_expenses(current_monthly_house_payment, current_annual_property_tax, current_state_tax_rate, current_monthly_common_expenses, 0)
        new_annual_expenses, new_annual_house_payment, new_total_property_tax, new_total_state_tax, _, new_common_expenses = calculate_annual_expenses(new_monthly_house_payment, new_annual_property_tax, new_state_tax_rate, current_monthly_common_expenses, spending_increase_percentage)
        
        additional_expenses = new_annual_expenses - current_annual_expenses
        required_new_salary = current_salary + additional_expenses
        monthly_required_new_salary = required_new_salary / 12
        percentage_increase = ((required_new_salary - current_salary) / current_salary) * 100
        
        st.subheader('Results')
        st.markdown(f"<h3 style='color: red;'>Needed Annual Salary: ${required_new_salary:,.2f}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: red;'>Needed Monthly Salary: ${monthly_required_new_salary:,.2f}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: red;'>Percentage Increase: {percentage_increase:.2f}%</h3>", unsafe_allow_html=True)

        results_df = display_results(current_annual_expenses, new_annual_expenses, additional_expenses)
        breakdown_df = display_breakdown(new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_common_expenses)
        detailed_calculations = display_detailed_calculations(current_monthly_house_payment, current_annual_house_payment, current_total_property_tax, current_total_state_tax, current_annual_expenses, current_annual_common_expenses,
                                                              new_monthly_house_payment, new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_common_expenses, new_annual_expenses,
                                                              current_state_tax_rate, spending_increase_percentage, new_state_tax_rate, current_monthly_common_expenses)
        display_charts(current_annual_house_payment, current_total_property_tax, current_total_state_tax, current_annual_common_expenses, new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_common_expenses)

        excel_report = create_excel_report(results_df, breakdown_df, detailed_calculations)
        if excel_report:
            st.download_button(label="Download Report", data=excel_report, file_name="salary_comparison_report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    main()
