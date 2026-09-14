from load_data import load_games
from recommend import create_matrices
from sklearn.metrics.pairwise import cosine_similarity


def evaluate_recommendations(
    games,
    genre_matrix,
    summary_matrix,
    platform_matrix,
    test_games,
    number_of_recommendations=5
):

    results = []

    for title in test_games:

        matching_games = games[
            games["Title"].str.lower() == title.lower()
        ]

        if matching_games.empty:
            print(f"{title}: Game not found.")
            continue

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

        average_similarity = (
            final_scores[similar_game_indices].mean()
        )

        recommendation_genres = set()

        for index in similar_game_indices:
            recommendation_genres.update(
                games.iloc[index]["Genre_List"]
            )

        genre_diversity = len(recommendation_genres)

        results.append({
            "game": title,
            "average_similarity": average_similarity,
            "genre_diversity": genre_diversity
        })

    return results


if __name__ == "__main__":

    games = load_games()

    genre_matrix, summary_matrix, platform_matrix = create_matrices(
        games
    )

    test_games = [
        "Undertale",
        "Hades",
        "Elden Ring",
        "Hollow Knight",
        "Celeste",
        "Minecraft",
        "Portal 2",
        "Resident Evil 4",
        "Persona 5 Royal",
        "Stray"
    ]

    results = evaluate_recommendations(
        games,
        genre_matrix,
        summary_matrix,
        platform_matrix,
        test_games
    )

    print("\nRecommendation Evaluation:")

    for result in results:
        print(
            f"\n{result['game']}"
            f"\nAverage similarity: "
            f"{result['average_similarity']:.2f}"
            f"\nGenre diversity: "
            f"{result['genre_diversity']} genres"
        )