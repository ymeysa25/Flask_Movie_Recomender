import pandas as pd
import json




def load_db():
    return pd.read_csv("db/csv/MOVIES_DB.csv")

movies = load_db()


def load_latest_movie():
    df = load_db()
    df.to_json(r'movie.json', orient='records')

    with open("movie.json", "r") as file:
        data = file.read()
        data = json.loads(data)

    return data


def load_movie(category):
    filename = "db/json/popular_movie.json"
    pop = movies.sort_values(category, ascending=False)
    pop_movie = pop[["title", "popularity", "img_url", "vote_average"]][:6]

    # normalize vote average
    nor_vote_avg = [round(i / 2) for i in pop_movie['vote_average']]
    pop_movie['vote_average'] = nor_vote_avg

    movie = pop_movie.to_json(orient='records')
    data = json.loads(movie)
    # with open(filename, "r") as file:
    #     data = file.read()
    #     data = json.loads(data)

    return data

def get_movie(idx):
    movie = movies[idx:idx+1][['title', 'score', 'img_url', 'overview']].to_json(orient='records')
    movie = json.loads(movie)
    return movie


# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(title, cosine_sim):
    indices = pd.Series(movies.index, index= movies['title']).drop_duplicates()

    # Get the index of the movie that matches the title
    idx = indices[title]
    print(idx)
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # normalize vote average
    avg_round = [round(i / 2) for i in movies['vote_average']]
    movies['vote_average'] = avg_round

    movie_detail = movies[["title", "popularity", "img_url", "vote_average"]].iloc[movie_indices].to_json(orient='records')
    movie_detail = json.loads(movie_detail)


    # Return the top 10 most similar movies
    return idx, movie_detail
