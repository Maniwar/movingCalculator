import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(layout="wide")

# Helper function to calculate annual expenses
def calculate_annual_expenses(monthly_payment, annual_property_tax, state_tax_rate, monthly_common_expenses, spending_increase_percentage, salary):
    annual_house_payment = monthly_payment * 12
    total_property_tax = annual_property_tax
    total_state_tax = salary * (state_tax_rate / 100)
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
        new_salary = st.number_input('Desired net annual salary ($)', min_value=0, step=1000, format='%d', key='new_salary')
        new_monthly_house_payment = st.number_input('Monthly house payment ($)', min_value=0, step=100, format='%d', key='new_monthly_house_payment')
        new_annual_property_tax = st.number_input('Annual property tax ($)', min_value=0, step=100, format='%d', key='new_annual_property_tax')
        new_state_tax_rate = st.number_input('State tax rate (%)', min_value=0.0, max_value=100.0, step=0.01, format='%.2f', key='new_state_tax_rate')
        spending_increase_percentage = st.number_input('Increase in spending (%) for current monthly household and utility expenses', min_value=0.0, max_value=100.0, step=0.01, format='%.2f', key='spending_increase_percentage')
    return current_salary, current_monthly_house_payment, current_annual_property_tax, current_state_tax_rate, current_monthly_common_expenses, new_salary, new_monthly_house_payment, new_annual_property_tax, new_state_tax_rate, spending_increase_percentage

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
                                  new_monthly_house_payment, new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_common_expenses, new_annual_expenses, current_state_tax_rate, spending_increase_percentage, new_state_tax_rate, current_monthly_common_expenses, current_salary, required_new_salary):
    st.subheader('Detailed Calculations')
    detailed_calculations = {
        'Calculation Steps': [
            f' - Current Annual House Payment: {current_monthly_house_payment} * 12 = ${current_annual_house_payment:,.2f}',
            f' - Current Annual Property Tax: ${current_total_property_tax:,.2f}',
            f' - Current Annual State Tax: ${current_salary:,.2f} * {current_state_tax_rate / 100:.2f} = ${current_total_state_tax:,.2f}',
            f' - Current Total Annual Expenses: ${current_annual_house_payment:,.2f} + ${current_total_property_tax:,.2f} + ${current_total_state_tax:,.2f} + ${current_annual_common_expenses:,.2f} = ${current_annual_expenses:,.2f}',
            f' - New Annual House Payment: {new_monthly_house_payment} * 12 = ${new_annual_house_payment:,.2f}',
            f' - New Annual Property Tax: ${new_total_property_tax:,.2f}',
            f' - New Annual State Tax: ${required_new_salary:,.2f} * {new_state_tax_rate / 100:.2f} = ${new_total_state_tax:,.2f}',
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
    st.divider()
    new_expense_proportion_df = pd.DataFrame(new_expense_proportion_data)
    fig = px.pie(new_expense_proportion_df, values='New Annual ($)', names='Category', title='Proportion of Each Category in New Annual Expenses')
    st.plotly_chart(fig)

# Main function to run the app
def main():
    st.title('Salary Comparison and Raise Calculator')
    
    current_salary, current_monthly_house_payment, current_annual_property_tax, current_state_tax_rate, current_monthly_common_expenses, new_salary, new_monthly_house_payment, new_annual_property_tax, new_state_tax_rate, spending_increase_percentage = display_inputs()

    if st.button('Calculate Required Salary'):
        try:
            current_annual_expenses, current_annual_house_payment, current_total_property_tax, current_total_state_tax, current_annual_common_expenses, _ = calculate_annual_expenses(current_monthly_house_payment, current_annual_property_tax, current_state_tax_rate, current_monthly_common_expenses, 0, current_salary)
            new_annual_expenses, new_annual_house_payment, new_total_property_tax, new_total_state_tax, _, new_common_expenses = calculate_annual_expenses(new_monthly_house_payment, new_annual_property_tax, new_state_tax_rate, current_monthly_common_expenses, spending_increase_percentage, new_salary)
            
            additional_expenses = new_annual_expenses - current_annual_expenses
            required_new_salary = current_salary + additional_expenses
            monthly_required_new_salary = required_new_salary / 12
            
            if current_salary == 0:
                raise ValueError("Current salary cannot be zero.")
                
            percentage_increase = ((required_new_salary - current_salary) / current_salary) * 100

            # Include Font Awesome CSS
            st.markdown(
                """
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
                """,
                unsafe_allow_html=True
            )
            
            # Add custom styles
            st.markdown(
                """
                <style>
                .result-box {
                    border: 2px solid red;
                    padding: 10px;
                    border-radius: 10px;
                    text-align: center;
                    background-color: #ffebeb;
                }
                .result-box h2 {
                    color: red;
                    font-weight: bold;
                }
                .result-box .fa-icon {
                    font-size: 24px;
                    margin-right: 10px;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            
            # Display the results prominently
            st.markdown(
                f"""
                <div class="result-box">
                    <h2><i class="fas fa-dollar-sign fa-icon"></i>Needed Annual Salary: ${required_new_salary:,.2f}</h2>
                    <h2><i class="fas fa-calendar-alt fa-icon"></i>Needed Monthly Salary: ${monthly_required_new_salary:,.2f}</h2>
                    <h2><i class="fas fa-percentage fa-icon"></i>Percentage Increase: {percentage_increase:.2f}%</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.divider()
            
            results_df = display_results(current_annual_expenses, new_annual_expenses, additional_expenses)
            breakdown_df = display_breakdown(new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_common_expenses)

            st.divider()
            
            detailed_calculations = display_detailed_calculations(current_monthly_house_payment, current_annual_house_payment, current_total_property_tax, current_total_state_tax, current_annual_expenses, current_annual_common_expenses,
                                                                  new_monthly_house_payment, new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_common_expenses, new_annual_expenses,
                                                                  current_state_tax_rate, spending_increase_percentage, new_state_tax_rate, current_monthly_common_expenses, current_salary, required_new_salary)
            
            st.divider()
            
            display_charts(current_annual_house_payment, current_total_property_tax, current_total_state_tax, current_annual_common_expenses, new_annual_house_payment, new_total_property_tax, new_total_state_tax, new_common_expenses)
    
            excel_report = create_excel_report(results_df, breakdown_df, detailed_calculations)
            if excel_report:
                st.download_button(label="Download Report", data=excel_report, file_name="salary_comparison_report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                
        except ValueError as e:
            st.error(f"Error: {e}")
        except ZeroDivisionError:
            st.error("Current salary cannot be zero. Please enter a valid current salary.")

    # Adding a divider and the legal disclaimer
    st.divider()
    expander = st.expander("Legal and Data Privacy Statement", expanded=False)
    with expander:
        st.markdown(
        """
<p style="font-size:14px;">Legal Statement</p>
<p style="font-size:14px;">
This application ("App") is provided "as is" without any warranties, express or implied. The information provided by the App is intended to be used for informational purposes only and not as a substitute for professional advice, diagnosis, or treatment. Always seek the advice of your qualified financial advisor with any questions you may have regarding your finances. Never disregard professional advice or delay in seeking it because of something you have read on the App.
</p>
<p style="font-size:14px;">
While we strive to provide accurate information, we make no representation and assume no responsibility for the accuracy of information on or available through the App.
</p>
<p style="font-size:14px;">
The App does not endorse any specific product, service, or treatment. The use of any information provided by the App is solely at your own risk. The App and its owners or operators are not liable for any direct, indirect, punitive, incidental, special or consequential damages that result from the use of, or inability to use, this site.
</p>
<p style="font-size:14px;">
Certain state laws do not allow limitations on implied warranties or the exclusion or limitation of certain damages. If these laws apply to you, some or all of the above disclaimers, exclusions, or limitations may not apply to you, and you might have additional rights.
</p>
<p style="font-size:14px;">
By using this App, you agree to abide by the terms of this legal statement.
</p>
<p style="font-size:14px;">Data Privacy Statement</p>
<p style="font-size:14px;">
This application ("App") respects your privacy. This statement outlines our practices regarding your data.
</p>
<p style="font-size:14px;">
<b>Information Collection:</b> The only data the App collects is the information you enter when you use the App. We do not collect any personal data, including contact information.
</p>
<p style="font-size:14px;">
<b>Information Usage:</b> Your input data is used solely to provide the App's services, specifically to calculate and compare salary requirements. All data is processed in real time and is not stored on our servers or databases beyond this purpose.
</p>
<p style="font-size:14px;">
<b>Information Sharing:</b> We do not share your data with any third parties.
</p>
<p style="font-size:14px;">
<b>User Rights:</b> As we do not store your data beyond the current session, we cannot facilitate requests for data access, correction, or deletion.
</p>
<p style="font-size:14px;">
<b>Security Measures:</b> We implement security measures to protect your data during transmission, but no system is completely secure. We cannot fully eliminate the risks associated with data transmission.
</p>
<p style="font-size:14px;">
<b>Changes to this Policy:</b> Any changes to this data privacy statement will be updated on the App.
</p>
<p style="font-size:14px;">
<b>Ownership of Data:</b> All output data generated by the App, including but not limited to the analysis and calculations, belongs to the owner of the App. The owner retains the right to use, reproduce, distribute, display, and perform the data in any manner and for any purpose. The user acknowledges and agrees that any information input into the App may be used in this way, subject to the limitations set out in the Data Privacy Statement.
</p>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
