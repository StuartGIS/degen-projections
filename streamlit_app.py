import streamlit as st
import pandas as pd
import numpy as np
import requests
# import pulp
# from pulp import *
# from io import StringIO
import json

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Lobster&display=swap" rel="stylesheet"><h1 style="font-family: \'Lobster\', cursive; color: gold; text-shadow: -1px -1px 0 black, 1px -1px 0 black, -1px 1px 0 black, 1px 1px 0 black;">🏌️‍♂️ Degenerates</h1>', unsafe_allow_html=True)
st.divider()
# st.write(
#     "Select your name and a special message will pop up!"
# )
# name_selection = st.selectbox("Select your name:", ["Choose your name","Alex","Dave","Dante","Jason","Pete","Stuart"])

# if name_selection == 'Alex':
#   st.write(
#     "Alex has wonderful ideas but needs to watch his tone."
# )
# elif name_selection == 'Dave':
#   st.write(
#     "Dave is a just judge who makes fair rulings."
# )
# elif name_selection == 'Dante':
#   st.write(
#     "Dante has shown steady improvement in his game and has a nice baby fade."
# )
# elif name_selection == 'Jason':
#   st.write(
#     "Jason is doing a great job at being a new dad and his wise opinion is always welcome and respected."
# )
# elif name_selection == 'Pete':
#   st.write(
#     "Pete is also crushing the new dad game. We'd like to take his $5 more often though 😜"
# )
# elif name_selection == 'Stuart':
#   st.write(
#     "Stuart cares deeply about ALL of his subjects."
# )

# # Insert a small table-of-contents menu so users can jump to sections below
# st.divider()

# show tournament info
st.header("RBC Heritage")
st.markdown("Harbour Town Golf Links  \nHilton Head Island, South Carolina  \nApril 16-19, 2026")
# Display an image from a local file
# st.image("/workspaces/degen-projections/el_cardonal.jpeg")
st.divider()


# --- Table of contents / navigation ---
st.markdown("### Table of contents")

# Add new section for Drafted Players Season Standings

toc_sections = [
    ("Drafter Teams Live-Tournament Scoring Summary", "drafter-live"),
    ("Drafted Players Detailed Live-Tournament Scoring", "drafted-live"),
    ("Full Field Detailed Live-Tournament Scoring", "dg-full-field-live"),
    ("Draft Results", "draft-results"),
    ("Season Standings", "season-standings"),
    ("Drafted Players Season Standings", "drafted-players-season-standings"),
    ("All Players Season Standings", "all-players-season-standings"),
    # ("All Players: Performance Last 16 Rounds", "player-performance-last16"),
    # ("Current Event Players: Performance Last 16 Rounds", "current-event-player-performance-last16"),
    ("All Players: Performance 2026", "player-performance-2026"),
    ("Current Event Players: Performance 2026", "current-event-player-performance-2026"),
    ("2026 Points System", "points-2026"),
    ("Drafter Teams Pre-Tournament Projections Summary", "drafter-pre"),
    ("Drafted Players Detailed Pre-Tournament Projections", "drafted-pre"),
    ("Full Field Detailed Pre-Tournament Projections", "dg-pre-tournament"),
    ("Drafters Points Gained Per Round", "drafters-points-gained-per-round"),
    # ("Round Leads", "round-leads")
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

def style_live_rows(row):
    pos_str = str(row['current_pos']).strip().upper()
    if pos_str in ('WD', 'CUT', 'MC', '') or pd.isna(row['current_pos']):
        return ['background-color: rgba(139, 0, 0, 0.3); color: white'] * len(row)
    if pos_str.startswith('T'):
        pos_str = pos_str[1:]
    try:
        pos_num = int(pos_str)
    except:
        return ['background-color: rgba(139, 0, 0, 0.3); color: white'] * len(row)
    if pos_num == 1:
        color = 'rgba(144, 238, 144, 0.5)'  # light green, semi-transparent
    elif 2 <= pos_num <= 5:
        color = 'rgba(50, 205, 50, 0.5)'  # lime green, semi-transparent
    elif 6 <= pos_num <= 10:
        color = 'rgba(34, 139, 34, 0.5)'  # forest green, semi-transparent
    elif 11 <= pos_num <= 25:
        color = 'rgba(0, 100, 0, 0.5)'  # dark green, semi-transparent
    else:
        color = 'rgba(0, 100, 0, 0.2)'  # darkest green, semi-transparent
    return [f'background-color: {color}; color: white'] * len(row)

def style_drafter_live_rows(row):
    styles = [''] * len(row)  # default no style
    # Columns: ['Round', 'Alex', 'Alex Points', 'Dave', 'Dave Points', 'Stu', 'Stu Points']
    # Indices: 0: Round, 1: Alex, 2: Alex Points, 3: Dave, 4: Dave Points, 5: Stu, 6: Stu Points
    
    # For Alex
    alex_points = row['Alex Points']
    if alex_points == 50:
        color = 'rgba(144, 238, 144, 0.5)'
    elif alex_points == 25:
        color = 'rgba(50, 205, 50, 0.5)'
    elif alex_points == 15:
        color = 'rgba(34, 139, 34, 0.5)'
    elif alex_points == 7:
        color = 'rgba(0, 100, 0, 0.5)'
    elif alex_points == 1:
        color = 'rgba(0, 100, 0, 0.2)'
    elif alex_points == 0:
        color = 'rgba(139, 0, 0, 0.3)'
    else:
        color = None
    if color:
        styles[1] = f'background-color: {color}; color: white'  # Alex player
        styles[2] = f'background-color: {color}; color: white'  # Alex Points
    
    # For Dave
    dave_points = row['Dave Points']
    if dave_points == 50:
        color = 'rgba(144, 238, 144, 0.5)'
    elif dave_points == 25:
        color = 'rgba(50, 205, 50, 0.5)'
    elif dave_points == 15:
        color = 'rgba(34, 139, 34, 0.5)'
    elif dave_points == 7:
        color = 'rgba(0, 100, 0, 0.5)'
    elif dave_points == 1:
        color = 'rgba(0, 100, 0, 0.2)'
    elif dave_points == 0:
        color = 'rgba(139, 0, 0, 0.3)'
    else:
        color = None
    if color:
        styles[3] = f'background-color: {color}; color: white'  # Dave player
        styles[4] = f'background-color: {color}; color: white'  # Dave Points
    
    # For Stu
    stu_points = row['Stu Points']
    if stu_points == 50:
        color = 'rgba(144, 238, 144, 0.5)'
    elif stu_points == 25:
        color = 'rgba(50, 205, 50, 0.5)'
    elif stu_points == 15:
        color = 'rgba(34, 139, 34, 0.5)'
    elif stu_points == 7:
        color = 'rgba(0, 100, 0, 0.5)'
    elif stu_points == 1:
        color = 'rgba(0, 100, 0, 0.2)'
    elif stu_points == 0:
        color = 'rgba(139, 0, 0, 0.3)'
    else:
        color = None
    if color:
        styles[5] = f'background-color: {color}; color: white'  # Stu player
        styles[6] = f'background-color: {color}; color: white'  # Stu Points
    
    # Special handling for Total points row
    if row['Round'] == 'Total points':
        points_values = [row['Alex Points'], row['Dave Points'], row['Stu Points']]
        sorted_values = sorted(set(points_values), reverse=True)  # unique sorted descending
        if len(sorted_values) >= 3:
            max_val = sorted_values[0]
            second_val = sorted_values[1]
            min_val = sorted_values[2]
        elif len(sorted_values) == 2:
            max_val = sorted_values[0]
            second_val = sorted_values[1]
            min_val = sorted_values[1]  # if only two unique, second and min same
        else:
            max_val = sorted_values[0]
            second_val = sorted_values[0]
            min_val = sorted_values[0]
        
        for i, col in enumerate(['Alex Points', 'Dave Points', 'Stu Points']):
            val = row[col]
            if val == max_val:
                styles[2 + i*2] = 'background-color: darkgreen; color: white'
            elif val == second_val:
                styles[2 + i*2] = 'background-color: darkgoldenrod; color: white'
            elif val == min_val:
                styles[2 + i*2] = 'background-color: darkred; color: white'
    
    return styles

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

if 'player_name' in dg_pga_live_predictions_df.columns:
    dg_pga_live_predictions_df['player_first_last'] = dg_pga_live_predictions_df['player_name'].apply(reformat_name)
elif 'player_first_last' in dg_pga_live_predictions_df.columns:
    # Optionally reformat if needed, or just keep as is
    pass
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



dg_pga_live_predictions_df = dg_pga_live_predictions_df[['current_pos', 'player_first_last', 'current_score', 'current_points', 'round', 'thru', 'today', 'R1', 'R2', 'R3', 'R4', 'win', 'top_5', 'top_10', 'make_cut', 'last_update', 'event_name']]

# Convert probability columns to percentages for display
dg_pga_live_predictions_df[['win', 'top_5', 'top_10', 'make_cut']] *= 100

# Sort by Score in ascending order
dg_pga_live_predictions_df = dg_pga_live_predictions_df.sort_values('current_score')

# Apply conditional formatting
styled_dg_live = dg_pga_live_predictions_df.style.apply(style_live_rows, axis=1)

# Join draft results with live predictions and calculate projected points
draft_results = pd.read_csv("RBC_draft_results_csv.csv")

merged_players_live_preds_df = pd.merge(draft_results, dg_pga_live_predictions_df, left_on='Player', right_on='player_first_last', how='left')
# merged_players_live_preds_df['projected_points'] = (
#     merged_players_live_preds_df['win'] * 25 +
#     merged_players_live_preds_df['top_5'] * 10 +
#     merged_players_live_preds_df['top_10'] * 8 +
#     merged_players_live_preds_df['top_20'] * 6 +
#     # merged_players_live_preds_df['top_25'] * 5 +
#     merged_players_live_preds_df['make_cut'] * 1
# )
merged_players_live_preds_df = merged_players_live_preds_df[['Drafter', 'Pick', 'Round', 'current_pos', 'player_first_last', 'current_score', 'current_points', 'thru', 'R1', 'R2', 'R3', 'R4', 'win', 'top_5', 'top_10', 'make_cut']]

# Sort by Score in ascending order
merged_players_live_preds_df = merged_players_live_preds_df.sort_values('current_score')

# Apply conditional formatting
styled_drafted_live = merged_players_live_preds_df.style.apply(style_live_rows, axis=1)


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

# Convert Round column to string to handle mixed types
all_drafter_picks_df_live['Round'] = all_drafter_picks_df_live['Round'].astype(str)

# Sort by Round as integer, keeping 'Total points' last
def round_sort_key(val):
    try:
        return (0, int(val))
    except ValueError:
        return (1, float('inf'))  # 'Total points' or any non-integer goes last
all_drafter_picks_df_live = all_drafter_picks_df_live.sort_values(by='Round', key=lambda col: col.map(round_sort_key)).reset_index(drop=True)

# Rename columns for user-facing display
all_drafter_picks_df_live = all_drafter_picks_df_live.rename(columns={
    'alex_player': 'Alex',
    'alex_player_current_points': 'Alex Points',
    'dave_player': 'Dave',
    'dave_player_current_points': 'Dave Points',
    'stu_player': 'Stu',
    'stu_player_current_points': 'Stu Points'
})

# Anchor for: Drafter Teams with Live-Tournament Projected Points
st.markdown('<a id="drafter-live"></a>', unsafe_allow_html=True)
st.subheader("Drafter Teams Live-Tournament Scoring Summary")
st.write("Will update every 5 minutes after the tournament begins. Before the tournament begins, there will be missing/incorrect entries in the live tournament tables because DataGolf is still showing information from the previous tournament.")
# Quick link to the 2026 Points System section
st.markdown('See <a href="#points-2026">Degen points scoring system</a>.', unsafe_allow_html=True)
styled_drafter_live = all_drafter_picks_df_live.style.apply(style_drafter_live_rows, axis=1)
st.dataframe(styled_drafter_live, width='stretch', hide_index=True)

# Anchor for: Drafted Players with Live-Tournament Projected Points
st.markdown('<a id="drafted-live"></a>', unsafe_allow_html=True)
st.subheader("Drafted Players Detailed Live-Tournament Scoring")
st.write("The 'Win', 'Top 5', 'Top 10' and 'Make Cut' columns reflect live DataGolf projections.")
st.dataframe(styled_drafted_live, width='stretch', hide_index=True, column_config={
    'Round': st.column_config.TextColumn('Round'),
    'current_pos': st.column_config.TextColumn('Pos'),
    'player_first_last': st.column_config.TextColumn('Golfer'),
    'current_score': st.column_config.TextColumn('Score'),
    'current_points': st.column_config.NumberColumn('Points'),
    'thru': st.column_config.TextColumn('Thru'),
    'R2': st.column_config.NumberColumn('R2', format='%.0f'),
    'R3': st.column_config.NumberColumn('R3', format='%.0f'),
    'R4': st.column_config.NumberColumn('R4', format='%.0f'),
    'win': st.column_config.NumberColumn('Win', format='%.1f%%'),
    'top_5': st.column_config.NumberColumn('Top 5', format='%.1f%%'),
    'top_10': st.column_config.NumberColumn('Top 10', format='%.1f%%'),
    'make_cut': st.column_config.NumberColumn('Make Cut', format='%.1f%%')
})

st.divider()

# Anchor for: Datagolf Full Field Live Predictions
st.markdown('<a id="dg-full-field-live"></a>', unsafe_allow_html=True)
st.subheader("Full Field Detailed Live-Tournament Scoring")
st.dataframe(styled_dg_live, width='stretch', hide_index=True, column_config={
    'player_first_last': st.column_config.TextColumn('Golfer'),
    'current_score': st.column_config.TextColumn('Score'),
    'current_pos': st.column_config.TextColumn('Pos'),
    'current_points': st.column_config.NumberColumn('Points'),
    'R2': st.column_config.NumberColumn('R2', format='%.0f'),
    'R3': st.column_config.NumberColumn('R3', format='%.0f'),
    'R4': st.column_config.NumberColumn('R4', format='%.0f'),
    'win': st.column_config.NumberColumn('Win', format='%.1f%%'),
    'top_5': st.column_config.NumberColumn('Top 5', format='%.1f%%'),
    'top_10': st.column_config.NumberColumn('Top 10', format='%.1f%%'),
    'make_cut': st.column_config.NumberColumn('Make Cut', format='%.1f%%'),
    'round': st.column_config.TextColumn('Round'),
    'thru': st.column_config.TextColumn('Thru'),
    'today': st.column_config.TextColumn('Today'),
    'last_update': st.column_config.TextColumn('Last Update'),
    'event_name': st.column_config.TextColumn('Event Name')
})

st.divider()

# adjust path if needed
draft_results = pd.read_csv("RBC_draft_results_csv.csv")

# Anchor for: Draft Results
st.markdown('<a id="draft-results"></a>', unsafe_allow_html=True)
st.subheader("Draft Results")
st.dataframe(draft_results, width='stretch', hide_index=True)

# Season standings
st.markdown('<a id="season-standings"></a>', unsafe_allow_html=True)
st.subheader("Season Standings")
st.write("Updated April 19, 2026, after RBC heritage completion.")

import os
relevant_files = [f for f in os.listdir('.') if 'drafted_points_result' in f and f.endswith('.csv')]

if relevant_files:
    all_data = []
    points_wins = {'Alex': 0, 'Dave': 0, 'Stu': 0}
    total_drafts = len(relevant_files)
    per_draft_pcts = []
    for file in relevant_files:
        df = pd.read_csv(file)
        all_data.append(df)
        # For points win
        drafter_sums = df.groupby('Drafter')['current_points'].sum()
        max_points = drafter_sums.max()
        winners = drafter_sums[drafter_sums == max_points].index
        for winner in winners:
            points_wins[winner] += 1
        # Per draft stats
        draft_stats = df.groupby('Drafter').agg(
            total_players=('Drafter', 'size'),
            made_cut_count=('make_cut', 'sum'),
            top25_count=('current_points', lambda x: (x >= 7).sum()),
            top10_count=('top_10', 'sum'),
            top5_count=('top_5', 'sum'),
            sum_points=('current_points', 'sum'),
        ).reset_index()
        # Calculate winner_count as 1 if any win > 0 for that drafter in this draft, else 0
        win_by_drafter = df.groupby('Drafter')['win'].sum().reset_index()
        win_by_drafter['winner_count'] = (win_by_drafter['win'] > 0).astype(int)
        draft_stats = pd.merge(draft_stats, win_by_drafter[['Drafter', 'winner_count']], on='Drafter', how='left')
        draft_stats['made_cut_pct'] = draft_stats['made_cut_count'] / draft_stats['total_players']
        draft_stats['top25_pct'] = draft_stats['top25_count'] / draft_stats['total_players'] * 100
        draft_stats['top10_pct'] = draft_stats['top10_count'] / draft_stats['total_players']
        draft_stats['top5_pct'] = draft_stats['top5_count'] / draft_stats['total_players']
        draft_stats['winner_pct'] = draft_stats['winner_count'] * 100
        per_draft_pcts.append(draft_stats[['Drafter', 'made_cut_pct', 'top25_pct', 'top10_pct', 'top5_pct', 'winner_pct', 'total_players', 'winner_count', 'sum_points']])
    combined_df = pd.concat(all_data, ignore_index=True)
    # Average the percentages
    all_pcts = pd.concat(per_draft_pcts, ignore_index=True)
    avg_stats = all_pcts.groupby('Drafter').agg(
        made_cut_pct=('made_cut_pct', 'mean'),
        top25_pct=('top25_pct', 'mean'),
        top10_pct=('top10_pct', 'mean'),
        top5_pct=('top5_pct', 'mean'),
        winner_pct=('winner_pct', 'mean'),
        total_players=('total_players', 'sum'),
        winner_count=('winner_count', 'sum'),
        avg_weekly_points=('sum_points', 'mean'),
        total_season_points=('sum_points', 'sum'),
    ).reset_index()
    # Format
    avg_stats['Made Cut %'] = avg_stats['made_cut_pct'].round(2).astype(str) + '%'
    avg_stats['Top 25 %'] = avg_stats['top25_pct'].round(2).astype(str) + '%'
    avg_stats['Top 10 %'] = avg_stats['top10_pct'].round(2).astype(str) + '%'
    avg_stats['Top 5 %'] = avg_stats['top5_pct'].round(2).astype(str) + '%'
    avg_stats['Winner %'] = avg_stats['winner_pct'].round(2).astype(str) + '%'
    avg_stats['Winner Count'] = avg_stats['winner_count'].astype(str)
    points_win_counts = avg_stats['Drafter'].map(points_wins)
    avg_stats['Points Win Count'] = points_win_counts.astype(str)
    avg_stats['Points Win %'] = (points_win_counts / total_drafts * 100).round(2).astype(str) + '%'
    avg_stats['Tournaments Played'] = str(total_drafts)
    avg_stats['Avg Weekly Points'] = avg_stats['avg_weekly_points'].round(1).map(lambda x: f"{x:.1f}")
    avg_stats['Total Season Points'] = avg_stats['total_season_points'].astype(str)
    avg_stats['Season Earnings'] = avg_stats['Drafter'].map({'Alex': '$50', 'Dave': '$60', 'Stu': '$20'})
    display_stats = avg_stats[['Drafter', 'Made Cut %', 'Top 25 %', 'Top 10 %', 'Top 5 %', 'Winner %', 'Winner Count', 'Points Win %', 'Points Win Count', 'Tournaments Played', 'Avg Weekly Points', 'Total Season Points', 'Season Earnings']].set_index('Drafter').T
    display_stats.index = ['Made Cut', 'Top 25', 'Top 10', 'Top 5', 'Winners %', 'Winners', 'Points Wins %', 'Points Wins', 'Tournaments Played', 'Avg Weekly Points', 'Total Season Points', 'Season Earnings']
    # Add Geography Wins row
    geography_wins = pd.Series({'Alex': 3, 'Dave': 3, 'Stu': 7})
    display_stats.loc['Geography Wins'] = geography_wins
    
    def highlight_rank(s):
        parsed = []
        for val in s:
            if isinstance(val, str):
                if val.endswith('%'):
                    parsed.append(float(val[:-1]))
                elif val.startswith('$'):
                    parsed.append(float(val[1:]))
                else:
                    try:
                        parsed.append(float(val))
                    except:
                        parsed.append(float('nan'))
            else:
                parsed.append(float(val))
        series = pd.Series(parsed, index=s.index)
        ranks = series.sort_values(ascending=False).dropna().unique()
        if len(ranks) == 0:
            return ['' for _ in s]
        styles = []
        highest = ranks[0]
        # Case 1: all values are the same
        if len(ranks) == 1:
            for val in parsed:
                if pd.isna(val):
                    styles.append('')
                else:
                    styles.append('background-color: darkgreen; color: white')
        # Case 2: two or three cells tied for highest, one lower
        elif len(ranks) == 2:
            count_highest = sum(val == highest for val in parsed if not pd.isna(val))
            if count_highest >= 2:
                # Two or three tied for highest, one lower
                for val in parsed:
                    if pd.isna(val):
                        styles.append('')
                    elif val == highest:
                        styles.append('background-color: darkgreen; color: white')
                    else:
                        styles.append('background-color: darkred; color: white')
            else:
                # One highest, two tied for second
                second = ranks[1]
                for val in parsed:
                    if pd.isna(val):
                        styles.append('')
                    elif val == highest:
                        styles.append('background-color: darkgreen; color: white')
                    elif val == second:
                        styles.append('background-color: darkgoldenrod; color: white')
                    else:
                        styles.append('')
        # Case 3: three unique values
        elif len(ranks) == 3:
            highest = ranks[0]
            second = ranks[1]
            lowest = ranks[2]
            for val in parsed:
                if pd.isna(val):
                    styles.append('')
                elif val == highest:
                    styles.append('background-color: darkgreen; color: white')
                elif val == second:
                    styles.append('background-color: darkgoldenrod; color: white')
                elif val == lowest:
                    styles.append('background-color: darkred; color: white')
                else:
                    styles.append('')
        else:
            # More than 3 unique values, fallback: highest darkgreen, lowest darkred, others no color
            highest = ranks[0]
            lowest = ranks[-1]
            for val in parsed:
                if pd.isna(val):
                    styles.append('')
                elif val == highest:
                    styles.append('background-color: darkgreen; color: white')
                elif val == lowest:
                    styles.append('background-color: darkred; color: white')
                else:
                    styles.append('')
        return styles
    
    styled_df = display_stats.style.apply(highlight_rank, axis=1)
    st.dataframe(styled_df, width='stretch')
else:
    st.write("No relevant CSV files found in the repository.")


# Show 2026 Points System
st.divider()
# Anchor for: 2026 Points System
st.markdown('<a id="points-2026"></a>', unsafe_allow_html=True)
st.subheader("2026 Points System")
points = pd.read_csv("points_2026.csv")
# Rename values in Finishing Position column for user-facing display
points['Finishing Position'] = points['Finishing Position'].replace({
    '1st': 'Win',
    '2nd-5th': 'Top 5',
    '6th-10th': 'Top 10',
    '11th-25th': 'Top 25',
    'Made Cut': 'Make Cut'
})
st.dataframe(points, hide_index=True)
# st.dataframe(points.style.hide_index(), width='stretch')


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

# Convert probability columns to percentages for display
dg_pga_pre_tournament_predictions_df[['win', 'top_5', 'top_10', 'top_25', 'make_cut']] *= 100

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

# Convert Round column to string to handle mixed types
all_drafter_picks_df['Round'] = all_drafter_picks_df['Round'].astype(str)
# Anchor for: Drafter Teams with Pre-Tournament Projected Points
st.markdown('<a id="drafter-pre"></a>', unsafe_allow_html=True)
st.subheader("Drafter Teams Pre-Tournament Projections Summary")
st.markdown('See <a href="#points-2026">Degen points scoring system</a>.', unsafe_allow_html=True)
st.dataframe(all_drafter_picks_df.reset_index(drop=True), width='stretch', hide_index=True, column_config={
    'alex_player': st.column_config.TextColumn('Alex'),
    'alex_player_projected_points': st.column_config.NumberColumn('Alex Projected Points'),
    'dave_player': st.column_config.TextColumn('Dave'),
    'dave_player_projected_points': st.column_config.NumberColumn('Dave Projected Points'),
    'stu_player': st.column_config.TextColumn('Stu'),
    'stu_player_projected_points': st.column_config.NumberColumn('Stu Projected Points')
})

st.divider()

# Anchor for: Drafted Players with Datagolf Pre-Tournament Projections
st.markdown('<a id="drafted-pre"></a>', unsafe_allow_html=True)
st.subheader("Drafted Players Detailed Pre-Tournament Projections")
st.write("The 'win', 'top_5', 'top_10' and 'make_cut' columns reflect DataGolf projections and should be read as percentages. For example, if a player has a 'win' value of 0.12, then they have a 12% chance of winning.")

st.dataframe(merged_players_pretourney_preds_df.reset_index(drop=True), width='stretch', hide_index=True, column_config={
    'player_first_last': st.column_config.TextColumn('Golfer'),
    'win': st.column_config.NumberColumn('Win', format='%.1f%%'),
    'top_5': st.column_config.NumberColumn('Top 5', format='%.1f%%'),
    'top_10': st.column_config.NumberColumn('Top 10', format='%.1f%%'),
    'top_25': st.column_config.NumberColumn('Top 25', format='%.1f%%'),
    'make_cut': st.column_config.NumberColumn('Make Cut', format='%.1f%%'),
    'projected_points': st.column_config.NumberColumn('Projected Points')
})

st.divider()

# Anchor for: Datagolf Pre-Tournament Predictions
# Anchor for: Datagolf Pre-Tournament Predictions
st.markdown('<a id="dg-pre-tournament"></a>', unsafe_allow_html=True)
st.subheader("Full Field Detailed Pre-Tournament Projections")
st.dataframe(dg_pga_pre_tournament_predictions_df.reset_index(drop=True), width='stretch', hide_index=True, column_config={
    'player_first_last': st.column_config.TextColumn('Golfer'),
    'win': st.column_config.NumberColumn('Win', format='%.1f%%'),
    'top_5': st.column_config.NumberColumn('Top 5', format='%.1f%%'),
    'top_10': st.column_config.NumberColumn('Top 10', format='%.1f%%'),
    'top_25': st.column_config.NumberColumn('Top 25', format='%.1f%%'),
    'make_cut': st.column_config.NumberColumn('Make Cut', format='%.1f%%'),
    'projected_points': st.column_config.NumberColumn('Projected Points'),
    'event_name': st.column_config.TextColumn('Event Name')
})


# --- Drafted Players Season Standings ---
st.divider()
st.markdown('<a id="drafted-players-season-standings"></a>', unsafe_allow_html=True)
st.subheader("Drafted Players Season Standings")
st.write("Updated April 19, 2026, after RBC Heritage completion.")

# Load all drafted_points_results CSVs
import re
# Automatically find all drafted_points_result CSVs and extract tournament names
csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'drafted_points_result' in f]
dfs = []
tournament_pos_dicts = {}
tournament_names = []
for f in csv_files:
    try:
        df = pd.read_csv(f)
        dfs.append(df)
        # Extract tournament name (first word before underscore)
        match = re.match(r"([A-Za-z0-9]+)_.*drafted_points_result.*\.csv", f)
        if match:
            tname = match.group(1)
            tournament_names.append(tname)
            tournament_pos_dicts[tname] = dict(zip(df['player_first_last'], df['current_pos']))
    except Exception as e:
        st.warning(f"Could not load {f}: {e}")

if dfs:
    all_drafts = pd.concat(dfs, ignore_index=True)
    # Normalize column names (handle leading comma in some files)
    all_drafts.columns = [c.lstrip(',') for c in all_drafts.columns]
    # Group by player and add Events column
    player_stats = all_drafts.groupby('player_first_last').agg(
        Season_Points=('current_points', 'sum'),
        Events=('player_first_last', 'count'),
        Alex=('Drafter', lambda x: (x == 'Alex').sum()),
        Dave=('Drafter', lambda x: (x == 'Dave').sum()),
        Stu=('Drafter', lambda x: (x == 'Stu').sum())
    ).reset_index()
    # Add tournament columns for each tournament, with finishing position
    tourney_num_map = {}
    for f, tname in zip(csv_files, tournament_names):
        df = pd.read_csv(f)
        tnum = None
        if 'tourney_num' in df.columns:
            try:
                tnum = int(df['tourney_num'].iloc[0])
            except Exception:
                tnum = None
        tourney_num_map[tname] = tnum if tnum is not None else -1
        player_stats[tname] = player_stats['player_first_last'].map(tournament_pos_dicts[tname])
    # Order tournament columns by tourney_num descending (most recent first)
    sorted_tnames = sorted(tournament_names, key=lambda x: tourney_num_map.get(x, -1), reverse=True)
    cols = player_stats.columns.tolist()
    # Remove tournament columns from current position
    for tname in tournament_names:
        if tname in cols:
            cols.remove(tname)
    # Insert tournament columns after 'Stu', most recent first
    stu_idx = cols.index('Stu')
    for i, tname in enumerate(sorted_tnames):
        cols.insert(stu_idx + 1 + i, tname)
    player_stats = player_stats[cols]
    # Sort by Season Points descending
    player_stats = player_stats.sort_values('Season_Points', ascending=False).reset_index(drop=True)
    # Compute ranking with ties: all tied values get same integer (no 'T' prefix)
    ranks = player_stats['Season_Points'].rank(method='min', ascending=False).astype(int)
    player_stats.insert(0, 'Pos', ranks.astype(str).tolist())

    def style_tournament_cols(row):
        def pos_color(val):
            if pd.isna(val) or val is None or str(val).strip() == '':
                return ''
            pos_str = str(val).strip().upper()
            if pos_str in ('WD', 'CUT', 'MC', ''):
                return 'background-color: rgba(139, 0, 0, 0.3); color: white'
            if pos_str.startswith('T'):
                pos_str = pos_str[1:]
            try:
                pos_num = int(pos_str)
            except:
                return 'background-color: rgba(139, 0, 0, 0.3); color: white'
            if pos_num == 1:
                color = 'rgba(144, 238, 144, 0.5)'
            elif 2 <= pos_num <= 5:
                color = 'rgba(50, 205, 50, 0.5)'
            elif 6 <= pos_num <= 10:
                color = 'rgba(34, 139, 34, 0.5)'
            elif 11 <= pos_num <= 25:
                color = 'rgba(0, 100, 0, 0.5)'
            else:
                color = 'rgba(0, 100, 0, 0.2)'
            return f'background-color: {color}; color: white'
        styled = [''] * len(row)
        col_idx = {col: i for i, col in enumerate(row.index)}
        # Style all tournament columns
        for tname in tournament_names:
            if tname in col_idx:
                styled[col_idx[tname]] = pos_color(row[tname])
        return styled

    # Build column_config for all tournament columns
    column_config = {
        'Pos': st.column_config.NumberColumn('Pos'),
        'player_first_last': st.column_config.TextColumn('Player'),
        'Season_Points': st.column_config.NumberColumn('Season Points'),
        'Events': st.column_config.NumberColumn('Events'),
        'Alex': st.column_config.NumberColumn('Alex'),
        'Dave': st.column_config.NumberColumn('Dave'),
        'Stu': st.column_config.NumberColumn('Stu'),
    }
    for tname in tournament_names:
        column_config[tname] = st.column_config.TextColumn(tname)

    styled_player_stats = player_stats.style.apply(style_tournament_cols, axis=1)
    st.dataframe(styled_player_stats, hide_index=True, width='stretch', column_config=column_config)
else:
    st.info("No drafted points results data available.")


# --- All Players Season Standings ---
st.divider()
st.markdown('<a id="all-players-season-standings"></a>', unsafe_allow_html=True)
st.subheader("All Players Season Standings")
st.write("This table includes all players from all tournaments. Updated April 19, 2026, after RBC Heritage completion.")

# Find all full_field_points_results CSVs and extract tourney_num and event_name
import glob
full_field_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'full_field_points_results' in f]
full_field_dfs = []
tourney_info = []  # (tourney_num, event_name, file)
tournament_pos_dicts = {}
for f in full_field_files:
    try:
        df = pd.read_csv(f)
        # Try to get tourney_num from first row
        if 'tourney_num' in df.columns:
            tnum = int(df['tourney_num'].iloc[0])
        else:
            tnum = None
        # Use the first word before the underscore in the filename as the short column name
        short_col = f.split('_')[0]
        tourney_info.append((tnum, short_col, f))
        full_field_dfs.append(df)
        # Build player:pos dict for this tournament using short_col as key
        tournament_pos_dicts[short_col] = dict(zip(df['player_first_last'], df['current_pos']))
    except Exception as e:
        st.warning(f"Could not load {f}: {e}")

if full_field_dfs:
    # Sort tournaments by tourney_num descending
    tourney_info = [t for t in tourney_info if t[0] is not None]
    tourney_info.sort(key=lambda x: -x[0])
    # Use the text before the first underscore in the filename as the column name
    tournament_cols = []
    for tnum, short_col, fname in tourney_info:
        tournament_cols.append(short_col)
    # Concat all data
    all_full_field = pd.concat(full_field_dfs, ignore_index=True)
    all_full_field.columns = [c.lstrip(',') for c in all_full_field.columns]
    # Group by player and add Events column (count unique events)
    if 'event_name' in all_full_field.columns:
        player_stats = all_full_field.groupby('player_first_last').agg(
            Season_Points=('current_points', 'sum'),
            Events=('event_name', 'nunique')
        ).reset_index()
    elif 'tourney_num' in all_full_field.columns:
        player_stats = all_full_field.groupby('player_first_last').agg(
            Season_Points=('current_points', 'sum'),
            Events=('tourney_num', 'nunique')
        ).reset_index()
    else:
        # Fallback to row count if no event identifier is present
        player_stats = all_full_field.groupby('player_first_last').agg(
            Season_Points=('current_points', 'sum'),
            Events=('player_first_last', 'count')
        ).reset_index()
    # Add tournament columns for each tournament, with finishing position
    for short_col in tournament_cols:
        player_stats[short_col] = player_stats['player_first_last'].map(tournament_pos_dicts[short_col])
    # Move tournament columns to right of Events, in order
    cols = player_stats.columns.tolist()
    # Remove duplicates from tournament_cols while preserving order
    seen = set()
    unique_tournament_cols = []
    for col in tournament_cols:
        if col not in seen:
            unique_tournament_cols.append(col)
            seen.add(col)
    # Remove tournament columns from current position if present
    for short_col in unique_tournament_cols:
        if short_col in cols:
            cols.remove(short_col)
    events_idx = cols.index('Events')
    for i, short_col in enumerate(unique_tournament_cols):
        cols.insert(events_idx + 1 + i, short_col)
    # Remove any duplicate columns in the final list
    final_cols = []
    seen_final = set()
    for col in cols:
        if col not in seen_final:
            final_cols.append(col)
            seen_final.add(col)
    player_stats = player_stats[final_cols]
    # Sort by Season Points descending
    player_stats = player_stats.sort_values('Season_Points', ascending=False).reset_index(drop=True)
    # Compute ranking with ties
    ranks = player_stats['Season_Points'].rank(method='min', ascending=False).astype(int)
    player_stats.insert(0, 'Pos', ranks.astype(str).tolist())

    def style_tournament_cols(row):
        def pos_color(val):
            if pd.isna(val) or val is None or str(val).strip() == '':
                return ''
            pos_str = str(val).strip().upper()
            if pos_str in ('WD', 'CUT', 'MC', ''):
                return 'background-color: rgba(139, 0, 0, 0.3); color: white'
            if pos_str.startswith('T'):
                pos_str = pos_str[1:]
            try:
                pos_num = int(pos_str)
            except:
                return 'background-color: rgba(139, 0, 0, 0.3); color: white'
            if pos_num == 1:
                color = 'rgba(144, 238, 144, 0.5)'
            elif 2 <= pos_num <= 5:
                color = 'rgba(50, 205, 50, 0.5)'
            elif 6 <= pos_num <= 10:
                color = 'rgba(34, 139, 34, 0.5)'
            elif 11 <= pos_num <= 25:
                color = 'rgba(0, 100, 0, 0.5)'
            else:
                color = 'rgba(0, 100, 0, 0.2)'
            return f'background-color: {color}; color: white'
        styled = [''] * len(row)
        col_idx = {col: i for i, col in enumerate(row.index)}
        for short_col in tournament_cols:
            if short_col in col_idx:
                val = row[short_col]
                # Only apply pos_color if val is a scalar (not a Series)
                if not hasattr(val, "__len__") or isinstance(val, str):
                    styled[col_idx[short_col]] = pos_color(val)
                else:
                    styled[col_idx[short_col]] = ''
        return styled

    # Build column_config for all tournament columns
    column_config = {
        'Pos': st.column_config.NumberColumn('Pos'),
        'player_first_last': st.column_config.TextColumn('Player'),
        'Season_Points': st.column_config.NumberColumn('Season Points', format='%d'),
        'Events': st.column_config.NumberColumn('Events'),
    }
    for short_col in tournament_cols:
        column_config[short_col] = st.column_config.TextColumn(short_col)

    styled_all_players = player_stats.style.apply(style_tournament_cols, axis=1)
    st.dataframe(styled_all_players, hide_index=True, width='stretch', column_config=column_config)
else:
    st.info("No full field points results data available.")


# --- Round Leads Table (Moved to Bottom) ---


# st.markdown('<a id="round-leads"></a>', unsafe_allow_html=True)
# st.subheader("Round Leads")
# st.write("This table shows, for all players in any tournament, how many times they held or shared the lead at the end of each round (R1-R4) for the entire season. A lead is defined as the lowest or tied-lowest score for that round in any event.")

# import collections
# if 'full_field_dfs' in globals() and full_field_dfs:
#     # Aggregate all round leads
#     lead_counts = collections.defaultdict(lambda: [0, 0, 0, 0])  # player: [R1, R2, R3, R4]
#     for df in full_field_dfs:
#         for i, round_col in enumerate(['R1', 'R2', 'R3', 'R4']):
#             if round_col in df.columns:
#                 # Find the minimum score for this round (ignore NaN)
#                 min_score = pd.to_numeric(df[round_col], errors='coerce').min()
#                 if pd.isna(min_score):
#                     continue
#                 # Find all players with this score
#                 leaders = df.loc[pd.to_numeric(df[round_col], errors='coerce') == min_score, 'player_first_last']
#                 for player in leaders:
#                     lead_counts[player][i] += 1
#     # Build DataFrame
#     round_leads_df = pd.DataFrame([
#         {'Player': player, 'Rnd 1 Lead': counts[0], 'Rnd 2 Lead': counts[1], 'Rnd 3 Lead': counts[2], 'Rnd 4 Lead': counts[3]}
#         for player, counts in lead_counts.items()
#     ])
#     # Sort by Rnd 4 Lead descending, then Rnd 3, 2, 1
#     round_leads_df = round_leads_df.sort_values(['Rnd 4 Lead', 'Rnd 3 Lead', 'Rnd 2 Lead', 'Rnd 1 Lead'], ascending=False).reset_index(drop=True)
#     st.dataframe(round_leads_df, hide_index=True, width='stretch', column_config={
#         'Player': st.column_config.TextColumn('Player'),
#         'Rnd 1 Lead': st.column_config.NumberColumn('Rnd 1 Lead'),
#         'Rnd 2 Lead': st.column_config.NumberColumn('Rnd 2 Lead'),
#         'Rnd 3 Lead': st.column_config.NumberColumn('Rnd 3 Lead'),
#         'Rnd 4 Lead': st.column_config.NumberColumn('Rnd 4 Lead'),
#     })
# else:
#     st.info("No full field points results data available for round leads.")
# # --- Player Performance Last 16 Rounds ---
# st.divider()
# st.markdown('<a id="player-performance-last16"></a>', unsafe_allow_html=True)
# st.subheader("All Players: Performance Last 16 Rounds")
# st.write("Each row shows a player's average stats for their most recent 16 rounds played in 2026. This table updates after every tournament.")


# @st.cache_data(ttl=300)
# def load_last16_stats():
#     url = "https://feeds.datagolf.com/historical-raw-data/rounds?tour=pga&event_id=all&year=2026&file_format=json&key=57b951c096fc3f4eb093c152f5a5"
#     try:
#         data = requests.get(url).json()
#         rows = []
#         for event in data.values():
#             event_id = event['event_id']
#             event_name = event['event_name']
#             for round_num in range(1, 5):
#                 for player in event['scores']:
#                     player_name = player['player_name']
#                     round_data = player.get(f'round_{round_num}')
#                     if round_data:
#                         row = {'player_name': player_name, 'event_id': int(event_id), 'event_name': event_name, 'round_num': round_num}
#                         row.update(round_data)
#                         rows.append(row)
#         df = pd.DataFrame(rows)
#         if df.empty:
#             return df
#         df = df.sort_values(['player_name', 'event_id', 'round_num'])
#         def get_last_16(group):
#             return group.tail(16)
#         last16 = df.groupby('player_name', group_keys=False).apply(get_last_16)
#         stats = ['sg_total', 'sg_t2g', 'sg_ott', 'sg_app', 'sg_arg', 'sg_putt', 'gir', 'driving_dist', 'driving_acc', 'score']
#         avg_stats = last16.groupby('player_name')[stats].mean().reset_index()
#         avg_stats = avg_stats.rename(columns={'score': 'round_score'})
#         return avg_stats
#     except Exception as e:
#         st.error(f"Failed to load last 16 rounds stats: {e}")
#         return pd.DataFrame()



# last16_df = load_last16_stats()
# if not last16_df.empty:
#     # Sort by SG: Total descending before display
#     last16_df = last16_df.sort_values('sg_total', ascending=False).reset_index(drop=True)
#     # Reformat player_name from 'Last, First' to 'First Last'
#     def reformat_name(name):
#         parts = name.split(', ')
#         if len(parts) == 2:
#             return f"{parts[1]} {parts[0]}"
#         return name
#     last16_df['player_name'] = last16_df['player_name'].apply(reformat_name)
#     st.dataframe(
#         last16_df,
#         width='stretch',
#         hide_index=True,
#         column_config={
#             'player_name': st.column_config.TextColumn('Player'),
#             'sg_total': st.column_config.NumberColumn('SG: Total', format='%.2f'),
#             'sg_t2g': st.column_config.NumberColumn('SG: Tee to Green', format='%.2f'),
#             'sg_ott': st.column_config.NumberColumn('SG: Off the Tee', format='%.2f'),
#             'sg_app': st.column_config.NumberColumn('SG: Approach', format='%.2f'),
#             'sg_arg': st.column_config.NumberColumn('SG: Around Green', format='%.2f'),
#             'sg_putt': st.column_config.NumberColumn('SG: Putting', format='%.2f'),
#             'gir': st.column_config.NumberColumn('GIR', format='%.2f'),
#             'driving_dist': st.column_config.NumberColumn('Driving Dist', format='%.2f'),
#             'driving_acc': st.column_config.NumberColumn('Driving Acc', format='%.2f'),
#             'round_score': st.column_config.NumberColumn('Score', format='%.2f'),
#         },
#     )


# # --- Current Event Player Performance Last 16 Rounds ---
# st.divider()
# st.markdown('<a id="current-event-player-performance-last16"></a>', unsafe_allow_html=True)
# st.subheader("Current Event Players: Performance Last 16 Rounds")
# st.write("This table shows the last 16 round stats for players in the current event (Full Field Detailed Pre-Tournament Projections table).")

# if not last16_df.empty and 'player_first_last' in dg_pga_pre_tournament_predictions_df.columns:
#     # Get set of current event player names (already in First Last format)
#     event_players = set(dg_pga_pre_tournament_predictions_df['player_first_last'].unique())
#     # Filter last16_df to only those players
#     filtered_last16 = last16_df[last16_df['player_name'].isin(event_players)].copy()
#     filtered_last16 = filtered_last16.sort_values('sg_total', ascending=False).reset_index(drop=True)
#     st.dataframe(
#         filtered_last16,
#         width='stretch',
#         hide_index=True,
#         column_config={
#             'player_name': st.column_config.TextColumn('Player'),
#             'sg_total': st.column_config.NumberColumn('SG: Total', format='%.2f'),
#             'sg_t2g': st.column_config.NumberColumn('SG: Tee to Green', format='%.2f'),
#             'sg_ott': st.column_config.NumberColumn('SG: Off the Tee', format='%.2f'),
#             'sg_app': st.column_config.NumberColumn('SG: Approach', format='%.2f'),
#             'sg_arg': st.column_config.NumberColumn('SG: Around Green', format='%.2f'),
#             'sg_putt': st.column_config.NumberColumn('SG: Putting', format='%.2f'),
#             'gir': st.column_config.NumberColumn('GIR', format='%.2f'),
#             'driving_dist': st.column_config.NumberColumn('Driving Dist', format='%.2f'),
#             'driving_acc': st.column_config.NumberColumn('Driving Acc', format='%.2f'),
#             'round_score': st.column_config.NumberColumn('Score', format='%.2f'),
#         },
#     )
# else:
#     st.info("No current event last 16 rounds stats available.")

# --- All Players: Performance 2026 ---
st.divider()
st.markdown('<a id="player-performance-2026"></a>', unsafe_allow_html=True)
st.subheader("All Players: Performance 2026")
st.write("Each row shows a player's average stats for all measured rounds played in 2026. The 'Measured Rounds' column shows the total number of rounds for each player.")

@st.cache_data(ttl=300)
def load_all_2026_stats():
    url = "https://feeds.datagolf.com/historical-raw-data/rounds?tour=pga&event_id=all&year=2026&file_format=json&key=57b951c096fc3f4eb093c152f5a5"
    try:
        data = requests.get(url).json()
        rows = []
        for event in data.values():
            event_id = event['event_id']
            event_name = event['event_name']
            for round_num in range(1, 5):
                for player in event['scores']:
                    player_name = player['player_name']
                    round_data = player.get(f'round_{round_num}')
                    if round_data:
                        row = {'player_name': player_name, 'event_id': int(event_id), 'event_name': event_name, 'round_num': round_num}
                        row.update(round_data)
                        rows.append(row)
        df = pd.DataFrame(rows)
        if df.empty:
            return df
        df = df.sort_values(['player_name', 'event_id', 'round_num'])
        stats = ['sg_total', 'sg_t2g', 'sg_ott', 'sg_app', 'sg_arg', 'sg_putt', 'gir', 'driving_dist', 'driving_acc', 'score']
        avg_stats = df.groupby('player_name')[stats].mean().reset_index()
        avg_stats = avg_stats.rename(columns={'score': 'round_score'})
        avg_stats['Measured Rounds'] = df.groupby('player_name').size().values
        # Reformat player_name from 'Last, First' to 'First Last'
        def reformat_name(name):
            parts = name.split(', ')
            if len(parts) == 2:
                return f"{parts[1]} {parts[0]}"
            return name
        avg_stats['player_name'] = avg_stats['player_name'].apply(reformat_name)
        return avg_stats
    except Exception as e:
        st.error(f"Failed to load 2026 stats: {e}")
        return pd.DataFrame()

all2026_df = load_all_2026_stats()
if not all2026_df.empty:
    all2026_df = all2026_df.sort_values('sg_total', ascending=False).reset_index(drop=True)
    st.dataframe(
        all2026_df,
        width='stretch',
        hide_index=True,
        column_config={
            'player_name': st.column_config.TextColumn('Player'),
            'sg_total': st.column_config.NumberColumn('SG: Total', format='%.2f'),
            'sg_t2g': st.column_config.NumberColumn('SG: Tee to Green', format='%.2f'),
            'sg_ott': st.column_config.NumberColumn('SG: Off the Tee', format='%.2f'),
            'sg_app': st.column_config.NumberColumn('SG: Approach', format='%.2f'),
            'sg_arg': st.column_config.NumberColumn('SG: Around Green', format='%.2f'),
            'sg_putt': st.column_config.NumberColumn('SG: Putting', format='%.2f'),
            'gir': st.column_config.NumberColumn('GIR', format='%.2f'),
            'driving_dist': st.column_config.NumberColumn('Driving Dist', format='%.2f'),
            'driving_acc': st.column_config.NumberColumn('Driving Acc', format='%.2f'),
            'round_score': st.column_config.NumberColumn('Score', format='%.2f'),
            'Measured Rounds': st.column_config.NumberColumn('Measured Rounds', format='%d'),
        },
    )
else:
    st.info("No 2026 player stats available.")

# --- Current Event Players: Performance 2026 ---
st.divider()
st.markdown('<a id="current-event-player-performance-2026"></a>', unsafe_allow_html=True)
st.subheader("Current Event Players: Performance 2026")
st.write("This table shows the 2026 stats for players in the current event (Full Field Detailed Pre-Tournament Projections table). The 'Measured Rounds' column shows the total number of rounds for each player.")

if not all2026_df.empty and 'player_first_last' in dg_pga_pre_tournament_predictions_df.columns:
    event_players = set(dg_pga_pre_tournament_predictions_df['player_first_last'].unique())
    filtered_2026 = all2026_df[all2026_df['player_name'].isin(event_players)].copy()
    filtered_2026 = filtered_2026.sort_values('sg_total', ascending=False).reset_index(drop=True)
    st.dataframe(
        filtered_2026,
        width='stretch',
        hide_index=True,
        column_config={
            'player_name': st.column_config.TextColumn('Player'),
            'sg_total': st.column_config.NumberColumn('SG: Total', format='%.2f'),
            'sg_t2g': st.column_config.NumberColumn('SG: Tee to Green', format='%.2f'),
            'sg_ott': st.column_config.NumberColumn('SG: Off the Tee', format='%.2f'),
            'sg_app': st.column_config.NumberColumn('SG: Approach', format='%.2f'),
            'sg_arg': st.column_config.NumberColumn('SG: Around Green', format='%.2f'),
            'sg_putt': st.column_config.NumberColumn('SG: Putting', format='%.2f'),
            'gir': st.column_config.NumberColumn('GIR', format='%.2f'),
            'driving_dist': st.column_config.NumberColumn('Driving Dist', format='%.2f'),
            'driving_acc': st.column_config.NumberColumn('Driving Acc', format='%.2f'),
            'round_score': st.column_config.NumberColumn('Score', format='%.2f'),
            'Measured Rounds': st.column_config.NumberColumn('Measured Rounds', format='%d'),
        },
    )
else:
    st.info("No current event 2026 stats available.")


# --- Drafters Points Gained Per Round ---
st.divider()
st.markdown('<a id="drafters-points-gained-per-round"></a>', unsafe_allow_html=True)
st.subheader("Drafters Points Gained Per Round")
st.write("Each value is calculated as drafter average points minus the season average points per drafter for that round. For example, if a drafter's Draft Round 2 value is +1.7, that means per tournament, the golfer they draft in Round 2 has scored an average of 1.7 more points than the other drafters' golfers in Round 2.")

round_gain_files = [f for f in os.listdir('.') if f.endswith('.csv') and 'drafted_points_result' in f]
round_gain_dfs = []
for f in round_gain_files:
    try:
        df = pd.read_csv(f)
        df.columns = [c.lstrip(',') for c in df.columns]
        required_cols = {'Drafter', 'Round', 'current_points'}
        if required_cols.issubset(df.columns):
            trimmed = df[['Drafter', 'Round', 'current_points']].copy()
            trimmed['Round'] = pd.to_numeric(trimmed['Round'], errors='coerce')
            trimmed['current_points'] = pd.to_numeric(trimmed['current_points'], errors='coerce')
            round_gain_dfs.append(trimmed)
    except Exception as e:
        st.warning(f"Could not load {f}: {e}")

if round_gain_dfs:
    round_gain_data = pd.concat(round_gain_dfs, ignore_index=True)
    round_gain_data = round_gain_data[round_gain_data['Drafter'].isin(['Alex', 'Dave', 'Stu'])]
    round_gain_data = round_gain_data.dropna(subset=['Round', 'current_points'])
    round_gain_data['Round'] = round_gain_data['Round'].astype(int)
    round_gain_data = round_gain_data[round_gain_data['Round'].between(1, 8)]

    if not round_gain_data.empty:
        season_round_avg = round_gain_data.groupby('Round')['current_points'].mean()

        deltas_df = pd.DataFrame({'Draft Round': list(range(1, 9))})
        for drafter in ['Alex', 'Dave', 'Stu']:
            drafter_round_avg = (
                round_gain_data[round_gain_data['Drafter'] == drafter]
                .groupby('Round')['current_points']
                .mean()
            )
            deltas_df[drafter] = deltas_df['Draft Round'].map(drafter_round_avg - season_round_avg)

        deltas_df[['Alex', 'Dave', 'Stu']] = deltas_df[['Alex', 'Dave', 'Stu']].round(1)

        total_row = pd.DataFrame({
            'Draft Round': ['Total'],
            'Alex': [deltas_df['Alex'].sum()],
            'Dave': [deltas_df['Dave'].sum()],
            'Stu': [deltas_df['Stu'].sum()],
        })
        total_row[['Alex', 'Dave', 'Stu']] = total_row[['Alex', 'Dave', 'Stu']].round(1)
        deltas_df = pd.concat([deltas_df, total_row], ignore_index=True)

        def style_round_gain_threshold(row):
            styles = [''] * len(row)
            for idx, col in [(1, 'Alex'), (2, 'Dave'), (3, 'Stu')]:
                val = pd.to_numeric(row[col], errors='coerce')
                if pd.isna(val):
                    styles[idx] = ''
                elif val <= -2:
                    styles[idx] = 'background-color: rgba(255, 22, 12, 0.6); color: white'
                elif -2 < val < 0:
                    styles[idx] = 'background-color: rgba(139, 0, 0, 0.6); color: white'
                elif 0 <= val < 2:
                    styles[idx] = 'background-color: rgba(0, 100, 0, 0.6); color: white'
                else:
                    styles[idx] = 'background-color: rgba(144, 238, 144, 0.6); color: white'
            return styles

        styled_deltas_df = deltas_df.style.apply(style_round_gain_threshold, axis=1).format({
            'Alex': lambda v: f'+{v:.1f}' if pd.notna(v) and v > 0 else (f'{v:.1f}' if pd.notna(v) else ''),
            'Dave': lambda v: f'+{v:.1f}' if pd.notna(v) and v > 0 else (f'{v:.1f}' if pd.notna(v) else ''),
            'Stu': lambda v: f'+{v:.1f}' if pd.notna(v) and v > 0 else (f'{v:.1f}' if pd.notna(v) else ''),
        })

        st.dataframe(
            styled_deltas_df,
            width='stretch',
            hide_index=True,
            column_config={
                'Draft Round': st.column_config.TextColumn('Draft Round'),
                'Alex': st.column_config.TextColumn('Alex'),
                'Dave': st.column_config.TextColumn('Dave'),
                'Stu': st.column_config.TextColumn('Stu'),
            },
        )
    else:
        st.info("No drafted round data available for rounds 1-8.")
else:
    st.info("No drafted points results data available.")
