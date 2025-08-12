import os,pandas as pd,numpy as np
os.makedirs("data",exist_ok=True)
league_size=10
pos_slots={"GK":2,"DEF":5,"MID":5,"FWD":3}
budget_per_team=200
spend_fraction=0.7
df=pd.read_csv("data/fpl_espn_scored.csv")
for c in ["fpl_id","full_name","position","latest_team","2023/24","2024/25","min_2023/24","min_2024/25"]:
    if c not in df.columns: raise ValueError(f"Missing column: {c}")
def per90(p,m):
    m=np.where(m>0,m,np.nan)
    return (p/m)*90.0
r24=per90(df["2024/25"].fillna(0).values,df["min_2024/25"].fillna(0).values)
r23=per90(df["2023/24"].fillna(0).values,df["min_2023/24"].fillna(0).values)
rate_blend=np.nan_to_num(0.7*r24)+np.nan_to_num(0.3*r23)
mins_total=df["min_2023/24"].fillna(0)+df["min_2024/25"].fillna(0)
pos_med=pd.Series(rate_blend).groupby(df["position"]).transform("median")
K=1500.0
w=mins_total/(mins_total+K)
rate_adj=w*rate_blend+(1.0-w)*pos_med
cap=df.groupby("position").apply(lambda g: pd.Series({"cap":np.nanpercentile(rate_adj[g.index],95)}))["cap"]
df["rate_adj"]=np.minimum(rate_adj,df["position"].map(cap))
min_proj=(0.7*df["min_2024/25"].fillna(0)+0.3*df["min_2023/24"].fillna(0)).clip(lower=0,upper=3300)
df["proj_pts"]=np.maximum(0.0,df["rate_adj"]*(min_proj/90.0))
rep={}
for pos,slots in pos_slots.items():
    g=df[df["position"]==pos].sort_values("proj_pts",ascending=False).reset_index(drop=True)
    rep[pos]=float(g.loc[min(len(g)-1,slots*league_size),"proj_pts"]) if len(g)>0 else 0.0
df["rep_dyn"]=df["position"].map(rep).fillna(0.0)
df["vorp_dyn"]=(df["proj_pts"]-df["rep_dyn"]).clip(lower=0)
total_vorp=float(df["vorp_dyn"].sum())
dpp=(budget_per_team*league_size*spend_fraction)/total_vorp if total_vorp>0 else 0.0
df["rec_bid_dyn"]=(df["vorp_dyn"]*dpp).round(2)
def tiers(x):
    x=x.sort_values("proj_pts",ascending=False).reset_index(drop=True)
    if len(x)<6:
        x["tier_dyn"]=1;return x
    q=x["proj_pts"].quantile([0.8,0.6,0.4,0.2]).tolist()
    def t(v):
        if v>=q[0]: return 1
        if v>=q[1]: return 2
        if v>=q[2]: return 3
        if v>=q[3]: return 4
        return 5
    x["tier_dyn"]=x["proj_pts"].apply(t);return x
df=df.groupby("position",group_keys=False).apply(tiers)
aav_path="data/last_season_aav.csv"
if os.path.exists(aav_path):
    aav=pd.read_csv(aav_path);key=["fpl_id"] if "fpl_id" in aav.columns else ["full_name","position"]
    df=df.merge(aav,how="left",on=key)
else:
    df["aav"]=pd.NA
cols=["fpl_id","full_name","position","latest_team","2023/24","2024/25","min_2023/24","min_2024/25","proj_pts","rep_dyn","vorp_dyn","rec_bid_dyn","tier_dyn","aav"]
df[cols].sort_values(["position","rec_bid_dyn"],ascending=[True,False]).reset_index(drop=True).to_csv("data/auction_board.csv",index=False)