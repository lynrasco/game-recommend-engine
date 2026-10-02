import streamlit as st
import random
from src.load_data import load_games
from src.recommend import create_matrices, recommend
from src.ui import display_recommendation

st.set_page_config(
    page_title="Game Recommendation Engine",
    layout="wide"
)

st.markdown(
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

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #191D27;
        border: 1px solid #2C3240;
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.65rem 1rem;
        border: 1px solid #343A49;
        background-color: #1C202B;
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
    }

    div[data-testid="stMetric"] {
        background-color: #202532;
        border: 1px solid #303646;
        border-radius: 10px;
        padding: 0.8rem;
    }

    .recommendation-spacer {
        height: 24px;
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
    .search-section {
        background-color: #171B24;
        border: 1px solid #2C3240;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0 2rem 0;
    }
    .search-title {
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .search-subtitle {
        color: #929AAA;
        font-size: 0.9rem;
        margin-bottom: 1.25rem;
    }
    .hero {
        padding: 1rem 0 1.5rem 0;
    }
    .hero h1 {
        margin-bottom: 0.35rem;
    }

    .hero p {
        color: #A9B0BD;
        font-size: 1.1rem;
        margin: 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero">
        <h1>Game Recommendation Engine</h1>
        <p>
            Discover your next game using genre, description,
            and platform similarity.
        </p>
    </div>
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
    """
    <div class="settings-header">
        <div class="settings-title">Recommendation Settings</div>
        <div class="settings-subtitle">
            Customize your recommendations
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("### Results")

number_of_recommendations = st.sidebar.slider(
    "Number of recommendations",
    3,
    10,
    5
)

st.sidebar.markdown("### Filters")

minimum_rating = st.sidebar.slider(
    "Minimum game rating",
    0.0,
    5.0,
    0.0,
    0.1
)

selected_platform = st.sidebar.selectbox(
    "Platform",
    platform_options
)

selected_genre = st.sidebar.selectbox(
    "Genre",
    ["Any Genre"] + genre_options
)

minimum_year = st.sidebar.slider(
    "Minimum release year",
    int(games["Release_Year"].min()),
    int(games["Release_Year"].max()),
    int(games["Release_Year"].min())
)

st.markdown(
    """
    <div class="search-section">
        <div class="search-title">
            Find your next game
        </div>
        <div class="search-subtitle">
            Choose a game you already love and discover similar titles.
        </div>
    """,
    unsafe_allow_html=True
)

search_col, _ = st.columns([1, 2])

with search_col:
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
            na=False,
            regex=False
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


recommend_button, surprise_button = st.columns(2)

with recommend_button:
    recommend_clicked = st.button("Recommend Games")

with surprise_button:
    surprise_clicked = st.button("Surprise Me")

if surprise_clicked:

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
        surprise_games["Release_Year"].fillna(0) >= minimum_year
    ]

    if surprise_games.empty:

        st.warning(
            "No games match your current Surprise Me filters. "
            "Try relaxing one of the filters."
        )

    else:

        game_title = random.choice(
            surprise_games["Title"].tolist()
        )

        st.info(
            f"Surprise game selected: {game_title}"
        )


if recommend_clicked or surprise_clicked:

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
            selected_platform,
            selected_genre,
            minimum_year
        )

        if not recommendations:

            st.warning(
                "No recommendations matched your selected filters. "
                "Try lowering the minimum rating, changing the platform or genre, "
                "or choosing an earlier release year."
            )

        else:

            st.subheader(
                f"Games similar to {game_title}"
            )

            st.caption(
                "Based on genre, description, and platform similarity."
            )

            for recommendation in recommendations:

                display_recommendation(
                    recommendation,
                    game_title
                )