from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

sales = pd.read_csv("data/daily_sales_compiled.csv")

# The unique elements in the data sets are: 'pink morsel', 'gold morsel' 'magenta morsel' 'chartreuse morsel'
# 'periwinkle morsel' 'vermilion morsel' and 'lapis morsel' This needs a bit of reworking once I am more familiar
# with pandas but for now, I will filter all the morsel into their respective colors

pink = sales[(sales['product'] == 'pink morsel')]
gold = sales[(sales['product'] == 'gold morsel')]
chartreuse = sales[(sales['product'] == 'chartreuse morsel')]
periwinkle = sales[(sales['product'] == 'periwinkle morsel')]
vermilion = sales[(sales['product'] == 'vermilion morsel')]
lapis = sales[(sales['product'] == 'lapis morsel')]

app.layout = html.Div(children=[
    html.H1(
        children='Quantium Forage Challenge'
    ),

    html.Div(
        children=' By Roy Lim',
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
                "width": '33%',
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
                "width": '33%',
                'display': 'inline-block'
            }
        ),

        html.Div([
            dcc.Dropdown(
                ["price", "quantity", "total (price * quantity)"],
                'price',
                id="data_type"
            )
        ],
            style={
                "width": '33%',
                'display': 'inline-block'
            }
        ),

        dcc.Graph(id='indicator-graphic')
    ])

])

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('product1', 'value'),
    Input('product2', 'value'),
    Input('data_type', 'value'))
def update_graph(product1, product2, data_type):
    prod1 = sales[(sales['product'] == product1)]
    prod2 = sales[(sales['product'] == product2)]
    fig = px.line(prod1, x="date", y='price', title=data_type + " vs time")
    fig.add_scatter(x=prod2['date'], y=prod2['price'])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
