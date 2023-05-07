from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px


from helper_functions import search_dataframe, get_movie_information, get_dash_recommendations

app = Dash(__name__)

genres = [
    'Animation', 'Adventure', 'Romance', 'Comedy', 'Action', 'Family',
    'History', 'Drama', 'Crime', 'Fantasy', 'Science Fiction',
    'Thriller', 'Music', 'Horror', 'Documentary', 'Mystery', 'Western',
    'TV Movie', 'War', 'Foreign'
]

app.layout = html.Div([
    html.H1(children='Save your movie date night'),
    html.
    P(children=
      "Have you ever been in the situation that you and your significant other have no idea on what to whatch? We come to your rescue!"
      ),
    html.
    P(children=
      "Not only will we provie you with a recommendation based on your favorite movie but also interesting insights about it."
      ),
    html.Hr(),
    html.Br(),
    html.Br(),
    html.P(children="Type a movie name and check if it is in our database"),
    dcc.Input(id="input_random_tile", type="text", placeholder=""),
    html.P(id="output_fuzzy_search"),
    html.
    P(children=
      "Now copy one of the results and use it as input in the next search field"
      ),
    html.Br(),
    html.Br(),
    html.H2(children='Movie Title input'),
    dcc.Input(id="input_true_title", type="text", placeholder=""),
    #dcc.Graph(figure={}, id="graph_true_title"),
    # shows data frame
    html.H2(children='Your recommendation: '),
    html.Table([
        html.Tr([html.Td(["Recommendation 1: "]),
                 html.Td(id='recom_1')]),
        html.Tr([html.Td(["Recommendation 2: "]),
                 html.Td(id='recom_2')]),
        html.Tr([html.Td(["Recommendation 3: "]),
                 html.Td(id='recom_3')]),
        html.Tr([html.Td(["Recommendation 4: "]),
                 html.Td(id='recom_4')]),
        html.Tr([html.Td(["Recommendation 5: "]),
                 html.Td(id='recom_5')]),
    ]),
    html.Table([
        html.Tr([html.Td(["Title: "]),
                 html.Td(id='title')]),
        html.Tr([html.Td(["Genre: "]),
                 html.Td(id='genre')]),
        html.Tr([html.Td(["Budget: "]),
                 html.Td(id='budget')]),
        html.Tr([html.Td(["Runtime: "]),
                 html.Td(id='runtime')]),
        html.Tr([html.Td(["Popularity: "]),
                 html.Td(id='popularity')]),
    ]),
    html.H2(
        children='Some additional information about topics in certain genres'),
    dcc.Dropdown(options=genres,
                 value='Animation',
                 id='controls_and_dropdown_item'),
    # plot histogram
    # dcc.Graph(figure=px.histogram(df, x='adult', y='budget', histfunc='avg'))
])


@app.callback(
    Output("output_fuzzy_search", "children"),
    Input("input_random_tile", "value"),
)
def update_output(input1):
    return search_dataframe(input1)


@app.callback(
    Output('title', 'children'),
    Output('genre', 'children'),
    Output('budget', 'children'),
    Output('runtime', 'children'),
    Output('popularity', 'children'),
    Input("input_true_title", "value"),
)
def update_movie_information(movie_title):
    return get_movie_information(movie_title)


@app.callback(
    Output('recom_1', 'children'),
    Output('recom_2', 'children'),
    Output('recom_3', 'children'),
    Output('recom_4', 'children'),
    Output('recom_5', 'children'),
    Input("input_true_title", "value"),
)
def update_recommendation(movie_title):
    return get_dash_recommendations(movie_title)




if __name__ == '__main__':
    app.run_server(debug=True)
