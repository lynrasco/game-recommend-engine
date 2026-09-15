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
            platform_matrix
        )

        if not recommendations:
            st.error("Game not found.")

        else:
            st.subheader(f"Games similar to {game_title}")

            for recommendation in recommendations:

                st.markdown(
                    f"## {recommendation['title']}"
                )

                st.metric(
                    "Overall similarity",
                    f"{recommendation['overall_similarity']:.0%}"
                )

                st.write("Genre similarity")

                st.progress(
                    float(recommendation["genre_similarity"])
                )
                st.caption(
                    f"{recommendation['genre_similarity']:.2f}"
                )

                st.write("Description similarity")
                st.progress(
                    float(recommendation["summary_similarity"])
                )
                st.caption(
                    f"{recommendation['summary_similarity']:.2f}"
                )
                
                st.write("Platform similarity")
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

                st.divider()