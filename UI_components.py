import streamlit as st
from sqlalchemy import text

def render_sidebar_navigation():
    #st.sidebar.title("🎬 Sakila DVD Rental")


    # Use your actual filenames with emojis
    # st.sidebar.page_link("🏠_Home.py", label="Home", icon="🏠")
    # st.sidebar.page_link("pages/1📊_EDA.py", label="EDA Analysis", icon="📊")
    # st.sidebar.page_link("pages/2📈_Predictions.py", label=" Movie Recommendations", icon="🔮")
    
    #st.sidebar.markdown("---")
    
    # Add database connection status - FIXED with text()
    try:
        from Backend import create_db_engine
        engine = create_db_engine()
        if engine:
            with engine.connect() as conn:
                # FIXED: Use text() for SQL execution
                conn.execute(text("SELECT 1"))
            st.sidebar.success("✅ Database Connected")
        else:
            st.sidebar.error("❌ Database Offline")
    except Exception as e:
        st.sidebar.error(f"❌ Database Offline: {str(e)}")
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Sakila DVD Rental Analysis**  
    Built with Streamlit  
    Data from MySQL Sakila Database
    """)
    
    # Add quick actions
    st.sidebar.markdown("### Quick Actions")
    if st.sidebar.button("🔄 Refresh Data", help="Reload all data from database"):
        st.rerun()