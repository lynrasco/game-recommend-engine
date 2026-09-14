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
        print("Game not found.")
        return

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

    print(
        f"\nGames similar to "
        f"{games.iloc[game_index]['Title']}:"
    )

    for index in similar_game_indices:
        recommended_game = games.iloc[index]

        shared_genres = set(
            games.iloc[game_index]["Genre_List"]
        ) & set(
            recommended_game["Genre_List"]
        )
        
        print(
            f"\n{recommended_game['Title']}"
            f"\nOverall similarity: {final_scores[index]:.2f}"
            f"\nGenre similarity: {genre_scores[index]:.2f}"
            f"\nSummary similarity: {summary_scores[index]:.2f}"
            f"\nPlatform similarity: {platform_scores[index]:.2f}"
            f"\nShared genres: {', '.join(shared_genres)}"
        )