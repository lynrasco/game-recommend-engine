from src.load_data import load_games
from src.recommend import create_matrices, recommend


games = load_games()

genre_matrix, summary_matrix, platform_matrix = create_matrices(games)

while True:
    game_title = input("\nEnter a game (or type 'e' to exit): ")

    if game_title.lower() == "e":
        print("Game Recommendation Engine closing...")
        break

    recommend(
        game_title,
        games,
        genre_matrix,
        summary_matrix,
        platform_matrix
    )