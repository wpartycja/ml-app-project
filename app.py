# Import packages
import base64
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import pickle
import matplotlib.pyplot as plt
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from PIL import Image


# Incorporate data
df = pd.read_csv('./data/movies_metadata.csv')
dff = pd.read_csv('./data/full_data_2_index.csv')
genres = dff['genres']

image_path = './data/plot.png'
pil_img = Image.open("./data/plot.png")

with open('./data/embed_tsne.pkl', 'rb') as f:
    x = pickle.load(f)

def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Dropdown(['popularity', 'genres', 'vote_average'], 'popularity', id='demo-dropdown'),
    html.Div(id='dd-output-container'),

# usign get_asset_url function
    html.Img(src=pil_img, width="600", height="700"),                
    html.Div(children='The movies dataset'),
    html.Hr(),
    dcc.RadioItems(options=['popularity', 'vote_count', 'vote_average'], value='popularity', id='controls-and-radio-item'),
    dcc.Graph(figure={}, id='controls-and-graph'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=6),
])

@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return f'You have selected {value}'


# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='title', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)











"""
# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Incorporate data
df = pd.read_csv('./data/movies_metadata.csv')

new_df = df.drop(columns=["belongs_to_collection", "homepage", "poster_path", "production_companies", "runtime", "status", "video", "adult", "imdb_id","production_countries", "release_date" ])

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)



# App layout
app.layout = html.Div([
    html.Div(className='row',children='My First App with Data, Graph, and Controls', style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}),
    html.Hr(),
    html.Div(className='row', children=[dcc.RadioItems(options=['popularity', 'vote_count', 'vote_average'], value='popularity',inline=True, id='my-radio-buttons-final')]),
    html.Div(className='row', children=[dash_table.DataTable(data=new_df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})]),
    html.Div(className='six columns', children=[  dcc.Graph(figure={}, id='histo-chart-final')])
  
])
@callback(
    Output(component_id='histo-chart-final', component_property='figure'),
    Input(component_id='my-radio-buttons-final', component_property='value')
)

def update_graph(col_chosen):
    fig = px.histogram(df, x='title', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('The movies dataset', className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        dbc.RadioItems(options=[{"label": x, "value": x} for x in ['popularity', 'vote_count', 'vote_average']],
                       value='vote_count',
                       inline=True,
                       id='radio-buttons-final')
    ]),

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(data=new_df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'})
        ], width=6),

        dbc.Col([
            dcc.Graph(figure={}, id='my-first-graph-final')
        ], width=6),
    ]),

], fluid=True)

# Add controls to build the interaction
@callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Input(component_id='radio-buttons-final', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='title', y=col_chosen, histfunc='avg')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
"""