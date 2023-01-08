from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

sales = pd.read_csv("data/daily_sales_compiled.csv")

# The unique elements in the data sets are: 'pink morsel', 'gold morsel' 'magenta morsel' 'chartreuse morsel'
# 'periwinkle morsel' 'vermilion morsel' and 'lapis morsel'

app.layout = html.Div(children=[
    html.H1(
        children='Quantium Forage Challenge'
    ),

    html.Div(
        children=' By Roy Lim'
    ),
    html.H2(
        children='On the following dashboard, please choose two different products to compare with.'
    ),
    html.Div(
        children='The vertical, black line denotes when the Pink Morsel`s price was increased',
        style={
            'margin-bottom': '2rem'
        }
    ),

    html.Div([
        html.Div([
            dcc.Dropdown(
                sales['product'].unique(),
                'pink morsel',
                id="product1"
            )
        ],
            style={
                "width": '24%',
                'display': 'inline-block'
            }
        ),
        html.Div([
            dcc.Dropdown(
                sales['product'].unique(),
                'gold morsel',
                id="product2"
            )
        ],
            style={
                "width": '24%',
                'display': 'inline-block'
            }
        ),

        html.Div([
            dcc.Dropdown(
                ["price", "quantity"],
                'quantity',
                id="data_type"
            )
        ],
            style={
                "width": '24%',
                'display': 'inline-block'
            }
        ),
        html.Div([
            dcc.Dropdown(
                np.append('all regions', sales["region"].unique()),
                'all regions',
                id="region"
            )
        ],
            style={
                "width": '24%',
                'display': 'inline-block'
            }
        ),

        dcc.Graph(id='raw-graphic'),

        dcc.Graph(id='averaged-graphic')
    ])

])


# Raw Data
@app.callback(
    Output('raw-graphic', 'figure'),
    Input('product1', 'value'),
    Input('product2', 'value'),
    Input('data_type', 'value'),
    Input('region', 'value'))
def update_graph(product1, product2, data_type, region):
    prod1 = sales[(sales['product'] == product1)]
    prod2 = sales[(sales['product'] == product2)]

    # Filter based on region
    if region != 'all regions':
        prod1 = prod1[(prod1['region'] == region)]
        prod2 = prod2[(prod2['region'] == region)]

    # Add a scatter graph to plot
    fig = px.scatter(pd.concat([prod1, prod2]), x='date', y=data_type, title=data_type + " vs time", color='product')

    # Adding Legend
    fig.update_layout(showlegend=True)
    # Adding a vertical line for where the price change has occurred
    fig.add_vline(x="2021-01-14")
    return fig


# Raw Data
@app.callback(
    Output('averaged-graphic', 'figure'),
    Input('product1', 'value'),
    Input('product2', 'value'),
    Input('data_type', 'value'),
    Input('region', 'value'))
def update_graph(product1, product2, data_type, region):
    prod1 = sales[(sales['product'] == product1)]
    prod2 = sales[(sales['product'] == product2)]

    # Filter based on region
    if region != 'all regions':
        prod1 = prod1[(prod1['region'] == region)]
        prod2 = prod2[(prod2['region'] == region)]

    if data_type == 'quantity':
        # Group by date and take the average
        prod1 = prod1.groupby("date").mean(numeric_only=True)
        prod2 = prod2.groupby("date").mean(numeric_only=True)

    # Add a scatter graph to plot
    fig = px.scatter(pd.concat([prod1, prod2]), x='date', y=data_type, title=data_type + " vs time", color='product')

    # Adding Legend
    fig.update_layout(showlegend=True)
    # Adding a vertical line for where the price change has occurred
    fig.add_vline(x="2021-01-14")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
