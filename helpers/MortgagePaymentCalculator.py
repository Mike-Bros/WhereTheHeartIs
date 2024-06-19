import matplotlib.pyplot as plt
import ipywidgets as widgets


class Calculator:
    @staticmethod
    def calculate_mortgage_payments(home_price, down_payment_percent, loan_term_years, interest_rate_exact,
                                    interest_rate_start, interest_rate_end, interest_rate_step, cash_savings,
                                    moving_cost, closing_cost_estimation=0.03):
        # Calculate the loan amount
        down_payment = home_price * (down_payment_percent / 100)
        loan_amount = home_price - down_payment
        loan_term_months = loan_term_years * 12
        monthly_interest_rate = (interest_rate_exact / 100) / 12
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / (
                (1 + monthly_interest_rate) ** loan_term_months - 1)

        # Initialize the data dictionary
        data = {
            'Home Price': home_price,
            'Down Payment': down_payment,
            'Loan Amount': loan_amount,
            'Down Payment Percent': down_payment_percent,
            'Loan Term (Years)': loan_term_years,
            'Interest Rate Exact': interest_rate_exact,
            'Interest Rate Start': interest_rate_start,
            'Interest Rate End': interest_rate_end,
            'Interest Rate Step': interest_rate_step,
            'Cash Savings': cash_savings,
            'Moving Costs': moving_cost,
            'Closing Cost Estimation': closing_cost_estimation,
            'Interest Rates': [],
            'PMI': 0,
            'Closing Costs': 0,
            'Total Cash Required': 0,
            'Remaining Cash Savings': 0,
            'Total Cost of Loan': 0
        }

        # Determine if PMI is required based on the loan-to-value ratio
        ltv_ratio = loan_amount / home_price
        pmi_ltv_dropoff = 0.80
        pmi_required = ltv_ratio > pmi_ltv_dropoff

        if pmi_required:
            current_balance = loan_amount
            pmi_rate = 0.01  # PMI rate is typically about 1% of the loan amount per year
            pmi_months = 0
            total_pmi_paid = 0

            while ltv_ratio > pmi_ltv_dropoff:
                # Calculate interest and principal for the current month from the payment
                interest = current_balance * (monthly_interest_rate / 12)
                principal = monthly_payment - interest - (current_balance * pmi_rate / 12)

                # Update the loan amount
                current_balance -= principal
                current_ltv = current_balance / home_price

                # Add the PMI payment to the total
                total_pmi_paid += current_balance * pmi_rate / 12

                # Check if the LTV ratio has dropped below the threshold
                if current_ltv <= pmi_ltv_dropoff:
                    break

                # Increment the number of months
                pmi_months += 1

            data['PMI Dropoff Months'] = pmi_months
            data['PMI Total Paid'] = total_pmi_paid
            pmi_payment = loan_amount * pmi_rate / 12
            data['PMI'] = pmi_payment
            data['PMI Dropoff Ratio'] = current_ltv
        else:
            data['PMI Dropoff Months'] = 0
            data['PMI Total Paid'] = 0

        # Calculate property tax
        assessed_value = home_price
        property_tax_rate = 0.0123
        property_tax = assessed_value * property_tax_rate / 12
        data['Property Tax'] = property_tax

        # Calculate insurance
        insurance = 1915 / 12
        data['Insurance'] = insurance

        # Calculate payments for the exact interest rate
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / (
                (1 + monthly_interest_rate) ** loan_term_months - 1) + (pmi_payment if pmi_required else 0)
        data['Interest Rates'].append(
            {'Interest Rate': interest_rate_exact, 'Monthly Payment': monthly_payment, 'Is Exact Rate': True})

        # Calculate payments for each interest rate in the range
        interest_rate = interest_rate_start
        while interest_rate <= interest_rate_end:
            monthly_interest_rate = (interest_rate / 100) / 12
            monthly_payment = (loan_amount * (
                    monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) /
                               ((1 + monthly_interest_rate) ** loan_term_months - 1) +
                               (pmi_payment if pmi_required else 0))
            data['Interest Rates'].append(
                {'Interest Rate': interest_rate, 'Monthly Payment': monthly_payment, 'Is Exact Rate': False})
            interest_rate += interest_rate_step

        # Calculate closing costs
        closing_costs = closing_cost_estimation * home_price
        data['Closing Costs'] = closing_costs

        # Calculate the total cash required to close
        total_cash_required = down_payment + closing_costs + moving_cost + property_tax + insurance
        data['Total Cash Required'] = total_cash_required

        # Calculate the remaining cash savings after closing
        remaining_cash_savings = cash_savings - total_cash_required
        data['Remaining Cash Savings'] = remaining_cash_savings

        # Calculate the total cost of the loan
        total_cost_of_loan = monthly_payment * loan_term_months
        data['Total Cost of Loan'] = total_cost_of_loan

        return data


class Plotter:
    @staticmethod
    def construct_mortgage_payment_plot(ax, data):
        # Extracting data for plotting
        interest_rates = [entry['Interest Rate'] for entry in data['Interest Rates']]
        payments = [entry['Monthly Payment'] for entry in data['Interest Rates']]
        exact_rates = [entry['Interest Rate'] for entry in data['Interest Rates'] if entry['Is Exact Rate']]
        exact_payments = [entry['Monthly Payment'] for entry in data['Interest Rates'] if entry['Is Exact Rate']]

        # Plot projected payments with markers
        ax.plot(interest_rates, payments, label='Projected Payments', marker='o', linestyle='', color='blue')

        # Highlight the exact interest rate if it exists with a distinct marker
        if exact_rates:
            ax.scatter(exact_rates, exact_payments, color='red', s=100, zorder=5, label='Exact Rate',
                       edgecolors='black')

        # Add annotation with array to the exact interest rates plotted
        for i, rate in enumerate(exact_rates):
            ax.annotate(f"${payments[i]:.2f}\n{rate}%", (rate, payments[i]), textcoords="offset points",
                        xytext=(15, -50),
                        ha='center', arrowprops=dict(arrowstyle='->', lw=1.5))

        # Add annotations for all interest rates plotted
        for i, rate in enumerate(interest_rates):
            if rate not in exact_rates:
                ax.annotate(f"${payments[i]:.2f}\n{rate}%", (rate, payments[i]), textcoords="offset points",
                            xytext=(0, 10),
                            ha='center')

        # Set titles and labels
        ax.set_title('Mortgage Payments by Interest Rate', fontsize=16, fontweight='bold')
        ax.set_xlabel('Interest Rate (%)')
        ax.set_ylabel('Monthly Mortgage Payment ($)')
        ax.grid(True)
        ax.legend()

    @staticmethod
    def construct_summary_graphs(data):
        # Visualize the data not in the Mortgage Payments by Interest Rate plot
        fig, ax = plt.subplots(4, 2, figsize=(15, 15))
        fig.subplots_adjust(hspace=0.4)  # Add vertical space between rows
        fig.suptitle('Mortgage Payment Calculator Summary', fontsize=20)

        # Show the summary of inputs in the first row
        left_summary = ax[0, 0]
        right_summary = ax[0, 1]
        left_summary.axis('off')
        right_summary.axis('off')
        left_summary.set_title('Input Summary', fontsize=16, fontweight='bold')
        right_summary.set_title('Graph Input Summary', fontsize=16, fontweight='bold')

        # Data for table in left_summary
        left_data = [
            ["Home Price", f"${data['Home Price']:,}"],
            ["Down Payment", f"{data['Down Payment Percent']}%"],
            ["Loan Term", f"{data['Loan Term (Years)']} years"],
            ["Loan Interest Rate", f"{data['Interest Rate Exact']}%"],
            ["Cash Savings", f"${data['Cash Savings']:,}"],
            ["Moving Cost", f"${data['Moving Costs']:,}"]
        ]
        table_left = left_summary.table(cellText=left_data, colLabels=["Label", "Value"], loc='center')
        table_left.auto_set_font_size(False)
        table_left.set_fontsize(10)
        table_left.scale(1, 1.5)
        for key, cell in table_left.get_celld().items():
            cell.set_fontsize(10)
            if key[0] == 0:
                cell.set_fontsize(12)
                cell.set_text_props(ha="center", weight="bold")
            else:
                if key[1] == 0:  # First column (Label) left aligned
                    cell.set_text_props(ha="left")
                else:  # Second column (Value) right aligned
                    cell.set_text_props(ha="center")

        # Data for table in right_summary
        right_data = [
            ["Payment/Rate Graph Start", f"{data['Interest Rate Start']}%"],
            ["Payments/Rate Graph End", f"{data['Interest Rate End']}%"],
            ["Payments/Rate Graph Step", f"{data['Interest Rate Step']}%"]
        ]
        table_right = right_summary.table(cellText=right_data, colLabels=["Label", "Value"], loc='center')
        table_right.auto_set_font_size(False)
        table_right.set_fontsize(10)
        table_right.scale(1, 1.5)
        for key, cell in table_right.get_celld().items():
            cell.set_fontsize(10)
            if key[0] == 0:
                cell.set_fontsize(12)
                cell.set_text_props(ha="center", weight="bold")
            else:
                if key[1] == 0:  # First column (Label) left aligned
                    cell.set_text_props(ha="left")
                else:  # Second column (Value) right aligned
                    cell.set_text_props(ha="center")

        # Show pie chart of monthly mortgage principal and interest payment, PMI, taxes, and insurance
        total_monthly_cost_breakdown = [
            data['Interest Rates'][0]['Monthly Payment'] - data['PMI'],
            data['PMI'], data['Property Tax'], data['Insurance']
        ]
        total_monthly_cost = sum(total_monthly_cost_breakdown)
        total_monthly_cost_breakdown_labels = ['Principal & Interest', 'PMI', 'Property Tax', 'Insurance']
        total_monthly_cost_breakdown_colors = ['blue', 'green', 'red', 'purple']
        monthly_cost = ax[1, 0]
        slices, texts, autotexts = monthly_cost.pie(total_monthly_cost_breakdown,
                                                    labels=total_monthly_cost_breakdown_labels,
                                                    textprops={'fontsize': 8, 'style': 'italic', 'weight': 'bold'},
                                                    autopct=lambda pct: "{:.1f}%".format(pct),
                                                    colors=total_monthly_cost_breakdown_colors)
        monthly_cost.set_title(f"Total Monthly Housing Cost: ${total_monthly_cost:,.2f}", fontsize=16,
                               fontweight='bold')
        monthly_cost.axis('equal')
        monthly_cost.grid(False)
        for autotext, value in zip(autotexts, total_monthly_cost_breakdown):
            pct_value = float(autotext.get_text().replace('%', ''))
            new_text = f"${value:,.2f} | {pct_value:.1f}%"
            autotext.set_text(new_text)

        # Show the construct_mortgage_payment_plot in the next row
        mortgage_payment_plot = ax[1, 1]
        Plotter.construct_mortgage_payment_plot(mortgage_payment_plot, data)

        # Compare the total cost of the loan, loan amount, and home price
        loan_comparison = ax[2, 0]
        loan_comparison.bar(['Total Cost of Loan', 'Home Price', 'Loan Amount'],
                            [data['Total Cost of Loan'], data['Home Price'], data['Loan Amount']],
                            color=['blue', 'green', 'red'])
        loan_comparison.set_title('Loan Cost Comparison', fontsize=16, fontweight='bold')
        loan_comparison.set_ylabel('Amount ($)')
        loan_comparison.grid(False)
        for i, value in enumerate([data['Total Cost of Loan'], data['Home Price'], data['Loan Amount']]):
            loan_comparison.annotate(f"${value:,.2f}", (i, value), textcoords="offset points", xytext=(0, -15),
                                     ha='center')

        # Show the total cash required in a pie chart
        total_cash = ax[2, 1]
        slices, texts, autotexts = total_cash.pie([data['Down Payment'], data['Closing Costs'], data['Moving Costs']],
                                                  labels=['Down Payment', 'Closing Costs', 'Moving Costs'],
                                                  textprops={'fontsize': 8, 'style': 'italic', 'weight': 'bold'},
                                                  autopct=lambda pct: "{:.1f}%".format(pct),
                                                  colors=['blue', 'green', 'red'], )
        total_cash.set_title(f"Total Cash Required to Close: ${data['Total Cash Required']:,.0f}", fontsize=16,
                             fontweight='bold')
        total_cash.axis('equal')
        total_cash.grid(False)
        for autotext, value in zip(autotexts, [data['Down Payment'], data['Closing Costs'], data['Moving Costs']]):
            pct_value = float(autotext.get_text().replace('%', ''))
            new_text = f"${value:,.0f} | {pct_value:.1f}%"
            autotext.set_text(new_text)

        # Visualize PMI data
        pmi_costs = ax[3, 0]
        pmi_costs.bar(['PMI Total Paid', 'PMI Monthly'],
                      [data['PMI Total Paid'], data['PMI']],
                      color=['blue', 'green'])
        pmi_costs.set_title('PMI Costs', fontsize=16, fontweight='bold')
        pmi_costs.set_ylabel('Amount ($)')
        pmi_costs.grid(False)
        max_value = max(data['PMI Total Paid'], data['PMI'])
        for i, value in enumerate([data['PMI Total Paid'], data['PMI']]):
            if value < max_value * 0.1:
                pmi_costs.annotate(f"${value:,.2f}", (i, value), textcoords="offset points", xytext=(0, 10),
                                   ha='center')
            else:
                pmi_costs.annotate(f"${value:,.2f}", (i, value), textcoords="offset points", xytext=(0, -15),
                                   ha='center')

        misc_info = ax[3, 1]
        misc_info.axis('off')
        misc_info.set_title('Additional Information', fontsize=16, fontweight='bold')
        misc_data = [
            ["PMI Dropoff Ratio", f"{data['PMI Dropoff Ratio']:.2f}"],
            ["PMI Dropoff Months", f"{data['PMI Dropoff Months']}"],
            ["Remaining Cash Savings", f"${data['Remaining Cash Savings']:,}"]
        ]
        table_misc = misc_info.table(cellText=misc_data, colLabels=["Label", "Value"], loc='center')
        table_misc.auto_set_font_size(False)
        table_misc.set_fontsize(10)
        table_misc.scale(1, 1.5)
        for key, cell in table_misc.get_celld().items():
            cell.set_fontsize(10)
            if key[0] == 0:
                cell.set_fontsize(12)
                cell.set_text_props(ha="center", weight="bold")
            else:
                if key[1] == 0:
                    cell.set_text_props(ha="left")
                else:
                    cell.set_text_props(ha="center")

        # Return the figure and axis objects for further manipulation
        return fig, ax
