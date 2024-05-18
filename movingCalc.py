import streamlit as st

# Helper function to calculate annual expenses
def calculate_annual_expenses(monthly_payment, annual_property_tax, state_tax_rate, spending_increase_percentage):
    # Annual house payment
    annual_house_payment = monthly_payment * 12
    # Total annual property tax
    total_property_tax = annual_property_tax
    # Total state tax
    total_state_tax = (annual_house_payment + total_property_tax) * (state_tax_rate / 100)
    # Increase in common spending categories
    spending_increase = annual_house_payment * (spending_increase_percentage / 100)
    # Total annual expenses
    total_annual_expenses = annual_house_payment + total_property_tax + total_state_tax + spending_increase
    return total_annual_expenses

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
        current_annual_expenses = calculate_annual_expenses(current_monthly_house_payment, current_annual_property_tax, current_state_tax_rate, 0)
        new_annual_expenses = calculate_annual_expenses(new_monthly_house_payment, new_annual_property_tax, new_state_tax_rate, spending_increase_percentage)

        # Calculate the required raise
        additional_expenses = new_annual_expenses - current_annual_expenses
        required_new_salary = current_salary + additional_expenses

        st.subheader('Results')
        st.write(f'Current Annual Expenses: ${current_annual_expenses:,.2f}')
        st.write(f'New Annual Expenses: ${new_annual_expenses:,.2f}')
        st.write(f'Additional Expenses: ${additional_expenses:,.2f}')
        st.write(f'Needed Annual Salary to Offset Additional Expenses: ${required_new_salary:,.2f}')
        
        st.subheader('Breakdown of Additional Expenses')
        st.write(f'New Monthly House Payment: ${new_monthly_house_payment * 12:,.2f}')
        st.write(f'New Annual Property Tax: ${new_annual_property_tax:,.2f}')
        st.write(f'New State Tax: ${(new_annual_expenses - new_monthly_house_payment * 12 - new_annual_property_tax) * (new_state_tax_rate / 100):,.2f}')
        st.write(f'Increase in Common Spending Categories: ${new_annual_expenses * (spending_increase_percentage / 100):,.2f}')

if __name__ == "__main__":
    main()
