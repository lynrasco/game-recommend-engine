# Game Recommendation Engine
A content-based game recommendation system built using Python, Pandas, scikit-learn, and Streamlit

This application helps recommend games to users based on similarities in genre, description, and platform. Users can search for a game, customize recommendation filters, or use the 'Surprise Me' feature to randomize a ga,e that matches their criteria.

## Features

- Searching games by title
- Content-based game recommendations
- TF-IDF feature extraction
- Cosine similarity
- Weighted similarity scoring
- Genre filtering
- Platform filtering
- Minimum rating filtering
- Minimum release year filtering
- Surprise Me button
- Game cover artwork using RAWG API
- Similarity breakdown for each recommendation
- Explanation for each game recommendation
- Streamlit web interface

## How this application works

The recommendation system uses a content-based approach

### 1. Data Preprocessing

The game dataset (csv file) is cleaned before recommendations are generated

Includes:

- Removing unnecessary columns, and duplicate game titles
- Handling empty descriptions
- Parsing platform and genre data
- Removing certain edition-specific duplicate entries
- Extracting game release years

### 2. Feature Extraction

Three separate TF-IDF representations are created:

- Genres
- Game descriptions
- Platforms

TF-IDF converts the text-ased ame info into numerical feature vectors

### 3. Similarity Calculation

Cosine similarity is used to compare the selected game against the rest of the dataset.

The recommendation score comines these three similarity measurements:

- Genre Similarity: 30%
- Description Similarity: 60%
- Platform Similarity: 10%

### 4. Filtering

Before the final recommendations are returned, users can filter the results by customizing:

- Minimum game rating
- Platform
- Genre
- Minimum release year

### 5. Ranking

Games are ranked according to their final weighted similarity score, and the highest-scoring eligible games are returned.

## Tech Stack

- Python
- Pandas
- scikit-learn
- Streamlit
- TF-IDF
- Cosine similarity
- RAWG API
- Git / GitHub

## Project Structure

```text
GameRecommendationEngine/
│
├── .streamlit/
│   └── config.toml
├── data/
│   └── backloggd_games.csv
│
├── src/
│   ├── cover_art.py
│   ├── evaluate.py
│   ├── load_data.py
│   ├── recommend.py
│   └── ui.py
│
├── app.py
├── main.py
├── requirements.txt
├── .env
└── README.md