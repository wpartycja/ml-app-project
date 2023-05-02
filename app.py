# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('./data/movies_metadata.csv')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H4('Interactive scatter plot with Iris dataset'),
    dcc.Graph(id="scatter-plot"),
    html.P("Filter by petal width:"),
    dcc.RangeSlider(
        id='range-slider',
        min=0, max=2.5, step=0.1,
        marks={0: '0', 2.5: '2.5'},
        value=[0.5, 2]
    ),
    html.Div(children='The movies dataset'),
    html.Hr(),
    dcc.RadioItems(options=['popularity', 'vote_count', 'vote_average'], value='popularity', id='controls-and-radio-item'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    dcc.Graph(figure={}, id='controls-and-graph')
])

@app.callback(
    Output("scatter-plot", "figure"), 
    Input("range-slider", "value"))
def update_bar_chart(slider_range):
    df = px.data.iris() # replace with your own data source
    low, high = slider_range
    mask = (df['petal_width'] > low) & (df['petal_width'] < high)
    fig = px.scatter(
        df[mask], x="sepal_width", y="sepal_length", 
        color="species", size='petal_length', 
        hover_data=['petal_width'])
    return fig
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