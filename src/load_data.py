# GameRecommendationEngine/src/load_data.py
import pandas as pd
import ast

def parse_genres(value):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError, TypeError):
        return []

def load_games():
    games = pd.read_csv("data/backloggd_games.csv")

    games = games.drop(columns=["Unnamed: 0"])

    games = games.drop_duplicates(subset="Title")

    games = games[
        ~games["Title"].str.contains(
            r"Collector's Edition|Deluxe Edition|Special Edition|Voidheart Edition",
            case=False,
            na=False
        )
    ]

    games["Summary"] = games["Summary"].fillna("")

    games["Genre_List"] = games["Genres"].apply(parse_genres)
    games["Genres"] = games["Genre_List"].apply(lambda genres: " ".join(genres))

    games["Platforms"] = games["Platforms"].fillna("")
    games["Platform_List"] = games["Platforms"].apply(parse_genres)
    games["Platforms"] = games["Platform_List"].apply(
        lambda platforms: " ".join(platforms)
    )


    games = games.reset_index(drop=True)

    return games

