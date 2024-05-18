import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(layout="wide")

# Helper function to calculate annual expenses
def calculate_annual_expenses(monthly_payment, annual_property_tax, state_tax_rate, spending_increase_percentage):
    # Annual house payment
    annual_house_payment = monthly_payment * 12
    # Total annual property tax
    total_property_tax = annual_property_tax
    # Total state tax
    total_state_tax = (annual_house_payment + total_property_tax) * (state_tax_rate / 100)
    # Increase in common spending categories
    spending_increase = (annual_house_payment + total_property_tax + total_state_tax) * (spending_increase_percentage / 100)
    # Total annual expenses
    total_annual_expenses = annual_house_payment + total_property_tax + total_state_tax + spending_increase
    return total_annual_expenses, annual_house_payment, total_property_tax, total_state_tax, spending_increase

# Function to create a downloadable Excel file
def create_excel_report(results_df, breakdown_df, detailed_calculations):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
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

    writer.save()
    output.seek(0)
    return output

# Define the app
def main():
    st.title('Salary Comparison and Raise Calculator')

    col1, col2 = st.columns(2)
    
    with col1:
        st.header('Current Situation')
        current_salary = st.number_input('Net annual salary ($)', min_value=0, step=1000, format='%d')
        current_monthly_house_payment = st.number_input('Monthly house payment ($)', min_value=0, step=100, format='%d')
        current_annual_property_tax = st.number_input('Annual property tax ($)', min_value=0, step=100, format='%d')
        current_state_tax_rate = st.number_input('State tax rate (%)', min_value=0.0, max_value=100.0, step=0.01, format='%.2f')

    with col2:
        st.header('New Situation')
        new_monthly_house_payment = st.number_input('Monthly house payment ($)', min_value=0, step=100, format='%d')
        new_annual_property_tax = st.number_input('Annual property tax ($)', min_value=0, step=100, format='%d')
        new_state_tax_rate = st.number_input('State tax rate (%)', min_value=0.0, max_value=100.0, step=0.01, format='%.2f')
        spending_increase_percentage = st.number_input('Increase in spending (%)', min_value=0.0, max_value=100.0, step=0.01, format='%.2f')

    if st.button('Calculate Required Salary'):
        # Calculate annual expenses for current and new situations
        current_annual_expenses, current_annual_house_payment, current_total_property_tax, current_total_state_tax, current_spending_increase = calculate_annual_expenses(current_monthly_house_payment, current_annual_property_tax, current_state_tax_rate, 0)
        new_annual_expenses, new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_spending_increase = calculate_annual_expenses(new_monthly_house_payment, new_annual_property_tax, new_state_tax_rate, spending_increase_percentage)

        # Calculate the required raise
        additional_expenses = new_annual_expenses - current_annual_expenses
        required_new_salary = current_salary + additional_expenses
        monthly_required_new_salary = required_new_salary / 12

        # Display results in tables
        st.subheader('Results')
        results_data = {
            'Description': ['Current Annual Expenses', 'New Annual Expenses', 'Additional Expenses', 'Needed Annual Salary', 'Needed Monthly Salary'],
            'Amount ($)': [f'{current_annual_expenses:,.2f}', f'{new_annual_expenses:,.2f}', f'{additional_expenses:,.2f}', f'{required_new_salary:,.2f}', f'{monthly_required_new_salary:,.2f}']
        }
        results_df = pd.DataFrame(results_data)
        st.table(results_df)

        # Display breakdown of additional expenses
        st.subheader('Breakdown of Additional Expenses')
        breakdown_data = {
            'Description': ['New Annual House Payment', 'New Annual Property Tax', 'New Annual State Tax', 'Increase in Common Spending Categories'],
            'Amount ($)': [f'{new_annual_house_payment:,.2f}', f'{new_total_property_tax:,.2f}', f'{new_total_state_tax:,.2f}', f'{new_spending_increase:,.2f}']
        }
        breakdown_df = pd.DataFrame(breakdown_data)
        st.table(breakdown_df)

        # Display detailed calculations
        st.subheader('Detailed Calculations')
        detailed_calculations = {
            'Calculation Steps': [
                f' - Current Annual House Payment: {current_monthly_house_payment} * 12 = ${current_annual_house_payment:,.2f}',
                f' - Current Annual Property Tax: ${current_total_property_tax:,.2f}',
                f' - Current Annual State Tax: (${current_annual_house_payment:,.2f} + ${current_total_property_tax:,.2f}) * {current_state_tax_rate / 100:.2f} = ${current_total_state_tax:,.2f}',
                f' - Current Total Annual Expenses: ${current_annual_house_payment:,.2f} + ${current_total_property_tax:,.2f} + ${current_total_state_tax:,.2f} = ${current_annual_expenses:,.2f}',
                f' - New Annual House Payment: {new_monthly_house_payment} * 12 = ${new_annual_house_payment:,.2f}',
                f' - New Annual Property Tax: ${new_total_property_tax:,.2f}',
                f' - New Annual State Tax: (${new_annual_house_payment:,.2f} + ${new_total_property_tax:,.2f}) * {new_state_tax_rate / 100:.2f} = ${new_total_state_tax:,.2f}',
                f' - Increase in Common Spending Categories: (${new_annual_house_payment:,.2f} + ${new_total_property_tax:,.2f} + ${new_total_state_tax:,.2f}) * {spending_increase_percentage / 100:.2f} = ${new_spending_increase:,.2f}',
                f' - New Total Annual Expenses: ${new_annual_house_payment:,.2f} + ${new_total_property_tax:,.2f} + ${new_total_state_tax:,.2f} + ${new_spending_increase:,.2f} = ${new_annual_expenses:,.2f}'
            ]
        }
        for calc in detailed_calculations['Calculation Steps']:
            st.write(calc)

        # Bar chart comparing current and new annual expenses by category
        st.subheader('Comparison of Current and New Annual Expenses')
        expense_comparison_data = {
            'Category': ['House Payment', 'Property Tax', 'State Tax', 'Spending Increase'],
            'Current Annual ($)': [current_annual_house_payment, current_total_property_tax, current_total_state_tax, current_spending_increase],
            'New Annual ($)': [new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_spending_increase]
        }
        expense_comparison_df = pd.DataFrame(expense_comparison_data)
        fig = px.bar(expense_comparison_df, x='Category', y=['Current Annual ($)', 'New Annual ($)'], barmode='group', title='Comparison of Current and New Annual Expenses by Category')
        st.plotly_chart(fig)

        # Pie chart showing the proportion of each category in the new annual expenses
        st.subheader('Proportion of Each Category in New Annual Expenses')
        new_expense_proportion_data = {
            'Category': ['House Payment', 'Property Tax', 'State Tax', 'Spending Increase'],
            'New Annual ($)': [new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_spending_increase]
        }
        new_expense_proportion_df = pd.DataFrame(new_expense_proportion_data)
        fig = px.pie(new_expense_proportion_df, values='New Annual ($)', names='Category', title='Proportion of Each Category in New Annual Expenses')
        st.plotly_chart(fig)

        # Create Excel report and provide download link
        excel_report = create_excel_report(results_df, breakdown_df, detailed_calculations)
        st.download_button(
            label="Download Report",
            data=excel_report,
            file_name="salary_comparison_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
