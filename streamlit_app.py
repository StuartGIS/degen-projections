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
st.header("Sony Open")
st.markdown("Waiʻalae Country Club  \nHonolulu, Hawaii  \nJanuary 15-18, 2026")
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
    ("Season Standings", "season-standings"),
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



dg_pga_live_predictions_df = dg_pga_live_predictions_df[['current_pos', 'player_first_last', 'current_score', 'current_points', 'round', 'thru', 'today', 'R1', 'R2', 'R3', 'R4', 'win', 'top_5', 'top_10', 'make_cut', 'last_update', 'event_name']]

# Convert probability columns to percentages for display
dg_pga_live_predictions_df[['win', 'top_5', 'top_10', 'make_cut']] *= 100

# Sort by Score in ascending order
dg_pga_live_predictions_df = dg_pga_live_predictions_df.sort_values('current_score')

# Join draft results with live predictions and calculate projected points
draft_results = pd.read_csv("sony_2026_drafts_results_csv.csv")

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
st.dataframe(all_drafter_picks_df_live.reset_index(drop=True), width='stretch', hide_index=True)

# Anchor for: Drafted Players with Live-Tournament Projected Points
st.markdown('<a id="drafted-live"></a>', unsafe_allow_html=True)
st.subheader("Drafted Players Detailed Live-Tournament Scoring")
st.write("The 'Win', 'Top 5', 'Top 10' and 'Make Cut' columns reflect live DataGolf projections.")
st.dataframe(merged_players_live_preds_df.reset_index(drop=True), width='stretch', hide_index=True, column_config={
    'Round': st.column_config.TextColumn('Round'),
    'current_pos': st.column_config.TextColumn('Pos'),
    'player_first_last': st.column_config.TextColumn('Golfer'),
    'current_score': st.column_config.TextColumn('Score'),
    'current_points': st.column_config.NumberColumn('Points'),
    'thru': st.column_config.TextColumn('Thru'),
    'win': st.column_config.NumberColumn('Win', format='%.1f%%'),
    'top_5': st.column_config.NumberColumn('Top 5', format='%.1f%%'),
    'top_10': st.column_config.NumberColumn('Top 10', format='%.1f%%'),
    'make_cut': st.column_config.NumberColumn('Make Cut', format='%.1f%%')
})

st.divider()

# Anchor for: Datagolf Full Field Live Predictions
st.markdown('<a id="dg-full-field-live"></a>', unsafe_allow_html=True)
st.subheader("Full Field Detailed Live-Tournament Scoring")
st.dataframe(dg_pga_live_predictions_df.reset_index(drop=True), width='stretch', hide_index=True, column_config={
    'player_first_last': st.column_config.TextColumn('Golfer'),
    'current_score': st.column_config.TextColumn('Score'),
    'current_pos': st.column_config.TextColumn('Pos'),
    'current_points': st.column_config.NumberColumn('Points'),
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
draft_results = pd.read_csv("sony_2026_drafts_results_csv.csv")

# Anchor for: Draft Results
st.markdown('<a id="draft-results"></a>', unsafe_allow_html=True)
st.subheader("Draft Results")
st.dataframe(draft_results, width='stretch', hide_index=True)

# Season standings
st.markdown('<a id="season-standings"></a>', unsafe_allow_html=True)
st.subheader("Season Standings")
st.write("Updated Jan 19, 2026, after Sony Open completion.")

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
            winner_count=('win', 'sum'),
            sum_points=('current_points', 'sum'),
        ).reset_index()
        draft_stats['made_cut_pct'] = draft_stats['made_cut_count'] / draft_stats['total_players'] * 100
        draft_stats['top25_pct'] = draft_stats['top25_count'] / draft_stats['total_players'] * 100
        draft_stats['top10_pct'] = draft_stats['top10_count'] / draft_stats['total_players'] * 100
        draft_stats['top5_pct'] = draft_stats['top5_count'] / draft_stats['total_players'] * 100
        draft_stats['winner_pct'] = (draft_stats['winner_count'] > 0).astype(int) * 100
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
    avg_stats['Avg Weekly Points'] = avg_stats['avg_weekly_points'].round(2).map(lambda x: f"{x:.2f}")
    avg_stats['Total Season Points'] = avg_stats['total_season_points'].astype(str)
    avg_stats['Season Earnings'] = avg_stats['Drafter'].map({'Alex': '$0', 'Dave': '$10', 'Stu': '$0'})
    display_stats = avg_stats[['Drafter', 'Made Cut %', 'Top 25 %', 'Top 10 %', 'Top 5 %', 'Winner %', 'Winner Count', 'Points Win %', 'Points Win Count', 'Tournaments Played', 'Avg Weekly Points', 'Total Season Points', 'Season Earnings']].set_index('Drafter').T
    display_stats.index = ['Made Cut', 'Top 25', 'Top 10', 'Top 5', 'Winners %', 'Winners', 'Points Wins %', 'Points Wins', 'Tournaments Played', 'Avg Weekly Points', 'Total Season Points', 'Season Earnings']
    
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
        highest = ranks[0]
        second = ranks[1] if len(ranks) > 1 else highest
        lowest = ranks[-1]
        styles = []
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

# Convert probability columns to percentages for display
merged_players_pretourney_preds_df[['win', 'top_5', 'top_10', 'top_25', 'make_cut']] *= 100

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

