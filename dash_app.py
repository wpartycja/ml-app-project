from dash import Dash, html, dcc, callback, Output, Input
from plotly.graph_objs import Figure


from helper_functions import search_dataframe, get_movie_information, get_dash_recommendations, show_popularity_graph, genres

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Save your movie date night!'),
    html.
    P(children=
      "Have you ever been in the situation that you and your significant other have no idea on what to watch? We come to your rescue!"
      ),
    html.
    P(children=
      "Not only will we provie you with a recommendation based on your favorite movie but also interesting insights about it."
      ),
    html.Br(),
    html.H4(children="Type a movie name and check if it is in our database"),
    dcc.Input(id="input_random_title", type="text", placeholder=""),
    html.P(id="output_fuzzy_search"),
    html.
    P(children=
      "Now copy one of the results and use it as input in the next search field"
      ),
    html.Hr(),
    html.Br(),
    html.Br(),
    html.H2(
        children=
        'From here on please only verified inputs from the search bar above!'),
    html.Br(),
    html.
    H4(children='Your favorite movie you have already watched a houndred times:'
       ),
    dcc.Input(id="input_true_title", type="text", placeholder=""),
    #dcc.Graph(figure={}, id="graph_true_title"),
    # shows data frame
    html.H4(children='Your recommendation based on that movie: '),
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
    html.Hr(),
    html.Br(),
    html.Br(),
    html.H3(children='Get information on a movie in our database'),
    dcc.Input(id="get_movie_information", type="text", placeholder=""),
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
    html.Hr(),
    html.Br(),
    html.Br(),
    html.
    H3(children=
       "Still bored? Lets check the most popular movies from different categories!"
       ),
    dcc.Dropdown(id="genre_dropdown",
                 options=[{
                     "label": g,
                     "value": g
                 } for g in genres],
                 placeholder="Click to input a genre",
                 value=None),
    dcc.Graph(id="output_graph"),
    html.Hr(),
    html.Br(),
    html.Br(),
    html.H3(children="Some additional information from a LDA Analysis"),
    html.Img(src=app.get_asset_url("all_genres.png"),
             width="1331",
             height="800")
    # plot histogram
    # dcc.Graph(figure=px.histogram(df, x='adult', y='budget', histfunc='avg'))
])


@app.callback(Output("output_graph", "figure"),
              Input("genre_dropdown", "value"))
def update_graph(genre: str) -> Figure:
    """
    Return a figure showcasing the top 10 most popular movies for a genre
    """
    if not genre:
        return {}

    return show_popularity_graph(genre)


@app.callback(
    Output("output_fuzzy_search", "children"),
    Input("input_random_title", "value"),
)
def update_output(input1: str) -> str:
    """
    Check if a movie is in our data base
    """
    return search_dataframe(input1)


@app.callback(
    Output('recom_1', 'children'),
    Output('recom_2', 'children'),
    Output('recom_3', 'children'),
    Output('recom_4', 'children'),
    Output('recom_5', 'children'),
    Input("input_true_title", "value"),
)
def update_recommendation(movie_title: str) -> str:
    """
    Give a movie recommendation based on a provided title
    """
    return get_dash_recommendations(movie_title)


@app.callback(
    Output('title', 'children'),
    Output('genre', 'children'),
    Output('budget', 'children'),
    Output('runtime', 'children'),
    Output('popularity', 'children'),
    Input("get_movie_information", "value"),
)
def update_movie_information(movie_title: str) -> str:
    """
    Provide information on a movie based on its title
    """
    return get_movie_information(movie_title)


if __name__ == '__main__':
    app.run_server(debug=True)
