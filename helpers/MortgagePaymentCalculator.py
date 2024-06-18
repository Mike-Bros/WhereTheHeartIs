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
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / ((1 + monthly_interest_rate) ** loan_term_months - 1)

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
            # monthly_payment += loan_amount * pmi_rate / 12  # Add PMI to the monthly payment
            pmi_payment = loan_amount * pmi_rate / 12
            data['PMI'] = pmi_payment
            data['PMI Dropoff Ratio'] = current_ltv
        else:
            data['PMI Dropoff Months'] = 0
            data['PMI Total Paid'] = 0

        # Calculate property tax
        # 1.23% is Minneapolis average property tax rate
        assessed_value = home_price
        property_tax_rate = 0.0123
        property_tax = assessed_value * property_tax_rate / 12
        data['Property Tax'] = property_tax

        # Calculate insurance
        # National average is $1,915 per year
        insurance = 1915 / 12
        data['Insurance'] = insurance

        # Calculate payments for the exact interest rate
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / (
                (1 + monthly_interest_rate) ** loan_term_months - 1) + (pmi_payment if pmi_required else 0)
        # Store the exact interest rate with a True flag in the dictionary1
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
            # Store each interest rate with a False flag in the dictionary
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
            # annotate with $15.23|5% and an arrow pointing to the exact rate
            ax.annotate(f"${payments[i]:.2f}\n{rate}%", (rate, payments[i]), textcoords="offset points",
                        xytext=(15, -50),
                        ha='center', arrowprops=dict(arrowstyle='->', lw=1.5))

        # Add annotations for the all interest rates plotted
        for i, rate in enumerate(interest_rates):
            if rate not in exact_rates:
                # annotate with $15.23|5%
                ax.annotate(f"${payments[i]:.2f}\n{rate}%", (rate, payments[i]), textcoords="offset points",
                            xytext=(0, 10),
                            ha='center')

        # Set titles and labels
        ax.set_title('Mortgage Payments by Interest Rate')
        ax.set_xlabel('Interest Rate (%)')
        ax.set_ylabel('Monthly Mortgage Payment ($)')
        ax.grid(True)
        ax.legend()

    @staticmethod
    def construct_summary_graphs(data):
        # Visualize the data not in the Mortgage Payments by Interest Rate plot

        # Show the data in a bar chart
        fig, ax = plt.subplots(3, 2, figsize=(15, 15))
        fig.suptitle('Mortgage Payment Calculator Summary', fontsize=20)
        # First row has two plots side by side
        # Second row has two plots side by side

        # Show pie chart of monthly mortgage principal and interest paynt, PMI, taxes, and insurance for total monthly housing cos
        total_monthly_cost_breakdown = [data['Interest Rates'][0]['Monthly Payment']-data['PMI'], data['PMI'], data['Property Tax'],
                                        data['Insurance']]
        total_monthly_cost = sum(total_monthly_cost_breakdown)
        total_monthly_cost_breakdown_labels = ['Principal & Interest', 'PMI', 'Property Tax', 'Insurance']
        total_monthly_cost_breakdown_colors = ['blue', 'green', 'red', 'purple']
        monthly_cost = ax[0, 0]
        slices, texts, autotexts = monthly_cost.pie(total_monthly_cost_breakdown,
                                                    labels=total_monthly_cost_breakdown_labels,
                                                    autopct=lambda pct: "{:.1f}%".format(pct),
                                                    colors=total_monthly_cost_breakdown_colors)
        monthly_cost.set_title(f"Total Monthly Housing Cost: ${total_monthly_cost:,.2f}")
        monthly_cost.axis('equal')
        monthly_cost.grid(False)
        # Modify autotexts for the second pie chart
        for autotext, value in zip(autotexts, total_monthly_cost_breakdown):
            pct_value = float(autotext.get_text().replace('%', ''))
            new_text = f"${value:,.2f} | {pct_value:.1f}%"
            autotext.set_text(new_text)

        # Show the construct_mortgage_payment_plot in the last subplot
        mortgage_payment_plot = ax[0, 1]
        Plotter.construct_mortgage_payment_plot(mortgage_payment_plot, data)

        # Compare the total cost of the loan, to loan amount and home price
        loan_comparison = ax[1, 0]
        loan_comparison.bar(['Total Cost of Loan', 'Home Price', 'Loan Amount', ],
                            [data['Total Cost of Loan'], data['Home Price'], data['Loan Amount']],
                            color=['blue', 'green', 'red'])
        loan_comparison.set_title('Loan Cost Comparison')
        loan_comparison.set_ylabel('Amount ($)')
        loan_comparison.grid(False)
        # Add annotations to the bar chart for the exact values
        for i, value in enumerate([data['Total Cost of Loan'], data['Home Price'], data['Loan Amount']]):
            loan_comparison.annotate(f"${value:,.2f}", (i, value), textcoords="offset points", xytext=(0, -15),
                                     ha='center')

        # Show the total cash required in a pie chart
        total_cash = ax[1, 1]
        slices, texts, autotexts = total_cash.pie([data['Down Payment'], data['Closing Costs'], data['Moving Costs']],
                                                  labels=['Down Payment', 'Closing Costs', 'Moving Costs'],
                                                  autopct=lambda pct: "{:.1f}%".format(pct),
                                                  colors=['blue', 'green', 'red'],
                                                  textprops={'fontsize': 10})
        total_cash.set_title(f"Total Cash Required to Close: ${data['Total Cash Required']:,.0f}")
        total_cash.axis('equal')
        # Modify autotexts to include absolute values alongside percentages
        for autotext, value in zip(autotexts, [data['Down Payment'], data['Closing Costs'], data['Moving Costs']]):
            pct_value = float(
                autotext.get_text().replace('%', ''))  # Extract the numerical value from the percentage text
            new_text = f"${value:,.0f} | {pct_value:.1f}%"
            autotext.set_text(new_text)

        # Visualize PMI data
        pmi_costs = ax[2, 0]
        pmi_costs.bar(['PMI Total Paid', 'PMI Monthly'],
                     [data['PMI Total Paid'], data['PMI']],
                     color=['blue', 'green'])
        pmi_costs.set_title('PMI Costs')
        pmi_costs.set_ylabel('Amount ($)')
        pmi_costs.grid(False)
        # Add annotations to the bar chart for the exact values
        max_value = max(data['PMI Total Paid'], data['PMI'])
        for i, value in enumerate([data['PMI Total Paid'], data['PMI']]):
            if value < max_value * 0.1:
                # If the value is less than 10% of the max value, place the annotation above the bar
                pmi_costs.annotate(f"${value:,.2f}", (i, value), textcoords="offset points", xytext=(0, 10),
                                  ha='center')
            else:
                # Otherwise, place the annotation inside the bar
                pmi_costs.annotate(f"${value:,.2f}", (i, value), textcoords="offset points", xytext=(0, -15),
                                  ha='center')

        misc_info = ax[2, 1]
        misc_info.axis('off')
        misc_info.set_title('Additional Information')
        misc_info.text(0, 0.9, f"PMI Dropoff Ratio: {data['PMI Dropoff Ratio']:.2f}")
        misc_info.text(0, 0.8, f"PMI Dropoff Months: {data['PMI Dropoff Months']}")
        misc_info.text(0, 0.7, f"Remaining Cash Savings: ${data['Remaining Cash Savings']:,.0f}")



        # Return the figure and axis objects for further manipulation
        return fig, ax


class WidgetHelpers:
    def __init__(self):
        self.calculator_widgets = self.create_mortgage_payment_calculator_widgets()
        self.graph_output = widgets.Output()

    @staticmethod
    def style_css():
        return """
        <style>
            .widget-label { width: 20ex !important; }
                .widget-slider { width: 60% !important; }
                .widget-button { width: 300px !important; margin: 10px 0px; }
                .widget-text { width: 300px !important; }
                .widget-select { width: 300px !important; }
                .widget-output { height: 100% !important; }
            </style>
            """

    @staticmethod
    def update_label(value, precision=2, prepend='', append=''):
        return f"{prepend}{value:.{precision}f}{append}"

    @staticmethod
    def on_value_change(change, label, config):
        label.value = WidgetHelpers.update_label(change['new'], config['precision'], config['prepend'],
                                                 config['append'])

    @staticmethod
    def create_slider(config):
        slider = widgets.FloatSlider(
            value=config['default_value'], min=config['min'], max=config['max'],
            step=config['step'], description=config['description'], readout=config['readout']
        )
        label = widgets.Label(
            WidgetHelpers.update_label(slider.value, config['precision'], config['prepend'], config['append']))
        slider.observe(lambda change: WidgetHelpers.on_value_change(change, label, config), names='value')
        return slider, label

    @staticmethod
    def create_mortgage_payment_calculator_widgets():
        slider_configs = {
            'home_price': {'value': None, 'default_value': 225000, 'min': 150000, 'max': 800000, 'step': 1000,
                           'description': 'Home Price', 'readout': False, 'precision': 0, 'prepend': '$', 'append': ''},
            'down_payment_percent': {'value': None, 'default_value': 5, 'min': 0, 'max': 30, 'step': 1,
                                     'description': 'Down Payment',
                                     'readout': False, 'precision': 2, 'prepend': '', 'append': '%'},
            'loan_term_years': {'value': None, 'default_value': 30, 'min': 15, 'max': 30, 'step': 15,
                                'description': 'Loan Term',
                                'readout': False, 'precision': 0, 'prepend': '', 'append': ' years'},
            'interest_rate_exact': {'value': None, 'default_value': 7.2, 'min': 2, 'max': 8, 'step': 0.01,
                                    'description': 'Interest Rate', 'readout': False, 'precision': 2, 'prepend': '',
                                    'append': '%'},
            'interest_rate_start': {'value': None, 'default_value': 2, 'min': 1, 'max': 4, 'step': 0.25,
                                    'description': 'Interest Range Start', 'readout': False, 'precision': 2,
                                    'prepend': '', 'append': '%'},
            'interest_rate_end': {'value': None, 'default_value': 8, 'min': 4, 'max': 10, 'step': 0.25,
                                  'description': 'Interest Range End', 'readout': False, 'precision': 2, 'prepend': '',
                                  'append': '%'},
            'interest_rate_step': {'value': None, 'default_value': 0.50, 'min': 0, 'max': 1, 'step': 0.25,
                                   'description': 'Interest Range Step', 'readout': False, 'precision': 2, 'prepend': '',
                                   'append': '%'},
            'cash_savings': {'value': None, 'default_value': 15000, 'min': 0, 'max': 80000, 'step': 500,
                             'description': 'Cash Savings', 'readout': False, 'precision': 0, 'prepend': '$',
                             'append': ''},
            'moving_cost': {'value': None, 'default_value': 1200, 'min': 0, 'max': 3000, 'step': 50,
                            'description': 'Moving Costs', 'readout': False, 'precision': 0, 'prepend': '$',
                            'append': ''},
        }

        widgets_dict = {}
        for key, config in slider_configs.items():
            slider, label = WidgetHelpers.create_slider(config)
            widgets_dict[key] = {'slider': slider, 'label': label}

        return widgets_dict

    def get_calculator_widgets(self):
        return self.calculator_widgets

    def get_graph_output_widgets(self):
        return self.graph_output
