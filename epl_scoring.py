import os,requests,pandas as pd
os.makedirs("data",exist_ok=True)
base=pd.read_csv("data/fpl_season_totals.csv")
need=["fpl_id","full_name","position","team","season","minutes"]
for c in need:
    if c not in base.columns: raise ValueError(f"Missing column: {c}")
uids=sorted(base["fpl_id"].unique())
seasons_keep={"2023/24","2024/25"}
rows=[]
for pid in uids:
    h=requests.get(f"https://fantasy.premierleague.com/api/element-summary/{int(pid)}/").json().get("history_past",[])
    for s in h:
        if s["season_name"] in seasons_keep:
            rows.append({"fpl_id":pid,"season":s["season_name"],"total_points":s["total_points"]})
tp=pd.DataFrame(rows)
meta=(base.sort_values(["fpl_id","season"]).drop_duplicates(["fpl_id","season"],keep="last")[need])
df=meta.merge(tp,how="left",on=["fpl_id","season"])
order={"2023/24":1,"2024/25":2}
latest_team=(df.sort_values(["fpl_id","season"],key=lambda s:s.map(order)).drop_duplicates("fpl_id",keep="last")[["fpl_id","team"]].rename(columns={"team":"latest_team"}))
pts=df.pivot_table(index=["fpl_id"],columns="season",values="total_points",aggfunc="sum").reset_index()
mins=df.pivot_table(index=["fpl_id"],columns="season",values="minutes",aggfunc="sum").reset_index()
pts.columns=["fpl_id"]+[str(c) for c in pts.columns[1:]]
mins.columns=["fpl_id"]+[f"min_{c}" for c in mins.columns[1:]]
out=(pts.merge(mins,on="fpl_id").merge(base[["fpl_id","full_name","position"]].drop_duplicates("fpl_id"),on="fpl_id",how="left").merge(latest_team,on="fpl_id",how="left"))
for s in ["2023/24","2024/25"]:
    if s not in out.columns: out[s]=0
    if f"min_{s}" not in out.columns: out[f"min_{s}"]=0
out.to_csv("data/fpl_epl_scored.csv",index=False)