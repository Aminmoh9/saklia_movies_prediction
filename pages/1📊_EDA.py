import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Backend import get_daily_rentals, get_store_benefit, get_top_movies, get_unique_movies_rented
from UI_components import render_sidebar_navigation
import plotly.express as px
import plotly.graph_objects as go

# Navigation
# Fake sidebar title inside main page content
#st.sidebar.markdown("## 🎬 Sakila DVD Rental")
render_sidebar_navigation()

st.title("📊 Exploratory Data Analysis")

# Load data with loading states
with st.spinner("Loading rental data..."):
    daily_rentals = get_daily_rentals()
with st.spinner("Loading store benefits..."):
    store_benefit = get_store_benefit()
with st.spinner("Loading top movies..."):
    top_movies = get_top_movies()

# Check if data was loaded successfully
if daily_rentals.empty or store_benefit.empty or top_movies.empty:
    st.error("❌ Failed to load data from database. Please check your database connection.")
    st.stop()

# Add some summary statistics
st.subheader("📈 Summary Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    if not daily_rentals.empty:
        total_rentals = daily_rentals['rental_count'].sum()
        st.metric("Total Rentals (2005)", f"{total_rentals:,}")

with col2:
    if not store_benefit.empty:
        total_benefit = store_benefit['benefit'].sum()
        st.metric("Total Benefit", f"${total_benefit:,.2f}")

with col3:
    if not top_movies.empty:
        unique_movies_count = get_unique_movies_rented()
        st.metric("Unique Movies Rented (2005)", unique_movies_count)

st.markdown("#####")




# Line plot of daily rentals
# st.subheader("Daily Rentals by Store in 2005")

# if not daily_rentals.empty:
#     # Pivot the data for easier plotting
#     daily_pivot = daily_rentals.pivot_table(
#         values='rental_count', 
#         index='rental_date', 
#         columns='store_id', 
#         fill_value=0
#     )
    
#     fig, ax = plt.subplots(figsize=(10, 4))
#     for store_id in daily_pivot.columns:
#         ax.plot(daily_pivot.index, daily_pivot[store_id], 
#                 label=f'Store {store_id}', linewidth=2)
    
#     ax.set_xlabel('Date')
#     ax.set_ylabel('Number of Rentals')
#     ax.set_title('Daily Rentals by Store in 2005')
#     ax.legend()
#     ax.grid(True, alpha=0.3)
#     plt.xticks(rotation=45)
#     st.pyplot(fig)
# else:
#     st.warning("No rental data available for 2005")


#Plotly

daily_pivot = daily_rentals.pivot_table(
    values='rental_count', 
    index='rental_date', 
    columns='store_id', 
    fill_value=0
).reset_index()

daily_pivot.columns = [str(int(col)) if isinstance(col, float) or isinstance(col, int) else col for col in daily_pivot.columns]
daily_pivot_melted = daily_pivot.melt(id_vars='rental_date', var_name='Store', value_name='Rentals')

fig = px.line(
    daily_pivot_melted, 
    x='rental_date', y='Rentals', color='Store',
    title='📅 Daily Rentals by Store in 2005',
    labels={'rental_date': 'Date', 'Rentals': 'Number of Rentals'},
    template='plotly_white',
    color_discrete_map={
        '1': "#1faab4",  
        '2': "#f67fa3"   
    }
)
fig.update_traces(line=dict(width=2))
fig.update_layout(
    title_font_size=28,
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    xaxis_title_font=dict(size=16),
    yaxis_title_font=dict(size=16),
    legend_title_font=dict(size=14),
    legend_font=dict(size=14),
    font=dict(size=14),  # General font size
    margin=dict(t=40, b=20)
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("######")




# Bar plot of total benefit
# st.subheader("Total Benefit by Store")

# # Check if data is available
# if not store_benefit.empty:
#     # Create figure and axis
#     fig, ax = plt.subplots(figsize=(6, 4))  # Slightly larger for better readability

#     # Bar plot with custom colors
#     bars = ax.bar(store_benefit['store_id'].astype(str), store_benefit['benefit'],
#                   color=['skyblue', 'lightcoral'], alpha=0.8, width=0.6)

#     # Axis labels and title with font size
#     ax.set_xlabel('Store', fontsize=10)
#     ax.set_ylabel('Total Benefit ($)', fontsize=10)
#     ax.set_title('Total Benefit by Store', fontsize=12)

#     # Set font size for tick labels on both axes
#     ax.tick_params(axis='x', labelsize=9)
#     ax.tick_params(axis='y', labelsize=9)

    # Rotate x-axis labels if needed
    #plt.xticks(rotation=45)

    # Add gridlines
    # ax.yaxis.grid(True, linestyle='--', alpha=0.4)

    # # Add value labels on bars
    # for bar in bars:
    #     height = bar.get_height()
    #     ax.text(bar.get_x() + bar.get_width()/2., height,
    #             f'${height:,.0f}', ha='center', va='bottom', fontsize=9)

    # # Tight layout to prevent clipping
    # fig.tight_layout()

    # # Display plot in Streamlit
    # st.pyplot(fig)

# else:
#     st.warning("No benefit data available")

#plotly
fig = go.Figure()

colors = ["#1faab4", "#f67fa3"]  # Blue and orange—clean and professional

for i, row in store_benefit.iterrows():
    store_label = f"Store {int(row['store_id'])}"  
    fig.add_trace(go.Bar(
        x=[store_label],
        y=[row['benefit']],
        marker_color=colors[i],
        text=f"${row['benefit']:,.0f}",
        textposition='outside',
        name=store_label
    ))

fig.update_layout(
    title='💰 Total Benefit by Store',
    xaxis_title='Store',
    yaxis_title='Total Benefit ($)',
    xaxis=dict(tickfont=dict(size=14)),
    yaxis=dict(tickfont=dict(size=14)),
    template='plotly_white',
    showlegend=False,
    margin=dict(t=40, b=20),
    title_font_size=28,
    xaxis_title_font=dict(size=16),
    yaxis_title_font=dict(size=16),
    font=dict(size=14)
)

st.plotly_chart(fig, use_container_width=True)



# Top 5 most rented movies by store
st.subheader("Top 5 Most Rented Movies by Store in 2005")

if not top_movies.empty:
    for store_id in top_movies['store_id'].unique():
        st.write(f"**Store {store_id}**")
        store_data = top_movies[top_movies['store_id'] == store_id].head(5)
        
        # Display as a nice table
        display_df = store_data[['title', 'rental_count']].copy()
        display_df['rental_count'] = display_df['rental_count'].astype(int)
        display_df = display_df.rename(columns={
            'title': 'Movie Title',
            'rental_count': 'Rental Count'
        })
        
        st.dataframe(display_df.reset_index(drop=True), use_container_width=True)
        st.write("")  # Add some space
else:
    st.warning("No top movies data available")

