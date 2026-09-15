# GameRecommendationEngine/src/recommend.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def create_matrices(games):

    genre_vectorizer = TfidfVectorizer()

    genre_matrix = genre_vectorizer.fit_transform(
        games["Genres"]
    )

    summary_vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=30000
    )

    summary_matrix = summary_vectorizer.fit_transform(
        games["Summary"]
    )
    platform_vectorizer = TfidfVectorizer()
    platform_matrix = platform_vectorizer.fit_transform(
        games["Platforms"]
    )
    return genre_matrix, summary_matrix, platform_matrix


def recommend(
    title,
    games,
    genre_matrix,
    summary_matrix,
    platform_matrix,
    number_of_recommendations=5
):

    matching_games = games[
        games["Title"].str.lower() == title.lower()
    ]

    if matching_games.empty:
        return []

    game_index = matching_games.index[0]

    genre_scores = cosine_similarity(
        genre_matrix[game_index],
        genre_matrix
    ).flatten()

    summary_scores = cosine_similarity(
        summary_matrix[game_index],
        summary_matrix
    ).flatten()

    platform_scores = cosine_similarity(
        platform_matrix[game_index],
        platform_matrix
    ).flatten()

    final_scores = (
        0.3 * genre_scores +
        0.6 * summary_scores +
        0.1 * platform_scores
    )

    similar_game_indices = final_scores.argsort()[
        ::-1
    ][1:number_of_recommendations + 1]

    recommendations = []

    for index in similar_game_indices:

        recommended_game = games.iloc[index]

        shared_genres = (
            set(games.iloc[game_index]["Genre_List"])
            &
            set(recommended_game["Genre_List"])
        )

        recommendations.append({
            "title": recommended_game["Title"],
            "overall_similarity": final_scores[index],
            "genre_similarity": genre_scores[index],
            "summary_similarity": summary_scores[index],
            "platform_similarity": platform_scores[index],
            "shared_genres": sorted(shared_genres)
        })

    return recommendations