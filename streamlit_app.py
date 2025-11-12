import streamlit as st
import pandas as pd
import numpy as np
import requests
# import pulp
# from pulp import *
# from io import StringIO
import json

st.title("🏌️‍♂️ Degenerates")
st.divider()
st.write(
    "Select your name and a special message will pop up!"
)
name_selection = st.selectbox("Select your name:", ["Choose your name","Alex","Dave","Dante","Jason","Pete","Stuart"])

if name_selection == 'Alex':
  st.write(
    "Alex has wonderful ideas but needs to watch his tone."
)
elif name_selection == 'Dave':
  st.write(
    "Dave is a just judge who makes fair rulings."
)
elif name_selection == 'Dante':
  st.write(
    "Dante has shown steady improvement in his game and has a nice baby fade."
)
elif name_selection == 'Jason':
  st.write(
    "Jason is doing a great job at being a new dad and his wise opinion is always welcome and respected."
)
elif name_selection == 'Pete':
  st.write(
    "Pete is also crushing the new dad game. We'd like to take his $5 more often though 😜"
)
elif name_selection == 'Stuart':
  st.write(
    "Stuart cares deeply about ALL of his subjects."
)

# Insert a small table-of-contents menu so users can jump to sections below
st.divider()

# show tournament info
st.header("Butterfield Bermuda Championship")
st.markdown("Port Royal Golf Course  \nSouthampton Parish, Bermuda  \nNovember 13-16, 2025")
# Display an image from a local file
# st.image("/workspaces/degen-projections/el_cardonal.jpeg")
st.divider()


# --- Table of contents / navigation ---
st.markdown("### Table of contents")
toc_sections = [
    ("Drafter Teams Live-Tournament Scoring Summary", "drafter-live"),
    ("Drafted Players Detailed Live-Tournament Scoring", "drafted-live"),
    ("Full Field Detailed Live-Tournament Scoring", "dg-full-field-live"),
    ("Draft Results", "draft-results"),
    ("Proposed 2026 Points System", "points-2026"),
    ("Drafter Teams Pre-Tournament Projections Summary", "drafter-pre"),
    ("Drafted Players Detailed Pre-Tournament Projections", "drafted-pre"),
    ("Full Field Detailed Pre-Tournament Projections", "dg-pre-tournament")
]

for title, aid in toc_sections:
    # use a single f-string so both aid and title are interpolated correctly
    st.markdown(f'<a href="#{aid}">{title}</a><br/>', unsafe_allow_html=True)

st.divider()

# Live Datagolf Predictions
@st.cache_data(ttl=300)
def load_datagolf_live_preds(url: str) -> pd.DataFrame:
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

# adjust URL if needed
dg_pga_live_predictions_df = load_datagolf_live_preds(
    "https://feeds.datagolf.com/preds/in-play?tour=pga&add_position=25&file_format=csv&key=57b951c096fc3f4eb093c152f5a5"
)

# show full field live interactive table

def reformat_name(name):
    parts = name.split(', ')
    if len(parts) == 2:
        return f"{parts[1]} {parts[0]}"
    return name

dg_pga_live_predictions_df['player_first_last'] = dg_pga_live_predictions_df['player_name'].apply(reformat_name)
# dg_pga_live_predictions_df['projected_points'] = (
#     dg_pga_live_predictions_df['win'] * 25 +
#     dg_pga_live_predictions_df['top_5'] * 10 +
#     dg_pga_live_predictions_df['top_10'] * 8 +
#     dg_pga_live_predictions_df['top_20'] * 6 +
#     # dg_pga_live_predictions_df['top_25'] * 5 +
#     dg_pga_live_predictions_df['make_cut'] * 1
# )

# derive current_points from current_pos using the tournament rules
def current_points_from_pos(pos):
    import re
    if pd.isna(pos):
        return 1
    s = str(pos).strip().upper()
    # WD or CUT => 0 points
    if s in ("WD", "CUT"):
        return 0
    # remove leading 'T' for tied positions (T1, T2, ...)
    if s.startswith('T'):
        s2 = s[1:]
    else:
        s2 = s
    # extract first integer if present
    m = re.search(r"(\d+)", s2)
    if not m:
        return 1
    num = int(m.group(1))
    if num == 1:
        return 50
    if 2 <= num <= 5:
        return 25
    if 6 <= num <= 10:
        return 15
    if 11 <= num <= 25:
        return 7
    return 1

dg_pga_live_predictions_df['current_points'] = dg_pga_live_predictions_df['current_pos'].apply(current_points_from_pos)



dg_pga_live_predictions_df = dg_pga_live_predictions_df[['player_first_last','current_score','current_pos','current_points','win','top_5','top_10','make_cut','round','thru','today','R1','R2','R3','R4','last_update','event_name']]

# Join draft results with live predictions and calculate projected points
draft_results = pd.read_csv("bermuda_2025_draft_results_csv.csv")

merged_players_live_preds_df = pd.merge(draft_results, dg_pga_live_predictions_df, left_on='Player', right_on='player_first_last', how='left')
# merged_players_live_preds_df['projected_points'] = (
#     merged_players_live_preds_df['win'] * 25 +
#     merged_players_live_preds_df['top_5'] * 10 +
#     merged_players_live_preds_df['top_10'] * 8 +
#     merged_players_live_preds_df['top_20'] * 6 +
#     # merged_players_live_preds_df['top_25'] * 5 +
#     merged_players_live_preds_df['make_cut'] * 1
# )
merged_players_live_preds_df = merged_players_live_preds_df[['Drafter','Pick','Round','player_first_last','current_score','current_pos','current_points','win','top_5','top_10','make_cut','round','thru','today','R1','R2','R3','R4','last_update','event_name']]


# Live Tournament Drafter Teams Points Totals

# Filter for each drafter's picks
alex_picks_df_live = merged_players_live_preds_df[merged_players_live_preds_df['Drafter'] == 'Alex'][['Round', 'player_first_last','current_points']].rename(columns={
    'player_first_last': 'alex_player',
    'current_points': 'alex_player_current_points'
    # 'projected_points': 'alex_player_projected_points'
})

dave_picks_df_live = merged_players_live_preds_df[merged_players_live_preds_df['Drafter'] == 'Dave'][['Round', 'player_first_last','current_points']].rename(columns={
    'player_first_last': 'dave_player',
    'current_points': 'dave_player_current_points'
    # 'projected_points': 'dave_player_projected_points'
})

stu_picks_df_live = merged_players_live_preds_df[merged_players_live_preds_df['Drafter'] == 'Stu'][['Round', 'player_first_last','current_points']].rename(columns={
    'player_first_last': 'stu_player',
    'current_points': 'stu_player_current_points'
    # 'projected_points': 'stu_player_projected_points'
})

# Merge the dataframes based on the 'Round' column
all_drafter_picks_df_live = pd.merge(alex_picks_df_live, dave_picks_df_live, on='Round', how='left')
all_drafter_picks_df_live = pd.merge(all_drafter_picks_df_live, stu_picks_df_live, on='Round', how='left')

# Calculate total projected points for each drafter
# alex_total_points_live = all_drafter_picks_df_live['alex_player_projected_points'].sum()
alex_total_current_points_live = all_drafter_picks_df_live['alex_player_current_points'].sum()

# dave_total_points_live = all_drafter_picks_df_live['dave_player_projected_points'].sum()
dave_total_current_points_live = all_drafter_picks_df_live['dave_player_current_points'].sum()

# stu_total_points_live = all_drafter_picks_df_live['stu_player_projected_points'].sum()
stu_total_current_points_live = all_drafter_picks_df_live['stu_player_current_points'].sum()


# Create a new row for the totals
total_row_live = pd.DataFrame({
    'Round': ['Total points'],
    'alex_player': [''], # Keep player columns empty for the total row
    'alex_player_current_points': [alex_total_current_points_live],
    # 'alex_player_projected_points': [alex_total_points_live],
    'dave_player': [''],
    'dave_player_current_points': [dave_total_current_points_live],
    # 'dave_player_projected_points': [dave_total_points_live],
    'stu_player': [''],
    'stu_player_current_points': [stu_total_current_points_live],
    # 'stu_player_projected_points': [stu_total_points_live]
})

# Append the total row to the dataframe
all_drafter_picks_df_live = pd.concat([all_drafter_picks_df_live, total_row_live], ignore_index=True)

# Anchor for: Drafter Teams with Live-Tournament Projected Points
st.markdown('<a id="drafter-live"></a>', unsafe_allow_html=True)
st.subheader("Drafter Teams Live-Tournament Scoring Summary")
st.write("Will update every 5 minutes after the tournament begins. Before the tournament begins, there will be missing/incorrect entries in the live tournament tables because DataGolf is still showing information from the previous tournament.")
# Quick link to the Proposed 2026 Points System section
st.markdown('See <a href="#points-2026">Degen points scoring system</a>.', unsafe_allow_html=True)
st.dataframe(all_drafter_picks_df_live.reset_index(drop=True), use_container_width=True)

# Anchor for: Drafted Players with Live-Tournament Projected Points
st.markdown('<a id="drafted-live"></a>', unsafe_allow_html=True)
st.subheader("Drafted Players Detailed Live-Tournament Scoring")
st.write("The 'win', 'top_5', 'top_10' and 'make_cut' columns reflect DataGolf projections and should be read as percentages. For example, if a player has a 'win' value of 0.12, then they have a 12% chance of winning.")
st.dataframe(merged_players_live_preds_df.reset_index(drop=True), use_container_width=True)

st.divider()

# Anchor for: Datagolf Full Field Live Predictions
st.markdown('<a id="dg-full-field-live"></a>', unsafe_allow_html=True)
st.subheader("Full Field Detailed Live-Tournament Scoring")
st.dataframe(dg_pga_live_predictions_df.reset_index(drop=True), use_container_width=True)

st.divider()

# adjust path if needed
draft_results = pd.read_csv("bermuda_2025_draft_results_csv.csv")

# Anchor for: Draft Results
st.markdown('<a id="draft-results"></a>', unsafe_allow_html=True)
st.subheader("Draft Results")
st.dataframe(draft_results, use_container_width=True)

# Show Proposed 2026 Points System
st.divider()
# Anchor for: Proposed 2026 Points System
st.markdown('<a id="points-2026"></a>', unsafe_allow_html=True)
st.subheader("Proposed 2026 Points System")
points = pd.read_csv("points_2026.csv")
st.dataframe(points)
# st.dataframe(points.style.hide_index(), use_container_width=True)


st.divider()

# Load Datagolf pre-tournament predictions
@st.cache_data(ttl=3600)
def load_datagolf_pre_tournament_preds(url: str) -> pd.DataFrame:
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

dg_pga_pre_tournament_predictions_df = load_datagolf_pre_tournament_preds(
    "https://feeds.datagolf.com/preds/pre-tournament?tour=pga&add_position=25&file_format=csv&key=57b951c096fc3f4eb093c152f5a5"
)

dg_pga_pre_tournament_predictions_df = dg_pga_pre_tournament_predictions_df[dg_pga_pre_tournament_predictions_df['model'] == 'baseline_history_fit']


#calculate projected points based on proposed 2026 system
dg_pga_pre_tournament_predictions_df['projected_points'] = (
    dg_pga_pre_tournament_predictions_df['win'] * 25 +
    dg_pga_pre_tournament_predictions_df['top_5'] * 10 +
    dg_pga_pre_tournament_predictions_df['top_10'] * 8 +
    # dg_pga_pre_tournament_predictions_df['top_20'] * 6 +
    dg_pga_pre_tournament_predictions_df['top_25'] * 6 +
    dg_pga_pre_tournament_predictions_df['make_cut'] * 1
)


# Clean up player names and show pre-tournament projected points

def reformat_name(name):
    parts = name.split(', ')
    if len(parts) == 2:
        return f"{parts[1]} {parts[0]}"
    return name

dg_pga_pre_tournament_predictions_df['player_first_last'] = dg_pga_pre_tournament_predictions_df['player_name'].apply(reformat_name)
dg_pga_pre_tournament_predictions_df = dg_pga_pre_tournament_predictions_df[['player_first_last','win','top_5','top_10','top_25','make_cut','projected_points','event_name']]

# Join draft results with pre-tournament predictions

merged_players_pretourney_preds_df = pd.merge(draft_results, dg_pga_pre_tournament_predictions_df, left_on='Player', right_on='player_first_last', how='left')
merged_players_pretourney_preds_df = merged_players_pretourney_preds_df[['Drafter','Pick','Round','player_first_last','win','top_5','top_10','top_25','make_cut','projected_points']]

# Show drafter teams and projected points totals
#filter 
# Filter for each drafter's picks
alex_picks_df = merged_players_pretourney_preds_df[merged_players_pretourney_preds_df['Drafter'] == 'Alex'][['Round', 'player_first_last', 'projected_points']].rename(columns={
    'player_first_last': 'alex_player',
    'projected_points': 'alex_player_projected_points'
})

dave_picks_df = merged_players_pretourney_preds_df[merged_players_pretourney_preds_df['Drafter'] == 'Dave'][['Round', 'player_first_last', 'projected_points']].rename(columns={
    'player_first_last': 'dave_player',
    'projected_points': 'dave_player_projected_points'
})

stu_picks_df = merged_players_pretourney_preds_df[merged_players_pretourney_preds_df['Drafter'] == 'Stu'][['Round', 'player_first_last', 'projected_points']].rename(columns={
    'player_first_last': 'stu_player',
    'projected_points': 'stu_player_projected_points'
})

# Merge the dataframes based on the 'Round' column
all_drafter_picks_df = pd.merge(alex_picks_df, dave_picks_df, on='Round', how='left')
all_drafter_picks_df = pd.merge(all_drafter_picks_df, stu_picks_df, on='Round', how='left')

# Calculate total predicted points for each drafter
alex_total_points = all_drafter_picks_df['alex_player_projected_points'].sum()
dave_total_points = all_drafter_picks_df['dave_player_projected_points'].sum()
stu_total_points = all_drafter_picks_df['stu_player_projected_points'].sum()

# Create a new row for the totals
total_row = pd.DataFrame({
    'Round': ['Total points'],
    'alex_player': [''], # Keep player columns empty for the total row
    'alex_player_projected_points': [alex_total_points],
    'dave_player': [''],
    'dave_player_projected_points': [dave_total_points],
    'stu_player': [''],
    'stu_player_projected_points': [stu_total_points]
})

# Append the total row to the dataframe
all_drafter_picks_df = pd.concat([all_drafter_picks_df, total_row], ignore_index=True)
# Anchor for: Drafter Teams with Pre-Tournament Projected Points
st.markdown('<a id="drafter-pre"></a>', unsafe_allow_html=True)
st.subheader("Drafter Teams Pre-Tournament Projections Summary")
st.markdown('See <a href="#points-2026">Degen points scoring system</a>.', unsafe_allow_html=True)
st.dataframe(all_drafter_picks_df.reset_index(drop=True), use_container_width=True)

st.divider()

# Anchor for: Drafted Players with Datagolf Pre-Tournament Projections
st.markdown('<a id="drafted-pre"></a>', unsafe_allow_html=True)
st.subheader("Drafted Players Detailed Pre-Tournament Projections")
st.write("The 'win', 'top_5', 'top_10' and 'make_cut' columns reflect DataGolf projections and should be read as percentages. For example, if a player has a 'win' value of 0.12, then they have a 12% chance of winning.")

st.dataframe(merged_players_pretourney_preds_df.reset_index(drop=True), use_container_width=True)

st.divider()

# Anchor for: Datagolf Pre-Tournament Predictions
st.markdown('<a id="dg-pre-tournament"></a>', unsafe_allow_html=True)
st.subheader("Full Field Detailed Pre-Tournament Projections")
st.dataframe(dg_pga_pre_tournament_predictions_df.reset_index(drop=True), use_container_width=True)

