import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from sqlalchemy import create_engine

# ---------------- Supabase engine ---------------- #
def create_db_engine():
    """
    Create SQLAlchemy engine for Supabase PostgreSQL using Streamlit secrets
    """
    try:
        # Get the connection string from Streamlit secrets
        connection_string = st.secrets.get("SUPABASE_CONNECTION_STRING")
        if not connection_string:
            raise ValueError("SUPABASE_CONNECTION_STRING not found in Streamlit secrets")

        return create_engine(connection_string)
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return None

@st.cache_resource
def get_engine():
    """Cache and reuse the Supabase engine"""
    return create_db_engine()

# ---------------- Query functions ---------------- #

@st.cache_data
def get_daily_rentals():
    engine = get_engine()
    if engine is None:
        return pd.DataFrame()
    try:
        query = """
        SELECT 
            DATE(r.rental_date) as rental_date,
            i.store_id,
            COUNT(r.rental_id) as rental_count
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        WHERE EXTRACT(YEAR FROM r.rental_date) = 2005
        GROUP BY DATE(r.rental_date), i.store_id
        ORDER BY rental_date, store_id
        """
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Error fetching daily rentals: {e}")
        return pd.DataFrame()

@st.cache_data
def get_store_benefit():
    engine = get_engine()
    if engine is None:
        return pd.DataFrame()
    try:
        query = """
        SELECT 
            i.store_id,
            SUM(p.amount) as benefit
        FROM payment p
        JOIN rental r ON p.rental_id = r.rental_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        GROUP BY i.store_id
        ORDER BY store_id
        """
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Error fetching store benefits: {e}")
        return pd.DataFrame()

@st.cache_data
def get_top_movies():
    engine = get_engine()
    if engine is None:
        return pd.DataFrame()
    try:
        query = """
        WITH store_rentals AS (
            SELECT 
                i.store_id,
                f.film_id,
                f.title,
                COUNT(r.rental_id) as rental_count,
                ROW_NUMBER() OVER (PARTITION BY i.store_id ORDER BY COUNT(r.rental_id) DESC) as rank
            FROM rental r
            JOIN inventory i ON r.inventory_id = i.inventory_id
            JOIN film f ON i.film_id = f.film_id
            WHERE EXTRACT(YEAR FROM r.rental_date) = 2005
            GROUP BY i.store_id, f.film_id, f.title
        )
        SELECT store_id, film_id, title, rental_count
        FROM store_rentals
        WHERE rank <= 5
        ORDER BY store_id, rental_count DESC
        """
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Error fetching top movies: {e}")
        return pd.DataFrame()

@st.cache_data
def get_movie_database():
    engine = get_engine()
    if engine is None:
        return pd.DataFrame()
    try:
        query = """
        SELECT 
            f.film_id,
            f.title,
            f.description,
            f.rating
        FROM film f
        WHERE f.description IS NOT NULL AND f.description != ''
        ORDER BY f.title
        """
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Error fetching movie database: {e}")
        return pd.DataFrame()

@st.cache_data
def get_unique_movies_rented():
    engine = get_engine()
    if engine is None:
        return 0
    try:
        query = """
        SELECT COUNT(DISTINCT i.film_id) as unique_movies_rented
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        WHERE EXTRACT(YEAR FROM r.rental_date) = 2005
        """
        result = pd.read_sql(query, engine)
        return result['unique_movies_rented'].iloc[0] if not result.empty else 0
    except Exception as e:
        st.error(f"Error fetching unique movies rented: {e}")
        return 0

# ---------------- NLP Model ---------------- #

@st.cache_resource
def get_sentence_model():
    """Load the sentence transformer model"""
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource
def get_movie_embeddings():
    """Cache movie descriptions and their embeddings"""
    movie_db = get_movie_database()
    if movie_db.empty:
        return pd.DataFrame(), np.array([])
    
    model = get_sentence_model()
    movie_descriptions = movie_db['description'].fillna('').astype(str).tolist()
    embeddings = model.encode(movie_descriptions, normalize_embeddings=True)
    return movie_db, embeddings

def find_similar_movies(query, top_n=3):
    """Find top N similar movies based on a query description"""
    if not query.strip():
        return []

    movie_db, movie_embeddings = get_movie_embeddings()
    if movie_db.empty:
        st.error("Movie database is empty!")
        return []

    model = get_sentence_model()
    input_embedding = model.encode([query], normalize_embeddings=True)
    similarities = cosine_similarity(input_embedding, movie_embeddings)[0]

    top_indices = similarities.argsort()[-top_n:][::-1]
    results = []
    for idx in top_indices:
        movie = movie_db.iloc[idx]
        results.append((movie['title'], movie['rating'], similarities[idx]))

    return results
