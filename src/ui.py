import streamlit as st
import ast

from src.cover_art import get_game_cover


def display_recommendation(recommendation, selected_game_title):

    with st.container():

        cover_url = get_game_cover(recommendation["title"])

        # Main card layout
        col1, col2 = st.columns([1, 3])

        # Cover
        with col1:
            if cover_url:
                st.image(
                    cover_url,
                    use_container_width=True
                )
            else:
                st.caption("No cover available")

        # Game information
        with col2:

            title_col, match_col = st.columns([3, 1])

            with title_col:
                st.subheader(recommendation["title"])

            with match_col:
                st.metric(
                    "Match",
                    f"{recommendation['overall_similarity']:.0%}"
                )

            # Genres
            genres = recommendation["genres"]

            if genres:
                st.markdown(
                    " · ".join(genres)
                )

            # Developer
            developers = recommendation["developers"]

            if isinstance(developers, str):
                try:
                    developers = ast.literal_eval(developers)
                except (ValueError, SyntaxError):
                    developers = [developers]

            st.caption(
                "Developer: " + ", ".join(developers)
            )

            # Release date
            st.caption(
                "Release date: "
                + str(recommendation["release_date"])
            )

            # Platforms
            st.caption(
                "Platforms: "
                + recommendation["platforms"]
            )

            # Rating
            rating = recommendation["rating"]

            if rating == rating:
                full_stars = round(rating)
                empty_stars = 5 - full_stars

                stars = "★" * full_stars + "☆" * empty_stars

                st.write(
                    f"**Rating:** {stars}  `{rating:.1f}/5`"
                )
            else:
                st.write("**Rating:** Not rated")

        st.divider()

        # Description
        st.markdown("#### About")

        summary = recommendation["summary"]

        if summary:
            st.write(summary)
        else:
            st.caption("No description available.")

        # Similarity breakdown
        st.markdown("#### Similarity breakdown")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Genre",
                f"{recommendation['genre_similarity']:.0%}"
            )

        with col2:
            st.metric(
                "Description",
                f"{recommendation['summary_similarity']:.0%}"
            )

        with col3:
            st.metric(
                "Platform",
                f"{recommendation['platform_similarity']:.0%}"
            )

        # Why this game?
        display_why_this_game(
            recommendation,
            selected_game_title
        )

        st.markdown(
            "<div class='recommendation-spacer'></div>",
            unsafe_allow_html=True
        )


def display_why_this_game(recommendation, selected_game_title):

    shared_genres = recommendation["shared_genres"]

    genre_score = recommendation["genre_similarity"]
    summary_score = recommendation["summary_similarity"]
    platform_score = recommendation["platform_similarity"]

    reasons = []

    if shared_genres:
        genre_count = len(shared_genres)

        reasons.append(
            f"Shares {genre_count} genre"
            + ("s" if genre_count != 1 else "")
            + f" with {selected_game_title}"
        )

    if genre_score >= 0.75:
        reasons.append("Very similar genre profile")
    elif genre_score >= 0.50:
        reasons.append("Similar genre profile")

    if summary_score >= 0.25:
        reasons.append("Similar game description")

    if platform_score >= 0.75:
        reasons.append("Available on similar platforms")

    if not reasons:
        reasons.append(
            "Some similarities across the game's features"
        )

    st.markdown("#### Why this game?")

    for reason in reasons:
        st.markdown(f"- {reason}")