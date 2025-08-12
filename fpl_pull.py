import os,requests,pandas as pd
os.makedirs("data",exist_ok=True)
seasons={"2023/24","2024/25"}
b=requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
teams={t["id"]:t["name"] for t in b["teams"]}
pos={1:"GK",2:"DEF",3:"MID",4:"FWD"}
rows=[]
for p in b["elements"]:
    h=requests.get(f"https://fantasy.premierleague.com/api/element-summary/{p['id']}/").json()
    for s in h.get("history_past",[]):
        if s["season_name"] in seasons:
            rows.append({"fpl_id":p["id"],"full_name":f"{p['first_name']} {p['second_name']}","team":teams.get(p["team"]),"position":pos.get(p["element_type"]),"season":s["season_name"],"minutes":s["minutes"],"goals":s["goals_scored"],"assists":s["assists"],"clean_sheets":s["clean_sheets"],"goals_conceded":s["goals_conceded"],"yellow_cards":s["yellow_cards"],"red_cards":s["red_cards"],"saves":s.get("saves",0),"penalties_saved":s.get("penalties_saved",0),"penalties_missed":s.get("penalties_missed",0),"own_goals":s.get("own_goals",0)})
pd.DataFrame(rows).to_csv("data/fpl_season_totals.csv",index=False)
