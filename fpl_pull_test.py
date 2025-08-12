import os
import requests
import pandas as pd

os.makedirs("test", exist_ok=True)

# Seasons we want
seasons = {"2022/23", "2023/24"}

# Get bootstrap data
bootstrap = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
teams = {t["id"]: t["name"] for t in bootstrap["teams"]}
positions = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}

rows = []

for player in bootstrap["elements"]:
    history = requests.get(f"https://fantasy.premierleague.com/api/element-summary/{player['id']}/").json()
    for s in history.get("history_past", []):
        if s["season_name"] in seasons:
            rows.append({
                "fpl_id": player["id"],
                "full_name": f"{player['first_name']} {player['second_name']}",
                "team": teams.get(player["team"]),
                "position": positions.get(player["element_type"]),
                "season": s["season_name"],
                "minutes": s["minutes"],
                "goals": s["goals_scored"],
                "assists": s["assists"],
                "clean_sheets": s["clean_sheets"],
                "goals_conceded": s["goals_conceded"],
                "yellow_cards": s["yellow_cards"],
                "red_cards": s["red_cards"],
                "saves": s.get("saves", 0),
                "penalties_saved": s.get("penalties_saved", 0),
                "penalties_missed": s.get("penalties_missed", 0),
                "own_goals": s.get("own_goals", 0)
            })

df = pd.DataFrame(rows)
csv_path = "test/fpl_season_totals_2022_2023.csv"
df.to_csv(csv_path, index=False)
print(f"✅ Saved to {csv_path} with {len(df)} rows")
