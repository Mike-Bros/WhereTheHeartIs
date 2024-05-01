import matplotlib.pyplot as plt
import ipywidgets as widgets


class Calculator:

    @staticmethod
    def calculate_mortgage_payments(home_price, down_payment_percent, loan_term_years, interest_rate_exact,
                                    interest_rate_start, interest_rate_end, interest_rate_step):
        # Calculate the loan amount
        down_payment = home_price * (down_payment_percent / 100)
        loan_amount = home_price - down_payment

        # Initialize the data dictionary
        data = {}

        # Calculate payments for the exact interest rate
        monthly_interest_rate = (interest_rate_exact / 100) / 12
        loan_term_months = loan_term_years * 12
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / (
                (1 + monthly_interest_rate) ** loan_term_months - 1)
        # Store the exact interest rate with a True flag in the dictionary
        data[interest_rate_exact] = {'Monthly Payment': monthly_payment, 'Is Exact Rate': True}

        # Calculate payments for each interest rate   in the range
        interest_rate = interest_rate_start
        while interest_rate <= interest_rate_end:
            monthly_interest_rate = (interest_rate / 100) / 12
            monthly_payment = loan_amount * (
                    monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months) / (
                                      (1 + monthly_interest_rate) ** loan_term_months - 1)
            # Store each interest rate with a False flag in the dictionary
            data[interest_rate] = {'Monthly Payment': monthly_payment, 'Is Exact Rate': False}
            interest_rate += interest_rate_step

        return data


class Plotter:

    @staticmethod
    def construct_mortgage_payment_plot(results):
        # Extracting data for plotting
        interest_rates = list(results.keys())
        payments = [results[rate]['Monthly Payment'] for rate in interest_rates]
        exact_rates = [rate for rate in interest_rates if results[rate]['Is Exact Rate']]
        exact_payments = [results[rate]['Monthly Payment'] for rate in exact_rates]

        # Create figure and axis objects
        fig, ax = plt.subplots(figsize=(10, 6))

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
                .widget-output { height: 340px !important; }
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
            'home_price': {'value': None, 'default_value': 250000, 'min': 150000, 'max': 300000, 'step': 5000,
                           'description': 'Home Price', 'readout': False, 'precision': 0, 'prepend': '$', 'append': ''},
            'down_payment_percent': {'value': None, 'default_value': 5, 'min': 0, 'max': 30, 'step': 1,
                                     'description': 'Down Payment',
                                     'readout': False, 'precision': 2, 'prepend': '', 'append': '%'},
            'loan_term_years': {'value': None, 'default_value': 30, 'min': 15, 'max': 30, 'step': 5,
                                'description': 'Loan Term',
                                'readout': False, 'precision': 0, 'prepend': '', 'append': ' years'},
            'interest_rate_exact': {'value': None, 'default_value': 7.38, 'min': 2, 'max': 8, 'step': 0.01,
                                    'description': 'Interest Rate', 'readout': False, 'precision': 2, 'prepend': '',
                                    'append': '%'},
            'interest_rate_start': {'value': None, 'default_value': 2, 'min': 1, 'max': 4, 'step': 0.25,
                                    'description': 'Interest Rate Start', 'readout': False, 'precision': 2,
                                    'prepend': '', 'append': '%'},
            'interest_rate_end': {'value': None, 'default_value': 8, 'min': 4, 'max': 10, 'step': 0.25,
                                  'description': 'Interest Rate End', 'readout': False, 'precision': 2, 'prepend': '',
                                  'append': '%'},
            'interest_rate_step': {'value': None, 'default_value': 0.50, 'min': 0, 'max': 1, 'step': 0.25,
                                   'description': 'Interest Rate Step', 'readout': False, 'precision': 2, 'prepend': '',
                                   'append': '%'},
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
