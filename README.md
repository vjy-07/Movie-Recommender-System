# 🎬 Movie Recommender System

This is a **content-based movie recommendation system** built with **Python** and **Streamlit**. It recommends five movies similar to the one you select from a dropdown, using content similarity (like genres, keywords, cast) and displays their posters using **The Movie Database (TMDB) API**.

---

## 🚀 Features

- Recommend 5 similar movies using content-based filtering
- Movie posters fetched dynamically from TMDB API
- Interactive UI using Streamlit
- Uses precomputed similarity matrix for fast results

---

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/vjy-07/Movie-Recommender-System.git
cd Movie-Recommender-System
```

### 🐍 2. (Optional) Create a virtual environment

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```
### 📦 3. Install the required dependencies

```bash
pip install -r requirements.txt
```
### 🔑 4. Set up TMDB API Key

Create a `.env` file in the root directory and add your API key:

```ini
TMDB_API_KEY=your_tmdb_api_key_here
```
### 💻 5. Run the App

Start the Streamlit application using the following command:

```bash
streamlit run app.py
```
### 📁 Project Structure

```
Movie-Recommender-System/
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── .env                    # API key
├── .gitignore              # Ignore venv, .env, model
├── model/
    ├── movie_list.pkl      # Movie data
    └── similarity.pkl      # Similarity matrix
```
### 🧠 How It Works

This project uses **content-based filtering**:

- For each movie, a feature vector is created using metadata like cast, crew, keywords, and genres.
- A cosine similarity matrix is computed between all movies.
- Given a selected movie, the 5 most similar movies are recommended.


