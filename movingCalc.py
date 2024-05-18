import streamlit as st
import pandas as pd
import plotly.express as px

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

# Define the app
def main():
    st.title('Salary Comparison and Raise Calculator')
    
    st.header('Current Situation')
    current_salary = st.number_input('Enter your current net annual salary ($)', min_value=0, step=1000)
    current_monthly_house_payment = st.number_input('Enter your current monthly house payment ($)', min_value=0, step=100)
    current_annual_property_tax = st.number_input('Enter your current annual property tax ($)', min_value=0, step=100)
    current_state_tax_rate = st.number_input('Enter your current state tax rate (%)', min_value=0.0, max_value=100.0, step=0.01)

    st.header('New Situation')
    new_monthly_house_payment = st.number_input('Enter your new monthly house payment ($)', min_value=0, step=100)
    new_annual_property_tax = st.number_input('Enter your new annual property tax ($)', min_value=0, step=100)
    new_state_tax_rate = st.number_input('Enter your new state tax rate (%)', min_value=0.0, max_value=100.0, step=0.01)
    spending_increase_percentage = st.number_input('Enter the percentage increase in common spending categories (%)', min_value=0.0, max_value=100.0, step=0.01)

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
            'Amount ($)': [current_annual_expenses, new_annual_expenses, additional_expenses, required_new_salary, monthly_required_new_salary]
        }
        results_df = pd.DataFrame(results_data)
        st.table(results_df)

        # Display breakdown of additional expenses
        st.subheader('Breakdown of Additional Expenses')
        breakdown_data = {
            'Description': ['New Annual House Payment', 'New Annual Property Tax', 'New Annual State Tax', 'Increase in Common Spending Categories'],
            'Amount ($)': [new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_spending_increase]
        }
        breakdown_df = pd.DataFrame(breakdown_data)
        st.table(breakdown_df)

        # Display detailed calculations
        st.subheader('Detailed Calculations')
        st.write('**Current Situation:**')
        st.write(f' - Current Annual House Payment: {current_monthly_house_payment} * 12 = ${current_annual_house_payment:,.2f}')
        st.write(f' - Current Annual Property Tax: ${current_total_property_tax:,.2f}')
        st.write(f' - Current Annual State Tax: (${current_annual_house_payment:,.2f} + ${current_total_property_tax:,.2f}) * {current_state_tax_rate / 100:.2f} = ${current_total_state_tax:,.2f}')
        st.write(f' - Current Total Annual Expenses: ${current_annual_house_payment:,.2f} + ${current_total_property_tax:,.2f} + ${current_total_state_tax:,.2f} = ${current_annual_expenses:,.2f}')
        
        st.write('**New Situation:**')
        st.write(f' - New Annual House Payment: {new_monthly_house_payment} * 12 = ${new_annual_house_payment:,.2f}')
        st.write(f' - New Annual Property Tax: ${new_total_property_tax:,.2f}')
        st.write(f' - New Annual State Tax: (${new_annual_house_payment:,.2f} + ${new_total_property_tax:,.2f}) * {new_state_tax_rate / 100:.2f} = ${new_total_state_tax:,.2f}')
        st.write(f' - Increase in Common Spending Categories: (${new_annual_house_payment:,.2f} + ${new_total_property_tax:,.2f} + ${new_total_state_tax:,.2f}) * {spending_increase_percentage / 100:.2f} = ${new_spending_increase:,.2f}')
        st.write(f' - New Total Annual Expenses: ${new_annual_house_payment:,.2f} + ${new_total_property_tax:,.2f} + ${new_total_state_tax:,.2f} + ${new_spending_increase:,.2f} = ${new_annual_expenses:,.2f}')

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

if __name__ == "__main__":
    main()
