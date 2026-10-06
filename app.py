import random
import streamlit as st
from src.load_data import load_games
from src.recommend import create_matrices, recommend
from src.ui import display_recommendation


st.set_page_config(
    page_title="Game Recommendation Engine",
    layout="wide"
)


st.html(
    """
    <style>
        .stApp {
            background-color: #0F1117;
        }

        .block-container {
            max-width: 1200px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }

        h1 {
            font-size: 3rem !important;
            font-weight: 700 !important;
            letter-spacing: -1px;
        }

        h2, h3 {
            font-weight: 600 !important;
        }

        [data-testid="stSidebar"] {
            min-width: 290px;
            max-width: 290px;
            background-color: #151821;
            border-right: 1px solid #292E3A;
        }

        .stButton > button {
            width: 100%;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.65rem 1rem;
            border: 1px solid #343A49;
            background-color: #1C202B;
            color: #F1F3F5;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            border-color: #8B7CF6;
            color: #FFFFFF;
        }

        .stTextInput input {
            border-radius: 10px;
            background-color: #181C25;
            border: 1px solid #343A49;
            color: #F1F3F5;
        }

        .stTextInput input:focus {
            border-color: #8B7CF6;
            box-shadow: 0 0 0 1px #8B7CF6;
        }

        .hero {
            padding: 1rem 0 1.5rem 0;
        }

        .hero h1 {
            margin: 0 0 0.35rem 0;
        }

        .hero p {
            color: #A9B0BD;
            font-size: 1.1rem;
            margin: 0;
        }

        .search-section {
            background-color: #171B24;
            border: 1px solid #2C3240;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1.5rem 0 1rem 0;
        }

        .search-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #F1F3F5;
            margin-bottom: 0.25rem;
        }

        .search-subtitle {
            color: #929AAA;
            font-size: 0.9rem;
        }

        .settings-header {
            padding: 0.5rem 0 1.25rem 0;
        }

        .settings-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #F1F3F5;
        }

        .settings-subtitle {
            font-size: 0.82rem;
            color: #8F97A6;
            margin-top: 0.3rem;
        }
    </style>
    """
)


@st.cache_data
def load_data():
    """Load and preprocess game data."""

    games = load_games()

    genre_matrix, summary_matrix, platform_matrix = create_matrices(
        games
    )

    return (
        games,
        genre_matrix,
        summary_matrix,
        platform_matrix
    )


def display_header():
    """Display the application header."""

    st.html(
        """
        <div class="hero">
            <h1>Game Recommendation Engine</h1>
            <p>
                Discover your next game using genre,
                description, and platform similarity.
            </p>
        </div>
        """
    )

    st.divider()


def display_sidebar(games):
    """Display recommendation settings."""

    st.sidebar.html(
        """
        <div class="settings-header">
            <div class="settings-title">
                Recommendation Settings
            </div>

            <div class="settings-subtitle">
                Customize your recommendations
            </div>
        </div>
        """
    )

    st.sidebar.markdown("### Results")

    number_of_recommendations = st.sidebar.slider(
        "Number of recommendations",
        min_value=3,
        max_value=10,
        value=5
    )

    st.sidebar.markdown("### Filters")

    minimum_rating = st.sidebar.slider(
        "Minimum game rating",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.1
    )

    platform_options = sorted(
        {
            platform
            for platforms in games["Platform_List"]
            for platform in platforms
        }
    )

    genre_options = sorted(
        {
            genre
            for genres in games["Genre_List"]
            for genre in genres
        }
    )

    selected_platform = st.sidebar.selectbox(
        "Platform",
        ["Any Platform"] + platform_options
    )

    selected_genre = st.sidebar.selectbox(
        "Genre",
        ["Any Genre"] + genre_options
    )

    minimum_year = st.sidebar.slider(
        "Minimum release year",
        min_value=int(games["Release_Year"].min()),
        max_value=int(games["Release_Year"].max()),
        value=int(games["Release_Year"].min())
    )

    return (
        number_of_recommendations,
        minimum_rating,
        selected_platform,
        selected_genre,
        minimum_year
    )


def search_games(games):
    """Search for games by title."""

    st.html(
        """
        <div class="search-section">
            <div class="search-title">
                Find your next game
            </div>

            <div class="search-subtitle">
                Choose a game you already love and discover similar titles.
            </div>
        </div>
        """
    )

    game_search = st.text_input(
        "Search by title",
        placeholder="Try Hades, Minecraft, Portal 2...",
    )

    if not game_search:
        return None

    matching_titles = (
        games[
            games["Title"].str.contains(
                game_search,
                case=False,
                na=False,
                regex=False
            )
        ]["Title"]
        .tolist()
    )

    matching_titles = matching_titles[:20]

    if not matching_titles:
        st.warning(
            "No games found. Try another title."
        )
        return None

    st.caption(
        f"{len(matching_titles)} matching game"
        f"{'s' if len(matching_titles) != 1 else ''} found"
    )

    return st.selectbox(
        "Select a game",
        matching_titles
    )


def select_surprise_game(
    games,
    minimum_rating,
    selected_platform,
    selected_genre,
    minimum_year
):
    """Select a random game that matches the current filters."""

    surprise_games = games[
        games["Rating"].fillna(0) >= minimum_rating
    ]

    if selected_platform != "Any Platform":
        surprise_games = surprise_games[
            surprise_games["Platform_List"].apply(
                lambda platforms:
                selected_platform in platforms
            )
        ]

    if selected_genre != "Any Genre":
        surprise_games = surprise_games[
            surprise_games["Genre_List"].apply(
                lambda genres:
                selected_genre in genres
            )
        ]

    surprise_games = surprise_games[
        surprise_games["Release_Year"].fillna(0)
        >= minimum_year
    ]

    if surprise_games.empty:
        return None

    return random.choice(
        surprise_games["Title"].tolist()
    )


def display_recommendations(
    game_title,
    games,
    genre_matrix,
    summary_matrix,
    platform_matrix,
    number_of_recommendations,
    minimum_rating,
    selected_platform,
    selected_genre,
    minimum_year
):
    """Generate and display recommendations."""

    recommendations = recommend(
        game_title,
        games,
        genre_matrix,
        summary_matrix,
        platform_matrix,
        number_of_recommendations,
        minimum_rating,
        selected_platform,
        selected_genre,
        minimum_year
    )

    if not recommendations:
        st.warning(
            "No recommendations matched your selected filters. "
            "Try lowering the minimum rating, changing the "
            "platform or genre, or choosing an earlier release year."
        )
        return

    st.subheader(
        f"Games similar to {game_title}"
    )

    st.caption(
        "Recommendations are based on genre, description, "
        "and platform similarity."
    )

    for recommendation in recommendations:
        display_recommendation(
            recommendation,
            game_title
        )


def main():

    games, genre_matrix, summary_matrix, platform_matrix = load_data()

    display_header()

    (
        number_of_recommendations,
        minimum_rating,
        selected_platform,
        selected_genre,
        minimum_year
    ) = display_sidebar(games)

    game_title = search_games(games)

    recommend_col, surprise_col = st.columns(2)

    with recommend_col:
        recommend_clicked = st.button(
            "Recommend Games"
        )

    with surprise_col:
        surprise_clicked = st.button(
            "🎲 Surprise Me"
        )

    if surprise_clicked:

        game_title = select_surprise_game(
            games,
            minimum_rating,
            selected_platform,
            selected_genre,
            minimum_year
        )

        if game_title is None:
            st.warning(
                "No games match your current Surprise Me filters. "
                "Try relaxing one of the filters."
            )
            return

        st.info(
            f"Surprise game selected: **{game_title}**"
        )

    if recommend_clicked or surprise_clicked:

        if not game_title:
            st.warning(
                "Please search for and select a game first."
            )
            return

        display_recommendations(
            game_title,
            games,
            genre_matrix,
            summary_matrix,
            platform_matrix,
            number_of_recommendations,
            minimum_rating,
            selected_platform,
            selected_genre,
            minimum_year
        )


if __name__ == "__main__":
    main()