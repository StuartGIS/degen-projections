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
st.header("Farmers Insurance Open")
st.markdown("Torrey Pines, North Course, South Course  \nLa Jolla, California  \nJanuary 29- February 1, 2026")
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
    ("2026 Points System", "points-2026"),
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
draft_results = pd.read_csv("farmers_2026_draft_results.csv")

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
draft_results = pd.read_csv("farmers_2026_draft_results.csv")

# Anchor for: Draft Results
st.markdown('<a id="draft-results"></a>', unsafe_allow_html=True)
st.subheader("Draft Results")
st.dataframe(draft_results, width='stretch', hide_index=True)

# Season standings
st.markdown('<a id="season-standings"></a>', unsafe_allow_html=True)
st.subheader("Season Standings")
st.write("Updated Jan 27, 2026, after American Express completion.")

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
    avg_stats['Season Earnings'] = avg_stats['Drafter'].map({'Alex': '$0', 'Dave': '$20', 'Stu': '$0'})
    display_stats = avg_stats[['Drafter', 'Made Cut %', 'Top 25 %', 'Top 10 %', 'Top 5 %', 'Winner %', 'Winner Count', 'Points Win %', 'Points Win Count', 'Tournaments Played', 'Avg Weekly Points', 'Total Season Points', 'Season Earnings']].set_index('Drafter').T
    display_stats.index = ['Made Cut', 'Top 25', 'Top 10', 'Top 5', 'Winners %', 'Winners', 'Points Wins %', 'Points Wins', 'Tournaments Played', 'Avg Weekly Points', 'Total Season Points', 'Season Earnings']
    # Add Geography Wins row
    geography_wins = pd.Series({'Alex': 0, 'Dave': 2, 'Stu': 0})
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

# Load all drafted_points_results CSVs
csv_files = [
    "amex_2026_drafted_points_results_csv.csv",
    "sony_open_drafted_points_results_csv.csv"
]
dfs = []
for f in csv_files:
    try:
        df = pd.read_csv(f)
        dfs.append(df)
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
    # Add Amex and Sony current_pos columns
    amex = pd.read_csv('amex_2026_drafted_points_results_csv.csv')
    sony = pd.read_csv('sony_open_drafted_points_results_csv.csv')
    player_stats['Amex'] = player_stats['player_first_last'].map(
        dict(zip(amex['player_first_last'], amex['current_pos']))
    )
    player_stats['Sony'] = player_stats['player_first_last'].map(
        dict(zip(sony['player_first_last'], sony['current_pos']))
    )
    # Sort by Season Points descending
    player_stats = player_stats.sort_values('Season_Points', ascending=False).reset_index(drop=True)
    player_stats.insert(0, 'Pos', player_stats.index + 1)

    def style_amex_sony(row):
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
        for col in ['Amex', 'Sony']:
            if col in col_idx:
                styled[col_idx[col]] = pos_color(row[col])
        return styled

    styled_player_stats = player_stats.style.apply(style_amex_sony, axis=1)
    st.dataframe(styled_player_stats, hide_index=True, width='stretch', column_config={
        'Pos': st.column_config.NumberColumn('Pos'),
        'player_first_last': st.column_config.TextColumn('Player'),
        'Season_Points': st.column_config.NumberColumn('Season Points'),
        'Events': st.column_config.NumberColumn('Events'),
        'Alex': st.column_config.NumberColumn('Alex'),
        'Dave': st.column_config.NumberColumn('Dave'),
        'Stu': st.column_config.NumberColumn('Stu'),
        'Amex': st.column_config.TextColumn('Amex'),
        'Sony': st.column_config.TextColumn('Sony'),
    })
else:
    st.info("No drafted points results data available.")

