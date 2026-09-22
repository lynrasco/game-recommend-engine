# GameRecommendationEngine/src/recommend.py
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
    number_of_recommendations=5,
    minimum_rating=0.0,
    selected_platform="Any Platform",
    selected_genre="Any Genre",
    minimum_year=None
):

    matching_games = games[
        games["Title"].str.lower() == title.lower()
    ]

    if matching_games.empty:
        return []

    game_index = matching_games.index[0]

    candidate_indices = games.index[
        games["Rating"].fillna(0) >= minimum_rating
    ]

    if selected_platform != "Any Platform":
        candidate_indices = candidate_indices[
            candidate_indices.map(
                lambda index:
                selected_platform in games.iloc[index]["Platform_List"]
            )
        ]

    if selected_genre != "Any Genre":
        candidate_indices = candidate_indices[
            candidate_indices.map(
                lambda index:
                selected_genre in games.iloc[index]["Genre_List"]
            )
        ]

    if minimum_year:
        candidate_indices = candidate_indices[
            games.loc[candidate_indices, "Release_Year"] >= minimum_year
        ]

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

    ranked_indices = final_scores.argsort()[::-1]

    similar_game_indices = [
        index
        for index in ranked_indices
        if index != game_index and index in candidate_indices
    ][:number_of_recommendations]

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
            "release_date": recommended_game["Release_Date"],
            "developers": recommended_game["Developers"],
            "summary": recommended_game["Summary"],
            "platforms": recommended_game["Platforms"],
            "genres": recommended_game["Genre_List"],
            "rating": recommended_game["Rating"],
            "overall_similarity": final_scores[index],
            "genre_similarity": genre_scores[index],
            "summary_similarity": summary_scores[index],
            "platform_similarity": platform_scores[index],
            "shared_genres": sorted(shared_genres)
        })

    return recommendations