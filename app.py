import streamlit as st

from src.load_data import load_games
from src.recommend import create_matrices, recommend
from src.ui import display_recommendation

st.set_page_config(
    page_title="Game Recommendation Engine",
    page_icon="🎮",
    layout="wide"
)

st.title("Game Recommendation Engine")

st.markdown(
    "Discover your next game based on **genre, description, and platform similarity**."
)

st.divider()


@st.cache_data
def load_data():

    games = load_games()

    genre_matrix, summary_matrix, platform_matrix = create_matrices(
        games
    )

    return games, genre_matrix, summary_matrix, platform_matrix


games, genre_matrix, summary_matrix, platform_matrix = load_data()

st.sidebar.header("Recommendation Settings")

number_of_recommendations = st.sidebar.slider(
    "Number of recommendations",
    3,
    10,
    5
)

minimum_rating = st.sidebar.slider(
    "Minimum game rating",
    0.0,
    5.0,
    0.0,
    0.1
)

platform_options = ["Any Platform"] + sorted(
    {
        platform
        for platforms in games["Platform_List"]
        for platform in platforms
    }
)

selected_platform = st.sidebar.selectbox(
    "Platform",
    platform_options
)

st.subheader("Find a game")

game_search = st.text_input(
    "Search by title",
    placeholder="Try Hades, Minecraft, Portal 2..."
)

matching_titles = []

if game_search:
    matching_titles = games[
        games["Title"].str.contains(
            game_search,
            case=False,
            na=False
        )
    ]["Title"].tolist()[:20]

game_title = None

if matching_titles:
    game_title = st.selectbox(
        "Select a game:",
        matching_titles
    )
elif game_search:
    st.warning("No games found. Try another title.")


if st.button("Recommend Games"):

    if not game_title:
        st.warning("Please select a game.")

    else:
        recommendations = recommend(
            game_title,
            games,
            genre_matrix,
            summary_matrix,
            platform_matrix,
            number_of_recommendations,
            minimum_rating,
            selected_platform
        )

        if not recommendations:
            st.warning(
                "No recommendations matched your selected filters. "
                "Try lowering the minimum rating or selecting a different platform."
            )

        else:
            st.subheader(f"Games similar to {game_title}")

            for recommendation in recommendations:
                display_recommendation(recommendation, game_title)