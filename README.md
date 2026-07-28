# 🎬 Movie Recommendation System

An interactive Movie Recommendation System built using **Python**, **Machine Learning**, and **Flask**. The model suggests similar movies based on content-based filtering using cosine similarity.

---

## 🛠️ Tech Stack & Tools

* **Programming Language:** Python
* **ML Libraries:** Pandas, NumPy, Scikit-Learn
* **Data Source:** TMDB 5000 Movie Dataset
* **Web Framework:** Flask / HTML / CSS
* **Model Serialization:** Pickle (`.pkl`)

---

## 🚀 Features

* Select or search for any movie from the dataset.
* Get top 5 recommended movies based on metadata (genres, keywords, cast, crew).
* Fast recommendation generation using pre-computed Cosine Similarity matrix.

---

## 📁 Project Structure

```text
RJS-movies-recommender/
│
├── app.py                      # Main application script
├── RJS-movies-recommender.ipynb # Jupyter notebook with model training logic
├── templates/                  # Web templates (HTML)
├── static/                     # CSS / JS static assets
├── requirements.txt            # Project dependencies
└── .gitignore                  # Git ignore rules
