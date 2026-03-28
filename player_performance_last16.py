import requests
import pandas as pd

def get_last_16_rounds_stats():
    url = "https://feeds.datagolf.com/historical-raw-data/rounds?tour=pga&event_id=all&year=2026&file_format=json&key=57b951c096fc3f4eb093c152f5a5"
    response = requests.get(url)
    data = response.json()
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
    # Sort by event_id and round_num (both ascending)
    df = df.sort_values(['player_name', 'event_id', 'round_num'])
    # For each player, get their most recent 16 rounds
    def get_last_16(group):
        return group.tail(16)
    last16 = df.groupby('player_name', group_keys=False).apply(get_last_16)
    # Compute averages for each stat
    stats = ['sg_total', 'sg_t2g', 'sg_ott', 'sg_app', 'sg_arg', 'sg_putt', 'gir', 'driving_dist', 'driving_acc', 'score']
    avg_stats = last16.groupby('player_name')[stats].mean().reset_index()
    avg_stats = avg_stats.rename(columns={'score': 'round_score'})
    return avg_stats
