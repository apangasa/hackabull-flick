from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import numpy as np
import json


def text_similarity(text_list, movie_in, movies, count):
    tf = TfidfVectorizer(analyzer='word', ngram_range=(
        1, 2), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(text_list)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    sim_scores = list(enumerate(cosine_sim[movie_in['id']]))
    sim_scores = sorted(sim_scores, reverse=True,
                        key=lambda element: element[1])
    sim_scores = sim_scores[1:count]
    return sim_scores


def score_by_genre(movie_in, movies, count):
    # fill index for genres appropriately
    genres = [movie[3] for movie in movies]

    return text_similarity(genres, movie_in, movies, count)


def score_by_synposis(synopses, movie_in, movies, count):
    return text_similarity(synopses, movie_in, movies, count)


def recommend(movie_in):
    movies_in = {}
    with open('backend/liked.json', 'r') as liked:
        movies_in = json.load(liked)
    movies_in[movie_in['id']] = movie_in

    movies = []  # Request movies

    scores_by_genre = set()
    for in_key in movies_in.keys():
        scores_by_genre += set(score_by_genre(movies_in[in_key], movies, 25))
    scores_by_genre = sorted(
        scores_by_genre, reverse=True, key=lambda element: element[1])[1:50]

    indices = [score[0] for score in scores_by_genre]
    # fill index for description appropriately
    synopses = [movies[index][4] for index in indices]
    scores_by_synopsis = score_by_synposis(synopses, movie_in, movies, 5)

    indices = [score[0] for score in scores_by_synopsis]
    recommendations = [movies[index] for index in indices]

    avg_sims = []

    # cosine similarity of feature vectors
    for rec in recommendations:
        rec_vector = np.array([rec['run_time'], rec['year'],
                               rec['imdb_rating'], rec['rt_rating'], rec['imdb_votes']])
        avg_sim = 0

        for query in movies_in:
            query_vector = np.array([query['run_time'], query['year'],
                                     query['imdb_rating'], query['rt_rating'], query['imdb_votes']])

            sim = cosine_similarity([query_vector], [rec_vector])
            avg_sim += sim

        avg_sim /= len(movies_in.keys())
        avg_sims.append(avg_sim)

    avg_sims_np = np.array(avg_sims)
    return recommendations[np.argmax(avg_sims_np)]
