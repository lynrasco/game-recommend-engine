import streamlit as st
import ast

from src.cover_art import get_game_cover

def display_similarity(label, score):
    st.markdown(
        f"""
        <div style="margin-bottom: 0.8rem;">
            <div style="
                display: flex;
                justify-content: space-between;
                margin-bottom: 0.25rem;
            ">
                <span style="color: #C9CED8;">{label}</span>
                <span style="color: #F1F3F5; font-weight: 600;">
                    {score:.0%}
                </span>
            </div>

            <div style="
                height: 7px;
                background: #2A2F3B;
                border-radius: 10px;
                overflow: hidden;
            ">
                <div style="
                    width: {score * 100}%;
                    height: 100%;
                    background: #8B7CF6;
                    border-radius: 10px;
                "></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_recommendation(recommendation, selected_game_title):

    with st.container(border=True):

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

            if not isinstance(developers, list):
                developers = [developers]

                developers = [
                    str(developer)
                    for developer in developers
                    if developer
                ]

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

        display_similarity(
            "Genre",
            recommendation["genre_similarity"]
        )

        display_similarity(
            "Description",
            recommendation["summary_similarity"]
        )

        display_similarity(
            "Platform",
            recommendation["platform_similarity"]
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
        st.markdown(
            f"""
            <div class="reason">
                ✓ {reason}
            </div>
            """,
            unsafe_allow_html=True
        )