import pandas as pd
from fuzzywuzzy import process, fuzz
import pickle
from numpy import ndarray

# loading data
df = pd.read_csv("data/full_data_3.csv", low_memory=False)

# loading cosine similarity of TF-IDF representation
with open("data/cosine_sim.pkl", "rb") as file:
  cosine_sim = pickle.load(file)


def search_dataframe(title_string: str) -> str:
    """
    Helper function to perform a fuzzy search based on user input and check
    if a movie is contained in our data base.
    """

    if title_string is None:
        return "Please wait for search results to appear (~30 sec) :)"

    else:
        # fuzzy search possible data entries
        similar_titles = process.extract(title_string,
                                         df["original_title"],
                                         scorer=fuzz.token_sort_ratio)
        title_string = "Here are your results: "

        # return all suggested entries up to 5 or less
        max_length = min(5, len(similar_titles))
        for title in similar_titles[:max_length]:
            title_string += f"  --  {title[0]}  --  "
        return title_string



def get_movie_information(movie_title: str) -> str:
    """
    Helper function to fetch information on a movie in our data base
    """

    if df['original_title'].eq(movie_title).any():
        tmp = df.loc[df["original_title"] == movie_title]
        try:
            title = tmp["original_title"].item()
            genre = tmp["genres_isolated"].item()
            budget = tmp["budget"].item()
            runtime = tmp["runtime"].item()
            popularity = tmp["popularity"].item()

        except:
            title = "Too many results: Please try another movie"
            genre = "Too many results: Please try another movie"
            budget = "Too many results: Please try another movie"
            runtime = "Too many results: Please try another movie"
            popularity = "Too many results: Please try another movie"

    else:
        title = None
        genre = None
        budget = None
        runtime = None
        popularity = None

    return title, genre, budget, runtime, popularity


def get_recommendations(title: str, n_recommendations: int,
                        cosine_sim: ndarray = cosine_sim) -> list:

    # Get the index of the movie that matches the title
    idx = df.loc[df['title'] == title].index.values[0]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:n_recommendations + 1]

    # Return the top 10 most similar movies
    return sim_scores


def get_dash_recommendations(title: str) -> str:
    if title not in df['title'].tolist():
        recom_1 = "Please try another movie"
        recom_2 = "Please try another movie"
        recom_3 = "Please try another movie"
        recom_4 = "Please try another movie"
        recom_5 = "Please try another movie"

    else:
        recomm = get_recommendations(title, 5)
        recomm_lst = []
        for idx, sim in recomm:
            movie_name = df.loc[df.index == idx]['title'].tolist()[0]
            sim = str(round(sim, 2))
            recomm_lst.append(f'{movie_name} ---- with a certainty of: {sim}%')

        recom_1 = recomm_lst[0]
        recom_2 = recomm_lst[1]
        recom_3 = recomm_lst[2]
        recom_4 = recomm_lst[3]
        recom_5 = recomm_lst[4]

    return recom_1, recom_2, recom_3, recom_4, recom_5
