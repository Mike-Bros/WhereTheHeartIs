import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import matplotlib.pyplot as plt
import io
import base64
import os
from datetime import datetime
from helpers.MortgagePaymentCalculator import Calculator, Plotter

app = dash.Dash(__name__)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Mortgage Payment Calculator</title>
        <link rel="icon" href="/assets/logo.ico" type="image/x-icon">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
        {%metas%}
        {%css%}
    </head>
    <body>
        <div id="root">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


def fig_to_uri(fig):
    out_img = io.BytesIO()
    fig.savefig(out_img, format='png')
    out_img.seek(0)
    encoded = base64.b64encode(out_img.read()).decode('ascii')
    # Close fig to converse memory
    plt.close(fig)
    return 'data:image/png;base64,{}'.format(encoded)


def input_with_icon(id, icon_class, value, placeholder,
                    main_class="w-full md:w-1/2 px-2",
                    input_class="block w-full pl-10 border border-gray-300 rounded-md py-2 focus:outline-none "
                                "focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    label_class="block text-sm font-medium text-gray-700"):
    return html.Div([
        html.Label(placeholder, className=label_class),
        html.Div([
            html.Div([
                html.I(className=f"{icon_class} text-gray-500")
            ], className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"),
            dcc.Input(id=id, type='number', value=value,
                      className=input_class),
        ], className="relative mt-2 rounded-md shadow-sm")
    ], className=main_class)


# Define the layout of the app
app.layout = html.Div([
    html.Img(src=app.get_asset_url('logo.svg'), className="w-16 h-16 mx-auto mt-4"),
    html.H1('Mortgage Payment Calculator', className="text-2xl font-bold text-center mb-4"),
    html.Div([
        html.Div([
            input_with_icon('home-price', 'fas fa-dollar-sign', 215000, 'Home Price'),
            input_with_icon('down-payment', 'fas fa-percentage', 5, 'Down Payment')
        ], className="flex flex-wrap -mx-2 mb-4"),
        html.Div([
            input_with_icon('loan-term', 'fas fa-calendar-alt', 30, 'Loan Term (years)'),
            input_with_icon('interest-rate-exact', 'fas fa-percentage', 7.15, 'Loan Interest Rate')
        ], className="flex flex-wrap -mx-2 mb-4"),
        html.Div([
            input_with_icon('cash-savings', 'fas fa-dollar-sign', 18000, 'Cash Savings'),
            input_with_icon('moving-cost', 'fas fa-dollar-sign', 1200, 'Moving Cost'),
        ], className="flex flex-wrap -mx-2 mb-4"),
        html.Div([
            input_with_icon('interest-rate-start', 'fas fa-percentage', 2, 'Payment/Rate Graph Start',
                            "w-full md:w-1/3 px-2"),
            input_with_icon('interest-rate-end', 'fas fa-percentage', 8, 'Mortgage Payments/Rate Graph End',
                            "w-full md:w-1/3 px-2"),
            input_with_icon('interest-rate-step', 'fas fa-stairs', 1, 'Mortgage Payments/Rate Graph Step',
                            "w-full md:w-1/3 px-2"),
        ], className="flex flex-wrap -mx-2 mb-4"),
        html.Button('Export Graph', id='export-button',
                    className="mt-4 bg-blue-500 text-white font-bold py-2 px-4 rounded"),
        html.Div(id='export-output', className="text-green-500 mt-2")
    ], className="p-6 bg-white shadow-md rounded-lg mx-auto w-3/4"),
    html.Div(id='summary-output', className="w-full mt-6"),
    html.Img(id='mortgage-graph', className="w-full mt-6")
], className="w-full")


@app.callback(
    Output('mortgage-graph', 'src'),
    [Input('home-price', 'value'),
     Input('down-payment', 'value'),
     Input('loan-term', 'value'),
     Input('interest-rate-exact', 'value'),
     Input('interest-rate-start', 'value'),
     Input('interest-rate-end', 'value'),
     Input('interest-rate-step', 'value'),
     Input('cash-savings', 'value'),
     Input('moving-cost', 'value')]
)
def update_graph(home_price, down_payment, loan_term, interest_rate_exact, interest_rate_start, interest_rate_end,
                 interest_rate_step, cash_savings, moving_cost):
    results = Calculator.calculate_mortgage_payments(
        home_price, down_payment, loan_term, interest_rate_exact, interest_rate_start, interest_rate_end,
        interest_rate_step, cash_savings, moving_cost
    )
    fig, _ = Plotter.construct_summary_graphs(results)
    return fig_to_uri(fig)


@app.callback(
    Output('export-output', 'children'),
    [Input('export-button', 'n_clicks')],
    [State('home-price', 'value'),
     State('down-payment', 'value'),
     State('loan-term', 'value'),
     State('interest-rate-exact', 'value'),
     State('interest-rate-start', 'value'),
     State('interest-rate-end', 'value'),
     State('interest-rate-step', 'value'),
     State('cash-savings', 'value'),
     State('moving-cost', 'value')]
)
def export_graph(n_clicks, home_price, down_payment, loan_term, interest_rate_exact, interest_rate_start,
                 interest_rate_end, interest_rate_step, cash_savings, moving_cost):
    if n_clicks is None:
        return ''

    results = Calculator.calculate_mortgage_payments(
        home_price, down_payment, loan_term, interest_rate_exact, interest_rate_start, interest_rate_end,
        interest_rate_step, cash_savings, moving_cost
    )
    fig, _ = Plotter.construct_summary_graphs(results)

    # Create the exports directory if it doesn't exist
    export_dir = 'exports'
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    # Create a timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(export_dir, f'{timestamp}_mortgage_summary.svg')

    # Save the image with the timestamped filename in the exports directory
    fig.savefig(filename, format='svg')
    return f'Image saved as {filename}'


if __name__ == '__main__':
    app.run_server(debug=True)
