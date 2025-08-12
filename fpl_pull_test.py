import os, argparse, requests, pandas as pd
os.makedirs("test", exist_ok=True)
ap = argparse.ArgumentParser()
ap.add_argument("--seasons", type=str, default="2022/23,2023/24")
ap.add_argument("--out", type=str, default="test/fpl_season_totals_2022_2023.csv")
a = ap.parse_args()
seasons = set([s.strip() for s in a.seasons.split(",") if s.strip()])
b = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
teams = {t["id"]: t["name"] for t in b["teams"]}
pos = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}
rows = []
for p in b["elements"]:
    h = requests.get(f"https://fantasy.premierleague.com/api/element-summary/{p['id']}/").json().get("history_past", [])
    for s in h:
        if s["season_name"] in seasons:
            rows.append({
                "fpl_id": p["id"],
                "full_name": f"{p['first_name']} {p['second_name']}",
                "latest_team": teams.get(p["team"]),
                "position": pos.get(p["element_type"]),
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
                "own_goals": s.get("own_goals", 0),
                "bonus": s.get("bonus", 0)
            })
pd.DataFrame(rows).to_csv(a.out, index=False)
print(a.out)
