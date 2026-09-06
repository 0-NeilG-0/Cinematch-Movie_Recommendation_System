import pandas as pd
import numpy as np
import ast
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data(filepath=r'Letterbox Movie Classification Dataset.csv'):
    """Loads the Letterbox dataset and renames standard columns."""
    try:
        df = pd.read_csv(filepath)
        df = df.rename(columns={
            'Film_title': 'name', 
            'Genres': 'genre', 
            'Average_rating': 'rating', 
            'Original_language': 'language',
            'Director': 'Director'
        })
        return df
    except FileNotFoundError:
        return None

def preprocess_data(df):
    """Cleans data, drops duplicates, and prepares list formats."""
    df = df.dropna(subset=['name', 'genre', 'language', 'Director']).copy()
    df = df.drop_duplicates(subset=['name'])
    
    # Fill missing values for the new popup columns so the app doesn't crash
    df['Description'] = df['Description'].fillna("No description available.")
    df['Studios'] = df['Studios'].fillna("Unknown")
    df['Watches'] = df['Watches'].fillna(0)
    
    def parse_genres(g_str):
        try:
            return ast.literal_eval(g_str)
        except (ValueError, SyntaxError):
            return []
            
    df['genre_list'] = df['genre'].apply(parse_genres)
    df['lang_list'] = df['language'].astype(str).apply(lambda x: [x.strip()])
    df['director_list'] = df['Director'].astype(str).apply(lambda x: [x.strip()])
    df['genre_display'] = df['genre_list'].apply(lambda x: ", ".join(x))
    
    df = df.reset_index(drop=True)
    return df

def create_feature_vectors(df):
    """Creates a unified matrix containing multi-hot encoding for Genres, Languages, and Directors."""
    mlb_genre = MultiLabelBinarizer()
    genre_matrix = mlb_genre.fit_transform(df['genre_list'])
    
    mlb_lang = MultiLabelBinarizer()
    lang_matrix = mlb_lang.fit_transform(df['lang_list'])
    
    mlb_director = MultiLabelBinarizer()
    director_matrix = mlb_director.fit_transform(df['director_list'])
    
    combined_matrix = np.hstack([genre_matrix, lang_matrix, director_matrix])
    return combined_matrix

def find_title_pattern_matches(movie_names, df):
    """Finds movies with similar names in the dataset."""
    pattern_matches = []
    for name in movie_names:
        matches = df[df['name'].str.contains(name, case=False)]
        pattern_matches.extend(matches['name'])
    return list(set(pattern_matches))

def recommend_movies(selected_movies, selected_directors, df, feature_matrix, top_n=10):
    """Calculates top recommendations based on selected movies and directors."""
    if not selected_movies and not selected_directors:
        return None
    
    selected_indices = df[df['name'].isin(selected_movies)].index.tolist()
    
    if selected_directors:
        director_indices = df[df['Director'].isin(selected_directors)].index.tolist()
        selected_indices.extend(director_indices)

    if not selected_indices:
        return None
    
    user_vector = feature_matrix[selected_indices].mean(axis=0).reshape(1, -1)
    sim_scores = cosine_similarity(user_vector, feature_matrix).flatten()
    
    df_result = df.copy()
    df_result['similarity'] = sim_scores
        
    df_result = df_result[~df_result['name'].isin(selected_movies)]
    if selected_directors:
        df_result = df_result[~df_result['Director'].isin(selected_directors)]
    
    title_pattern_matches = find_title_pattern_matches(selected_movies, df)
    title_filtered_df = df_result[df_result['name'].isin(title_pattern_matches)].copy()
    
    # --- ADDED NEW COLUMNS TO THE OUTPUT ---
    output_cols = ['name', 'Director', 'rating', 'genre_display', 'language', 'Description', 'Studios', 'Watches']
    
    if not title_filtered_df.empty:
        title_filtered_df.sort_values(by='similarity', ascending=False, inplace=True)
        top_movies_from_patterns = title_filtered_df.head(top_n // 2)

        remaining_movies = df_result[~df_result['name'].isin(title_pattern_matches)].copy()
        remaining_movies.sort_values(by='similarity', ascending=False, inplace=True)
        
        if len(remaining_movies) < (top_n - len(top_movies_from_patterns)):
            final_recommendations = pd.concat([
                top_movies_from_patterns, 
                remaining_movies.head(top_n - len(top_movies_from_patterns))
            ])
        else:
            remaining_top_movies = remaining_movies.head(top_n - len(top_movies_from_patterns))
            final_recommendations = pd.concat([top_movies_from_patterns, remaining_top_movies])
        
        final_recommendations = final_recommendations.reset_index(drop=True)
        return final_recommendations[output_cols]
    
    top_movies = df_result.sort_values(by='similarity', ascending=False).head(top_n)
    return top_movies[output_cols]