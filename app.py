'''
 # @ Create Time: 2022-08-31 15:41:53.387913
'''

import pathlib
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import urllib.request
import json
from numerize import numerize
from dash_bootstrap_templates import load_figure_template

load_figure_template('solar')

# stylesheet with the .dbc class
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# App Instance
app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR, dbc_css],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0'}]
                )
            

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

# get geoJSON file for zipcodes in IA
with urllib.request.urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
target_states = ['19']
counties['features'] = [f for f in counties['features'] if f['properties']['STATE'] in target_states]

# -- Import data, csv -> df
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df = pd.read_csv(DATA_PATH.joinpath('vodka21.csv'))


### ----------------------------------------------------
# CARD 1 - Total STATE sales 2021
total_sales_21 = numerize.numerize(df["Sales(USD)"].sum(), 2)

# CARD 2 - Total ABD profit 2021
total_profit_21 = numerize.numerize(df['profit'].sum(), 2)

# CARD 3 - State Sales per Capita 2021
total_sales = df['Sales(USD)'].sum()
total_population = df['population'].unique().sum()
total_sales_cap = numerize.numerize(total_sales / total_population, 2)

# User Input Card
card_metric = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("User Input", className='card-title text-success'),
                html.H6("Choose a Metric:", className='card-subtitle mb-2 mt-3'),
                dcc.Dropdown(id='slct_metric',
                    options=[
                        {'label': "Sales(USD)", 'value': "Sales(USD)"},
                        {'label': "Volume(L)", 'value': "Sales(Liters)"}],
                    multi=False,
                    value="Sales(USD)"),
                html.Br(),
                html.H6("Choose a County:", className='card-subtitle mb-2'),
                dcc.Dropdown(id='slct_county',
                    options=[{'label':x.title(), 'value':x}
                              for x in sorted(df['county'].unique())],
                    multi=False,
                    value='ADAIR'),
                html.Br(),
                html.Br()
            ]
        )
    ]
)
# -----------------------------------------------------------------------------------------------------
# APP LAYOUT

app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Iowa Vodka Sales Dashboard",
                            className='text-center text-success mb-4 mt-4'), width=12),
            dbc.Col(
                dbc.Card([
                        dbc.CardBody([
                            html.H6(
                                "Total State Sales 2021",
                                className='card-subtitle mb-2 text-success text-center'),
                            html.H1(
                                "$" + total_sales_21,
                                className='card-title mt-2 text-center text-primary'),
                            # html.H4(
                            #     sales_usd
                ])]),
            width=4, 
            ),
            dbc.Col(
                dbc.Card([
                        dbc.CardBody([
                            html.H6(
                                "ABD Total Profit 2021",
                                className='card-subtitle mb-2 text-success text-center'),
                            html.H1(
                                "$" + total_profit_21,
                                className='card-title mt-2 text-center text-primary'),
                            # html.H4(
                            #     sales_liters
                ])]),
                width=4
            ),
            dbc.Col(
                dbc.Card([
                        dbc.CardBody([
                            html.H6(
                                "State Sales per Capita 2021",
                                className='card-subtitle mb-2 text-success text-center'),
                            html.H1(
                                "$" + total_sales_cap,
                                className='card-title mt-2 text-center text-primary')
                            # html.H4(
                            #     sales_gallons
                ])]
                    ),
                width=4        
            )
        ],
            className="mb-4", justify='around'
        ),
        dbc.Row([
            dbc.Col([
                card_metric,
                html.Div(id='table_title', 
                         children=[], 
                         className='text-center  text-success mt-4',
                         style={'fontSize': '20px'}
                         ),
                html.Div(id='table-container')
        ]),
            dbc.Col(card_metric, width=3),
            dbc.Col(
                dcc.Graph(id='vodka_sales_map', figure={}), width=9),
                
                ],
        className="mb-4"
        ),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='monthly_sales', figure={}), width=8
            ),
            
        ])
        ],
        className="mb-4")

# # ------------------------------------------------------------------------------
# # Connect the Plotly graphs with Dash Components

@app.callback([ 
    Output(component_id='vodka_sales_map', component_property='figure')],
    Input(component_id='slct_metric', component_property='value')
)
def update_map(option_slctd):

    dff = df.copy()
    dff = dff.groupby(['fips', 'county'])[option_slctd].sum().reset_index()

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        geojson=counties,
        locations='fips',
        scope='usa',
        color=option_slctd,
        color_continuous_scale='Teal',
        range_color=[dff[option_slctd].min(), (dff[option_slctd].max() * .4)],
        hover_data=['county', option_slctd],
        labels={'county': 'County'},)
    fig.update_layout(
        title={
            'text': 'Iowa Vodka {}'.format(option_slctd),
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size':25}
            },
        height=500, 
        # margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
        geo_bgcolor='#22434a',
        paper_bgcolor='#22434a')
    fig.update_geos(fitbounds='locations', visible=False)
    # fig.update_coloraxes(colorbar_tickfont_color='white', colorbar_title_font_color='white')
    return [fig]

@app.callback(
    Output(component_id='monthly_sales', component_property='figure'),
    [Input(component_id='slct_county', component_property='value'),
     Input(component_id='slct_metric', component_property='value')
]
)

def update_chart(county, metric):
    dff2 = df.copy()
    dff2 = dff2[dff2['county']==county]
    dff2 = dff2.groupby(['month'])[metric].sum().reset_index()
    
    fig = px.bar(dff2, x = 'month', y = metric, color=metric, color_continuous_scale='Teal')

    fig.update_layout(
        title={
            'text': '{} County 2021 Monthly Vodka {}'.format(county.title(), metric),
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
        margin={'r': 0, 't': 40, 'l': 0, 'b': 25},
        paper_bgcolor='#22434a',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig.update_xaxes(
        # tickangle=45,
        title_text = None,
        title_standoff = 25, 
        title_font = {'size': 16},
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                'Oct', 'Nov', 'Dec'],
        tickvals = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
        showgrid=False

    )

    fig.update_yaxes(
        title_text = metric,
        title_standoff = 25,
        title_font = {'size':16},
        showgrid=True
    )
    return(fig)

@app.callback(
    [Output(component_id='table_title', component_property='children'),
     Output(component_id='table-container', component_property='children')],
    [Input(component_id='slct_county', component_property='value'),
     Input(component_id='slct_metric', component_property='value')]
)

def make_table(county, metric):
    dff3 = df.copy()
    dff3 = dff3[dff3['county']==county]
    dff3 = dff3.groupby('item_description')[metric].sum().sort_values(ascending=False).reset_index()[:5]
    dff3 = dff3.rename(columns={'item_description':'Product Name'})
    
    table_title = "Top Selling Products for {}".format(county.title())

    table_df = dbc.Table.from_dataframe(dff3, 
                    responsive=True,
                    striped=True,
                    bordered=True,
                    hover=True,
                    className="top_products mt-4",
                    # style={:'dark'}
                    )
    return table_title, table_df



# -------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)
    