import streamlit as st

from src.load_data import load_games
from src.recommend import create_matrices, recommend
from src.ui import display_recommendation

st.set_page_config(
    page_title="Game Recommendation Engine",
    page_icon="🎮",
    layout="wide"
)

st.markdown(
    """
    <style>

    .stApp {
        background-color: #11141c;
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
        min-width: 280px;
        max-width: 280px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1c212b;
        border: 1px solid #343b49;
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1rem;
    }

    .stTextInput input {
        border-radius: 8px;
    }

    div[data-testid="stMetric"] {
        background-color: #1d212b;
        border-radius: 10px;
        padding: 0.8rem;
    }

    .recommendation-spacer {
        height: 24px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("Game Recommendation Engine")

st.markdown(
    """
    <p style="font-size: 1.15rem; color: #a9b0bd; margin-top: -10px;">
        Discover your next game using genre, description, and platform similarity.
    </p>
    """,
    unsafe_allow_html=True
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

st.sidebar.markdown(
    "### Recommendation Settings"
)

st.sidebar.caption(
    "Customize how your recommendations are generated."
)

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

st.subheader("Find your next game")

st.caption(
    "Choose a game you already love and we'll find similar titles."
)

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

    st.caption(
        f"{len(matching_titles)} matching game"
        + ("s" if len(matching_titles) != 1 else "")
        + " found"
    )

    game_title = st.selectbox(
        "Select a game",
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

            st.caption(
                f"Based on genre, description, and platform similarity."
            )

            for recommendation in recommendations:
                display_recommendation(recommendation, game_title)