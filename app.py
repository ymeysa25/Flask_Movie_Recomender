from flask import Flask, render_template, jsonify, request
from RSEngine import load_latest_movie, load_movie, get_recommendations, get_movie
import pickle

app = Flask(__name__)

with open('model/cosine_sim_by_story.pickle', 'rb') as handle:
    cosine_sim_story = pickle.load(handle)

with open('model/cosine_sim_by_feature.pickle ', 'rb') as handle:
    cosine_sim_features = pickle.load(handle)

@app.route("/")
def homePage():
    top_rated = load_movie("vote_average")
    pop_movie = load_movie("popularity")
    most_vote = load_movie("vote_count")
    return render_template("index.html", top_rated = top_rated, pop_movie = pop_movie, most_vote =most_vote)


@app.route("/movies", methods = ["GET", "POST"])
def moviePage():
    data = {}
    try:
        movie_title = request.args.get('title')
        # Rec by Story
        movie_rec_by_story = get_recommendations(movie_title, cosine_sim_story)
        movie_rec_story = get_movie(movie_rec_by_story[0])

        # Credits, Genres and Keywords Based Recommender
        movie_rec_by_features = get_recommendations(movie_title, cosine_sim_features)


        return render_template("movie.html", data = movie_rec_story[0], movie_by_story = movie_rec_by_story[1],
                               movie_by_feature = movie_rec_by_features[1])
    except Exception as e:
        data['success'] = False
        data["message"] = str(e)
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
