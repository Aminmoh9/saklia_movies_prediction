import streamlit as st
from Backend import get_movie_database, find_similar_movies
#from UI_components import render_sidebar_navigation

# Navigation
# Fake sidebar title inside main page content

#render_sidebar_navigation()

st.title("🔮 Movie Recommendation System")

st.write("""
Enter a movie description below and get the top 3 most similar movies from our database.
The system uses advanced natural language processing to find matches based on content.
""")

# Check if movie database is available
with st.spinner("Loading movie database..."):
    movie_db = get_movie_database()

if movie_db.empty:
    st.error("❌ Could not load movie database. Please check your database connection.")
    st.info("Make sure the Sakila database is installed and contains the 'film' table.")
    st.stop()

# Show some stats
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Movies", len(movie_db))
with col2:
    st.metric("Unique Ratings", movie_db['rating'].nunique())

# Text area for movie description input
movie_description = st.text_area(
    "Enter a movie description:",
    height=150,
    placeholder="Describe a movie you're interested in...\nExample: 'A space adventure with aliens and spaceships'",
    help="Be as descriptive as possible for better results"
)

# Add examples for quick testing
st.caption("💡 Try these examples:")
examples = st.columns(3)
with examples[0]:
    if st.button("Space Adventure", width="stretch"):
        st.session_state.movie_desc = "A space adventure with aliens and spaceships"
with examples[1]:
    if st.button("Romantic Drama", width="stretch"):
        st.session_state.movie_desc = "A romantic story about two people falling in love"
with examples[2]:
    if st.button("Action Hero", width="stretch"):
        st.session_state.movie_desc = "An action hero saving the world from villains"

# Initialize session state
if 'movie_desc' not in st.session_state:
    st.session_state.movie_desc = ""

# Use session state value if set
if st.session_state.movie_desc:
    movie_description = st.session_state.movie_desc

if st.button("🎯 Get Your Prediction", type="primary"):
    if movie_description.strip():
        with st.spinner("Finding similar movies..."):
            # Get similar movies
            similar_movies = find_similar_movies(movie_description)
            
            if similar_movies:
                # Display results
                st.subheader("🎬 Top 3 Similar Movies:")
                
                for i, (title, rating, similarity) in enumerate(similar_movies, 1):
                    # Create columns for better layout
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{i}. {title}**")
                        # Get the full description from database
                        movie_desc = movie_db[movie_db['title'] == title]['description'].iloc[0]
                        st.caption(f"*{movie_desc}*")
                    
                    with col2:
                        # Color code ratings
                        rating_color = {
                            'G': 'green',
                            'PG': 'blue',
                            'PG-13': 'orange',
                            'R': 'red',
                            'NC-17': 'darkred'
                        }.get(rating, 'gray')
                        st.markdown(f"<span style='color: {rating_color}; font-weight: bold;'>Rating: {rating}</span>", 
                                  unsafe_allow_html=True)
                    
                    with col3:
                        # Color code similarity score
                        similarity_color = "green" if similarity > 0.7 else "orange" if similarity > 0.5 else "red"
                        st.markdown(f"<span style='color: {similarity_color}; font-weight: bold;'>Similarity: {similarity:.3f}</span>", 
                                  unsafe_allow_html=True)
                    
                    st.divider()
            else:
                st.warning("No similar movies found. Try a different description.")
    else:
        st.warning("Please enter a movie description to get recommendations.")

# Show sample of available movies
with st.expander("📋 Browse Available Movies"):
    st.dataframe(
        movie_db[['title', 'rating', 'description']].head(10),
        width="stretch",
        hide_index=True
    )
    st.caption(f"Showing 10 of {len(movie_db)} available movies")
