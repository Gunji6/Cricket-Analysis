import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Streamlit App
st.set_page_config(page_title="Player Analytics Dashboard", layout="wide")

# Create a folder to save CSVs if not exists
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)

# File paths
batting_path = os.path.join(data_folder, "batting.csv")
bowling_path = os.path.join(data_folder, "bowling.csv")


# Define file paths
batting_path = "batting_data.csv"
bowling_path = "bowling_data.csv"

# Function to load data based on file type
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith((".xls", ".xlsx")):
        return pd.read_excel(file)
    elif file.name.endswith(".json"):
        return pd.read_json(file)
    else:
        st.error(f"Unsupported file format: {file.name}")
        return None

# Upload only if files are not already saved
if not (os.path.exists(batting_path) and os.path.exists(bowling_path)):
    uploaded_batting = st.sidebar.file_uploader("Import Batting Data File", type=["csv", "xlsx", "xls", "json"], key="batting")
    uploaded_bowling = st.sidebar.file_uploader("Import Bowling Data File", type=["csv", "xlsx", "xls", "json"], key="bowling")
    
    if uploaded_batting and uploaded_bowling:
        batting_df = load_data(uploaded_batting)
        bowling_df = load_data(uploaded_bowling)
        
        # Save only if both files are valid
        if batting_df is not None and bowling_df is not None:
            batting_df.to_csv(batting_path, index=False)
            bowling_df.to_csv(bowling_path, index=False)
            st.success("Files uploaded and saved successfully as CSV!")
else:
    # Load saved CSVs
    batting_df = pd.read_csv(batting_path)
    bowling_df = pd.read_csv(bowling_path)

# Display message when files are loaded successfully
# if 'batting_df' in locals() and 'bowling_df' in locals():
#    st.success("Batting and Bowling Data Loaded Successfully!")


# **NEW: Display message if no data is available**
if 'batting_df' not in locals() or 'bowling_df' not in locals():
    st.title("Welcome to the Cricket Player 🏏 Analytics Dashboard!")
    st.write(" #### Please upload Batting and Bowling CSV files from the sidebar to start the analysis.")
    st.markdown("<p style='text-align: center;'>", unsafe_allow_html=True)
    st.image("Cricket.jpg", width=400)  # Adjust width, height not directly supported
    st.markdown("</p>", unsafe_allow_html=True)
    st.stop()  # Stop execution to prevent errors



# Extract unique teams and players
teams = sorted(set(batting_df['Country'].unique()).union(bowling_df['Country'].unique()))
team = st.sidebar.selectbox("Select Team", teams)

# Filter players by team
batting_players = batting_df[batting_df['Country'] == team]['player_name'].unique()
bowling_players = bowling_df[bowling_df['Country'] == team]['player_name'].unique()
players = sorted(set(batting_players).union(bowling_players))
player = st.sidebar.selectbox("Select Player", players)

# Filter data for the selected player
player_batting = batting_df[(batting_df['player_name'] == player) & (batting_df['Country'] == team)]
player_bowling = bowling_df[(bowling_df['player_name'] == player) & (bowling_df['Country'] == team)]

st.title(f"{player}'s Performance Dashboard")

# Display player data
st.subheader("Player Records")
if not player_batting.empty:
    st.write("### Batting Scorecard")
    st.dataframe(player_batting)
if not player_bowling.empty:
    st.write("### Bowling Scorecard")
    st.dataframe(player_bowling)

# Visualization
# if not player_batting.empty:
#     st.subheader("Batting Figures")
#     col1, col2 = st.columns(2)
    
#     with col1:
#         # Runs by Format - Using Horizontal Bar Chart with High-Contrast Colors
#         fig_bat_runs = px.bar(player_batting, x='Runs', y='Format', orientation='h', 
#                               title='Runs Breakdown Across Format', text='Runs',
#                               color='Runs', color_continuous_scale='magma')
#         fig_bat_runs.update_traces(textposition='outside')
#         st.plotly_chart(fig_bat_runs, use_container_width=True)
    
#     with col2:
#         # Strike Rate by Format - Using Cyan Shade for Visibility
#         fig_bat_sr = px.area(player_batting, x='Format', y='SR', title='Strike Rate Across Formats',
#                              color_discrete_sequence=['#00FFFF'])  # Neon Cyan
#         st.plotly_chart(fig_bat_sr, use_container_width=True)

# if not player_bowling.empty:
#     st.subheader("Bowling Figures")
#     col3, col4 = st.columns(2)
    
#     with col3:
#         # Economy Rate by Format - Lollipop Chart with Vibrant Colors
#         fig_bowl_eco = px.scatter(player_bowling, x='Format', y='Eco', size=[10]*len(player_bowling),
#                                   title='Economy Rate Across Formats', color='Eco',
#                                   color_continuous_scale='viridis')  # High-contrast green-blue
#         fig_bowl_eco.add_trace(px.line(player_bowling, x='Format', y='Eco').data[0])
#         st.plotly_chart(fig_bowl_eco, use_container_width=True)
    
#     with col4:
#         # Wickets Distribution - Using High-Contrast Pie Chart Colors
#         fig_bowl_wickets = px.pie(player_bowling, names='Format', values='Wickets', 
#                                   title='Wickets Breakdown Across Format',
#                                   color_discrete_sequence=px.colors.qualitative.Bold)  # High contrast for dark mode
#         st.plotly_chart(fig_bowl_wickets, use_container_width=True)


# st.title("Cricket Player Stats")

option = st.radio("Select Statistics:", ['Batting', 'Bowling'], horizontal=True)

if option == 'Batting' and not player_batting.empty:
    st.subheader("Batting Figures")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_bat_runs = px.bar(player_batting, x='Runs', y='Format', orientation='h', 
                              title='Runs Breakdown Across Formats', text='Runs',
                              color='Runs', color_continuous_scale='magma')
        fig_bat_runs.update_traces(textposition='outside')
        st.plotly_chart(fig_bat_runs, use_container_width=True)
    
    with col2:
        fig_bat_sr = px.area(player_batting, x='Format', y='SR', title='Strike Rate Across Formats',
                             color_discrete_sequence=['#00FFFF'])  # Neon Cyan
        st.plotly_chart(fig_bat_sr, use_container_width=True)

elif option == 'Bowling' and not player_bowling.empty:
    st.subheader("Bowling Figures")
    col3, col4 = st.columns(2)
    
    with col3:
        fig_bowl_eco = px.scatter(player_bowling, x='Format', y='Eco', size=[10]*len(player_bowling),
                                  title='Economy Rate Across Formats', color='Eco',
                                  color_continuous_scale='viridis')  # High-contrast green-blue
        fig_bowl_eco.add_trace(px.line(player_bowling, x='Format', y='Eco').data[0])
        st.plotly_chart(fig_bowl_eco, use_container_width=True)
    
    with col4:
        fig_bowl_wickets = px.pie(player_bowling, names='Format', values='Wickets', 
                                  title='Wickets Breakdown Across Formats',
                                  color_discrete_sequence=px.colors.qualitative.Bold)  # High contrast for dark mode
        st.plotly_chart(fig_bowl_wickets, use_container_width=True)

