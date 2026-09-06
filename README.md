# 🎬 CineMatch — Movie Recommendation System

**CineMatch** is an interactive, content-based movie recommendation application built with Python and Streamlit. Designed to simplify content discovery, CineMatch leverages machine learning and metadata similarity algorithms to analyze film characteristics—such as genres, language, production studios, and directors—delivering instant, tailored film suggestions based on user preferences.

---

## 📁 Repository Structure

```text
.
├── app.py                                  # Main Streamlit web application & UI logic
├── recommender.py                          # Recommendation algorithm & vector calculations
├── Letterbox Movie Classification Dataset.csv # Movie catalog dataset
├── dataset-links.txt                       # Source links for datasets
└── requirements.txt                       # Required Python dependencies

```

---

## 🛠️ Prerequisites & Setup

### 1. Prerequisites

* **Python 3.9+** installed on your machine.
* A free **TMDB (The Movie Database) API Key** to fetch real-time poster artwork.
*(Get one at [themoviedb.org](https://www.themoviedb.org/settings/api)).*

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/cinematch.git
cd cinematch

```

### 3. Create a Virtual Environment (Optional but Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

```

### 4. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## 🔑 TMDB API Key Setup

1. Open `app.py` in your code editor.
2. Locate the API key variable near the top:
```python
TMDB_API_KEY = "YOUR_API_KEY_HERE"

```


3. Replace `"YOUR_API_KEY_HERE"` with your TMDB v3 API key string.

---

## 🚀 How to Run the Program

Launch the web application via Streamlit:

```bash
streamlit run app.py

```

Your browser will automatically open a tab at `http://localhost:8501`.

---

## 🍿 Features

* **Smart Matching:** Generates top 10 recommendations using multi-feature similarity (genres, languages, directors).
* **Single-Screen UI:** Compact grid layout engineered to eliminate vertical scrolling.
* **Custom Theme Switcher:** Fully styled toggle switch to flip between Dark and Light modes.
* **Interactive Modal Overlays:** Click **View Details** on any card to inspect ratings, view counts, studios, directors, and plot synopses.

* This project is completely vibecoded
