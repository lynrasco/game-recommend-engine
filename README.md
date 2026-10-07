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


## Technical Highlights

- Built a content-based recommendation system using TF-IDF and cosine similarity
- Uses three independent feature representations for genre, description, and platform
- Combines similarity scores using a configurable weighted scoring model
- Applies user-selected filters before ranking recommendations
- Uses Streamlit caching to avoid repeatedly preprocessing the dataset
- Integrates the RAWG API to dynamically retrieve game artwork
- Provides recommendation explanations using shared genres and feature similarity
- Separates data loading, recommendation logic, evaluation, artwork retrieval, and UI components into dedicated modules
- Includes a reproducible evaluation script for testing recommendation similarity


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

TF-IDF converts the text-based game info into numerical feature vectors.

Description similarity receives the highest weight because game descriptions provide more detailed information about gameplay and themes, while genre and platform provide additional contextual signals.

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
| `src/evaluate.py` | Evaluation of recommendation similarity and unique genre coverage |

## Evaluation

The recommendation system was evaluated using a small test set of 10 games covering different genres and game types.

The evaluation measures:

- Average weighted similarity of the top 5 recommendations
- Number of unique genres represented across the recommendations

| Test Game | Average Weighted Similarity | Unique Genres |
|---|---:|---:|
| Undertale | 0.42 | 5 |
| Hades | 0.44 | 5 |
| Elden Ring | 0.50 | 2 |
| Hollow Knight | 0.43 | 3 |
| Celeste | 0.42 | 3 |
| Minecraft | 0.52 | 2 |
| Portal 2 | 0.48 | 5 |
| Resident Evil 4 | 0.62 | 3 |
| Persona 5 Royal | 0.41 | 3 |
| Stray | 0.44 | 2 |

The results show that the system generally produces recommendations with moderate to high similarity to the selected game. Resident Evil 4 produced the highest average similarity at 0.62, while Persona 5 Royal produced the lowest at 0.41.

This evaluation is primarily a consistency check of the content-based recommendation system rather than a measure of user satisfaction or recommendation accuracy. A larger evaluation dataset and human/user-based evaluation would provide a stronger measure of recommendation quality.

The evaluation can be reproduced using the command:

```bash
python -m src.evaluate
```

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