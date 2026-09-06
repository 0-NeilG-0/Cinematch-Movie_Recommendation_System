import streamlit as st
import requests
import pandas as pd
from recommender import load_data, preprocess_data, create_feature_vectors, recommend_movies

# --- API Setup ---
TMDB_API_KEY = "YOUR_API_KEY_HERE"  # Keep your TMDB API key here

def fetch_poster(movie_title):
    """Fetches the movie poster URL from TMDB API."""
    if TMDB_API_KEY == "YOUR_API_KEY_HERE" or TMDB_API_KEY == "---" or not TMDB_API_KEY:
        return "https://placehold.co/500x750/111111/FFFFFF/png?text=API+Key\nNeeded"
        
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": movie_title}
    
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                poster_path = data['results'][0].get('poster_path')
                if poster_path:
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        pass
    
    return "https://placehold.co/500x750/111111/FFFFFF/png?text=No+Poster\nFound"

def inject_custom_css(theme):
    """Injects custom CSS to modernize and polish the UI dynamically based on theme."""
    if theme == "dark":
        app_bg = "#0E1117"
        text_color = "#FAFAFA"
        card_bg = "rgba(255, 255, 255, 0.02)"
        card_border = "rgba(255, 255, 255, 0.06)"
        card_hover_bg = "rgba(255, 255, 255, 0.04)"
    else:
        app_bg = "#F4F6F9"
        text_color = "#111111"
        card_bg = "#FFFFFF"
        card_border = "rgba(0, 0, 0, 0.1)"
        card_hover_bg = "#E9ECEF"

    st.markdown(f"""
        <style>
        /* Hide default Streamlit header and footer */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Force App Background and Text Color */
        [data-testid="stAppViewContainer"], div[role="dialog"] {{
            background-color: {app_bg} !important;
            color: {text_color} !important;
        }}
        
        /* Ensure all standard text adopts the theme */
        .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{
            color: {text_color} !important;
        }}

        /* Adjust page margins */
        .block-container {{
            padding-top: 1rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }}

        /* Poster Image Enhancements */
        [data-testid="stImage"] img {{
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            object-fit: cover;
        }}
        
        [data-testid="stImage"] img:hover {{
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 12px 24px rgba(229, 9, 20, 0.35);
        }}

        /* Movie Card Container styling */
        div[data-testid="column"] {{
            background-color: {card_bg};
            border: 1px solid {card_border};
            border-radius: 14px;
            padding: 12px;
            transition: border-color 0.25s ease, background-color 0.25s ease;
        }}
        
        div[data-testid="column"]:hover {{
            border-color: rgba(229, 9, 20, 0.4);
            background-color: {card_hover_bg};
        }}

        /* Button Styling */
        div.stButton > button {{
            border-radius: 8px;
            border: 1px solid #E50914;
            background-color: transparent;
            color: {text_color};
            font-weight: 500;
            width: 100%;
            transition: all 0.2s ease;
        }}
        
        div.stButton > button:hover {{
            background-color: #E50914;
            color: #FFFFFF !important;
            border-color: #E50914;
            box-shadow: 0 4px 12px rgba(229, 9, 20, 0.4);
        }}
        </style>
    """, unsafe_allow_html=True)

# --- Popup Dialog Function ---
@st.dialog("🎬 Movie Details", width="large")  
def show_movie_details(movie, poster_url):
    """Displays a modal popup with detailed movie info."""
    col1, col2 = st.columns([1, 1.8])  
    
    with col1:
        st.image(poster_url, use_container_width=True)
        
    with col2:
        st.markdown(f"## {movie['name']}")
        st.caption(f"🎭 **Genres:** {movie['genre_display']}")
        
        st.divider()
        
        # Metric indicators
        mcol1, mcol2, mcol3 = st.columns(3)
        with mcol1:
            st.metric("Rating", f"{movie['rating']:.2f} ⭐")
        with mcol2:
            watches = int(movie['Watches']) if pd.notnull(movie['Watches']) else 0
            st.metric("Views", f"{watches:,}")
        with mcol3:
            st.metric("Language", str(movie['language']).upper())
            
        st.write("") 
        
        studios = str(movie['Studios']).replace("[", "").replace("]", "").replace("'", "")
        st.markdown(f"**🏢 Studio:** {studios}")
        st.markdown(f"**🎬 Director:** {movie['Director']}")

    st.divider()
    st.markdown("### Synopsis")
    st.write(movie['Description'])

# --- UI Configuration ---
st.set_page_config(page_title="CineMatch | AI Movie Recommender", page_icon="🎬", layout="wide") 

# Theme state management
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

# Top Right Theme Toggle
_, theme_col = st.columns([10, 1])
with theme_col:
    button_label = "☀️" if st.session_state.theme == "dark" else "🌙"
    st.button(button_label, on_click=toggle_theme, key="theme_toggle")

# Inject custom styling based on active theme
inject_custom_css(st.session_state.theme)

# Hero Header (with dynamic subtitle color)
subtitle_color = "#888888" if st.session_state.theme == "dark" else "#555555"
st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>🎬 CineMatch</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: {subtitle_color}; font-size: 1.1rem; margin-bottom: 30px;'>Discover personalized recommendations powered by metadata similarity matching</p>", unsafe_allow_html=True)

@st.cache_data
def get_processed_data():
    df = load_data()
    if df is not None:
        df = preprocess_data(df)
    return df

df = get_processed_data()

if df is None:
    st.error(r"Dataset not found! Ensure 'Letterbox Movie Classification Dataset.csv' is saved in the correct folder.")
else:
    movie_names = df['name'].sort_values().tolist()
    director_names = df['Director'].dropna().unique()

    # Inputs layout
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            selected_movies = st.multiselect("🎬 Select movies you like:", options=movie_names, placeholder="Search movies...")
        with col2:
            selected_directors = st.multiselect("🎥 Select preferred directors:", options=director_names, placeholder="Search directors...")

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        get_rec_btn = st.button("✨ Get Recommendations", type="primary", use_container_width=True)

    # Recommendation Trigger
    if get_rec_btn:
        if len(selected_movies) == 0 and len(selected_directors) == 0:
            st.warning("Please select at least one movie or director to get recommendations.")
        else:
            with st.spinner('Analyzing catalog metadata...'):
                feature_matrix = create_feature_vectors(df)
                recommendations = recommend_movies(selected_movies, selected_directors, df, feature_matrix, top_n=10)
                if recommendations is not None and not recommendations.empty:
                    st.session_state['recommendations'] = recommendations.to_dict('records')
                else:
                    st.session_state['recommendations'] = []

    st.markdown("<hr style='margin: 2rem 0; border-color: rgba(150,150,150,0.2);'>", unsafe_allow_html=True)

    # Display Grid
    if 'recommendations' in st.session_state:
        recommended_movies_list = st.session_state['recommendations']
        
        if recommended_movies_list:
            st.markdown("### 🍿 Top Recommendations For You")
            
            for row_idx in range(2): 
                cols = st.columns(5) 
                for col_idx in range(5):
                    movie_idx = row_idx * 5 + col_idx
                    
                    if movie_idx < len(recommended_movies_list):
                        movie = recommended_movies_list[movie_idx]
                        title = movie['name']
                        poster_url = fetch_poster(title)
                        
                        with cols[col_idx]:
                            st.image(poster_url, use_container_width=True)
                            
                            # Truncated title string for long titles
                            st.markdown(f"<p style='font-weight: 600; margin-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{title}</p>", unsafe_allow_html=True)
                            st.caption(f"⭐ {movie['rating']:.2f} | {str(movie['language']).upper()}")
                            
                            if st.button("View Details", key=f"btn_{movie_idx}_{title}"):
                                show_movie_details(movie, poster_url)
        else:
            st.info("No recommendations found matching your selections.")
    else:
        st.info("💡 Select movies or directors above and click **Get Recommendations** to generate your list.")