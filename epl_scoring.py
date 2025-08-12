import os, argparse, requests, pandas as pd
os.makedirs("data", exist_ok=True)
ap = argparse.ArgumentParser()
ap.add_argument("--inp", type=str, default="data/fpl_season_totals.csv")
ap.add_argument("--out", type=str, default="data/fpl_epl_scored.csv")
a = ap.parse_args()
base = pd.read_csv(a.inp)
need_any = ["fpl_id","full_name","position","season","minutes"]
for c in need_any:
    if c not in base.columns:
        raise ValueError(f"Missing column: {c}")
teamcol = "team" if "team" in base.columns else ("latest_team" if "latest_team" in base.columns else None)
uids = sorted(pd.unique(base["fpl_id"]))
def season_key(s):
    try:
        y = int(str(s).split("/")[0])
    except:
        y = 0
    return y
present = sorted(pd.unique(base["season"]), key=season_key)
if len(present) == 0:
    raise ValueError("No seasons found in input CSV")
keep = set(present[-2:]) if len(present) >= 2 else set(present)
rows = []
for pid in uids:
    h = requests.get(f"https://fantasy.premierleague.com/api/element-summary/{int(pid)}/").json().get("history_past", [])
    for s in h:
        if s.get("season_name") in keep:
            rows.append({"fpl_id": pid, "season": s["season_name"], "total_points": s.get("total_points", 0)})
tp = pd.DataFrame(rows)
meta_cols = ["fpl_id","full_name","position","season","minutes"] + ([teamcol] if teamcol else [])
meta = base.sort_values(["fpl_id","season"]).drop_duplicates(["fpl_id","season"], keep="last")[meta_cols]
df = meta.merge(tp, how="left", on=["fpl_id","season"])
if teamcol:
    latest_team = df.sort_values(["fpl_id","season"], key=lambda s: s.map(season_key)).drop_duplicates("fpl_id", keep="last")[["fpl_id", teamcol]].rename(columns={teamcol: "latest_team"})
else:
    latest_team = pd.DataFrame({"fpl_id": uids, "latest_team": pd.NA})
pts = df.pivot_table(index=["fpl_id"], columns="season", values="total_points", aggfunc="sum").reset_index()
mins = df.pivot_table(index=["fpl_id"], columns="season", values="minutes", aggfunc="sum").reset_index()
pts.columns = ["fpl_id"] + [str(c) for c in pts.columns[1:]]
mins.columns = ["fpl_id"] + [f"min_{c}" for c in mins.columns[1:]]
meta_names = base.sort_values("fpl_id").drop_duplicates("fpl_id")[["fpl_id","full_name","position"]]
out = pts.merge(mins, on="fpl_id").merge(meta_names, on="fpl_id", how="left").merge(latest_team, on="fpl_id", how="left")
for s in keep:
    col_pts = str(s)
    col_min = f"min_{s}"
    if col_pts not in out.columns: out[col_pts] = 0
    if col_min not in out.columns: out[col_min] = 0
out.to_csv(a.out, index=False)
print(a.out)
