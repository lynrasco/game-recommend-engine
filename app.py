import streamlit as st

from src.load_data import load_games
from src.recommend import create_matrices, recommend


st.title("Game Recommendation Engine")

st.write(
    "Find games similar to your favorites using "
    "genre, description, and platform similarity."
)


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


game_title = st.text_input(
    "Find a game:",
    placeholder="Type a game title..."
)


if st.button("Recommend Games"):

    if not game_title:
        st.warning("Please enter a game title.")

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
            st.error("Game not found.")

        else:
            st.subheader(f"Games similar to {game_title}")

            for recommendation in recommendations:
                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.subheader(recommendation["title"])

                    with col2:
                        st.metric(
                            "Match",
                            f"{recommendation['overall_similarity']:.0%}"
                        )

                    st.write(
                        "**Genres:** "
                        + " • ".join(recommendation["genres"])
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        developers = recommendation["developers"]

                        if isinstance(developers, str):
                            try:
                                import ast
                                developers = ast.literal_eval(developers)
                            except (ValueError, SyntaxError):
                                developers = [developers]

                        st.write(
                            "**Developer:** "
                            + ", ".join(developers)
                        )

                    with col2:
                        st.write(
                            "**Release date:** "
                            + str(recommendation["release_date"])
                        )

                        st.write(
                            "**Platforms:** "
                            + recommendation["platforms"]
                        )

                        rating = recommendation["rating"]

                        if rating == rating:
                            full_stars = round(rating)
                            empty_stars = 5 - full_stars
                            stars = "★" * full_stars + "☆" * empty_stars
                            st.write(f"**Rating:** {stars}")
                        else:
                            st.write("**Rating:** Not rated")

                        st.write("**About:**")
                        st.write(recommendation["summary"])

                        st.write("**Similarity breakdown:**")
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.write("Genre")
                            st.progress(
                                float(recommendation["genre_similarity"])
                            )

                            st.caption(
                                f"{recommendation['genre_similarity']:.2f}"
                            )

                        with col2:
                            st.write("Description")
                            st.progress(
                                float(recommendation["summary_similarity"])
                            )
                            st.caption(
                                f"{recommendation['summary_similarity']:.2f}"
                            )

                        with col3:
                            st.write("Platform")
                            st.progress(
                                float(recommendation["platform_similarity"])
                            )
                            st.caption(
                                f"{recommendation['platform_similarity']:.2f}"
                            )

                        st.write(
                            "**Shared genres:** "
                            + ", ".join(recommendation["shared_genres"])
                        )