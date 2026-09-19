# GameRecommendationEngine/src/cover_art.py
import os

import requests
from dotenv import load_dotenv
import streamlit as st


load_dotenv()

RAWG_API_KEY = os.getenv("RAWG_API_KEY")


@st.cache_data
def get_game_cover(title):

    if not RAWG_API_KEY:
        return None

    url = "https://api.rawg.io/api/games"

    params = {
        "key": RAWG_API_KEY,
        "search": title,
        "page_size": 1
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            return None

        return results[0].get("background_image")

    except requests.RequestException:
        return None

    