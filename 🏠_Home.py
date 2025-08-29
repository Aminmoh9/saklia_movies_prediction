import streamlit as st
from UI_components import render_sidebar_navigation
from Backend import create_db_engine, get_movie_database
from sqlalchemy import text

# Page config
st.set_page_config(
    page_title="Sakila DVD Rental Analysis",
    page_icon="🎬",
    layout="wide"
)

# Navigation
# Fake sidebar title inside main page content
#st.sidebar.markdown("## 🎬 Sakila DVD Rental")
render_sidebar_navigation()

# Main content
st.title("🎬 Sakila DVD Rental Store Analysis")

# Quick connection check 
try:
    engine = create_db_engine()
    if engine:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        st.success("✅ Successfully connected to Sakila database")
except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
    st.info("Please check your database configuration in the .env file")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Welcome to Sakila DVD Rental Analysis")
    st.write("""
    This application provides comprehensive analysis of the Sakila DVD rental store operations.
    
    **Features include:**
    - 📊 **EDA Analysis**: Explore rental patterns and store performance
    - 📈 **Visualizations**: Daily rentals, store benefits, and top movies
    - 🔮 **Movie Recommendations**: Find similar movies based on description
    - 🎯 **Real-time Data**: Direct connection to MySQL Sakila database
    
    Use the navigation sidebar to explore different sections of the analysis.
    """)
    
    st.subheader("About Sakila Database")
    st.write("""
    The Sakila database is a sample database provided by MySQL that represents a DVD rental store:
    - **16 Tables** including film, customer, rental, payment, etc.
    - **1,000 Films** with descriptions, ratings, and categories
    - **2 Stores** with complete rental history
    - **Sample Data** from 2005-2006 period
    """)
    
    # Show some quick stats
    try:
        movie_db = get_movie_database()
        if not movie_db.empty:
            st.metric("Movies in Database", len(movie_db))
    except:
        pass

with col2:
    # ADDED IMAGE HERE - DVD rental store image
    st.image("https://images.unsplash.com/photo-1598899134739-24c46f58b8c0?w=400&h=500&fit=crop", 
             caption="DVD Rental Store", 
             width='stretch')
    
    st.info("""
    **Getting Started:**
    1. Check EDA for data insights
    2. Use Predictions for movie recommendations
    3. Ensure your .env file is configured
    """)

# Add another image below the main content for better visual appeal
st.markdown("---")
st.subheader("📀 Our Movie Collection")

# Add multiple images in a grid
col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://images.unsplash.com/photo-1489599102910-59206b8ca314?w=300&h=200&fit=crop",
             caption="Action Movies Collection",
             width='stretch')
    st.image("https://images.unsplash.com/photo-1478720568477-b840004f9ac5?w=300&h=200&fit=crop",
             caption="Classic Films",
             width='stretch')
         
             

with col3:
    st.image("https://images.unsplash.com/photo-1542204165-65bf26472b9b?w=300&h=200&fit=crop",
             caption="New Releases",
             width='stretch')

# Add system requirements
with st.expander("⚙️ System Requirements"):
    st.write("""
    - Python 3.8+
    - MySQL Server with Sakila database
    - Required packages (see requirements.txt)
    - .env file with database credentials
    """)
    
    # Add a technical image
    st.image("https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=400&h=200&fit=crop",
             caption="Database Technology",
             width='stretch')