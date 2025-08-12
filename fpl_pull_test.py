import argparse
import pandas as pd
import requests
import os

def fetch_fpl_data(season):
    # Season ID mapping for FPL API (22/23 = 2022, 23/24 = 2023, etc.)
    url = f"https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch FPL data: {response.status_code}")

    data = response.json()
    players_df = pd.DataFrame(data["elements"])
    teams_df = pd.DataFrame(data["teams"])
    positions_df = pd.DataFrame(data["element_types"])

    # Merge to get readable team and position names
    players_df = players_df.merge(teams_df[["id", "name"]], left_on="team", right_on="id", suffixes=("", "_team"))
    players_df = players_df.merge(positions_df[["id", "singular_name"]], left_on="element_type", right_on="id", suffixes=("", "_pos"))

    return players_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--season", type=int, required=True, help="Season start year (e.g., 2022 for 22/23 season)")
    parser.add_argument("--out", type=str, required=True, help="Output CSV path (e.g., test/fpl_2022.csv)")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    df = fetch_fpl_data(args.season)
    df.to_csv(args.out, index=False)
    print(f"✅ Saved FPL data for {args.season} season to {args.out}")
