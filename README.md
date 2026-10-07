# Game Recommendation Engine
A content-based game recommendation system built using Python, Pandas, scikit-learn, and Streamlit

This application helps recommend games to users based on similarities in genre, description, and platform. Users can search for a game, customize recommendation filters, or use the 'Surprise Me' feature to randomize a game that matches their criteria.

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

## How It Works

The recommendation system uses a content-based filtering approach

### 1. Data Preprocessing

The game dataset (CSV file) is cleaned before recommendations are generated

Includes:

- Removing unnecessary columns, and duplicate game titles
- Handling empty descriptions
- Parsing platform and genre data
- Removing certain edition-specific duplicate entries
- Extracting game release years

### 2. Feature Extraction

Three separate TF-IDF representations are created:

| Feature | Weight |
|---|---:|
| Genre | 30% |
| Description | 60% |
| Platform | 10% |

TF-IDF converts the text-based game info into numerical feature vectors

### 3. Similarity Calculation

Cosine similarity is used to compare the selected game against the rest of the dataset.

The recommendation score combines these three similarity measurements:

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

## Project Structure & Architecture

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
└── README.md
```

The application is divided into several components:

| File | Responsibility |
|---|---|
| `app.py` | Streamlit application, user interaction, and recommendation workflow |
| `src/load_data.py` | Dataset loading and preprocessing |
| `src/recommend.py` | TF-IDF matrices, similarity calculations, filtering, and ranking |
| `src/ui.py` | Recommendation cards and recommendation explanations |
| `src/cover_art.py` | RAWG API integration for game artwork |
| `src/evaluate.py` | Evaluation of recommendation quality |

## Evaluation

The recommendation system was evaluated using a small set of test games across different genres and game types

Examples of games included:
- Undertale
- Hades
- Elden Ring
- Hollow Knight
- Celeste
- Minecraft
- Portal 2
- Resident Evil 4
- Persona 5 Royal
- Stray

This evaluation examines recommendation similarity and genre diversity across the test set.

## Setup

### 1. Clone this repository

```bash
git clone https://github.com/lynrasco/game-recommend-engine.git
cd GameRecommendationEngine
```

### 2. Install necessary dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure RAWG API

Create a .env file in the project root:

```bash
RAWG_API_KEY=api_key_here
```

### 4. Running the application

```bash
streamlit run app.py
```

## Limitations & Future Improvements

This current system uses metadata-based content similarity.
As a result, games with overlapping genre labels can receive
high genre similarity even when their gameplay experiences
differ significantly.

Potential improvements include:

- Incorporating user ratings and play history
- Adding game tags and keywords
- Including developer and publisher information
- Experimenting with different feature weights
- Using semantic embeddings for game descriptions
- Expanding the evaluation dataset
- Comparing the content-based approach with collaborative filtering