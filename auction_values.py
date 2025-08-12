import os,argparse,pandas as pd,numpy as np,re
os.makedirs("data",exist_ok=True)
ap=argparse.ArgumentParser()
ap.add_argument("--inp",type=str,default="data/fpl_epl_scored.csv")
ap.add_argument("--out",type=str,default="data/auction_board.csv")
ap.add_argument("--league-size",type=int,default=10)
ap.add_argument("--budget-per-team",type=float,default=200.0)
ap.add_argument("--spend-fraction",type=float,default=0.7)
ap.add_argument("--slots",type=str,default="GK:2,DEF:5,MID:5,FWD:3")
a=ap.parse_args()
def parse_slots(s):
    d={}
    for part in s.split(","):
        k,v=part.split(":")
        d[k.strip().upper()]=int(v)
    return d
df=pd.read_csv(a.inp)
need=["fpl_id","full_name","position","latest_team"]
for c in need:
    if c not in df.columns: raise ValueError(f"Missing column: {c}")
season_cols=[c for c in df.columns if re.fullmatch(r"\d{4}/\d{2}",str(c))]
if len(season_cols)<2: raise ValueError("Need at least two season total columns")
def s_key(s):
    try: return int(str(s).split("/")[0])
    except: return -1
season_cols=sorted(season_cols,key=s_key)
prev_season,cur_season=season_cols[-2],season_cols[-1]
m_prev,f_prev=f"min_{prev_season}",f"min_{cur_season}"
for c in [prev_season,cur_season,m_prev,f_prev]:
    if c not in df.columns: df[c]=0
def per90(p,m):
    m=np.where(m>0,m,np.nan)
    return (p/m)*90.0
r_cur=per90(df[cur_season].fillna(0).values,df[f_prev].fillna(0).values)
r_prev=per90(df[prev_season].fillna(0).values,df[m_prev].fillna(0).values)
rate_blend=np.nan_to_num(0.7*r_cur)+np.nan_to_num(0.3*r_prev)
mins_total=df[m_prev].fillna(0)+df[f_prev].fillna(0)
pos_med=pd.Series(rate_blend).groupby(df["position"]).transform("median")
K=1500.0
w=mins_total/(mins_total+K)
rate_adj=w*rate_blend+(1.0-w)*pos_med
cap=df.groupby("position").apply(lambda g: pd.Series({"cap":np.nanpercentile(rate_adj[g.index],95)}))["cap"]
df["rate_adj"]=np.minimum(rate_adj,df["position"].map(cap))
min_proj=(0.7*df[f_prev].fillna(0)+0.3*df[m_prev].fillna(0)).clip(lower=0,upper=3300)
avail_prev=(df[m_prev].fillna(0)/3420.0).clip(0,1)
avail_cur=(df[f_prev].fillna(0)/3420.0).clip(0,1)
avail_blend=0.7*avail_cur+0.3*avail_prev
min_proj=min_proj*(0.6+0.4*avail_blend)
df["proj_pts"]=np.maximum(0.0,df["rate_adj"]*(min_proj/90.0))
pos_slots=parse_slots(a.slots)
rep={}
for pos,slots in pos_slots.items():
    g=df[df["position"]==pos].sort_values("proj_pts",ascending=False).reset_index(drop=True)
    rep[pos]=float(g.loc[min(len(g)-1,slots*a.league_size),"proj_pts"]) if len(g)>0 else 0.0
df["rep_dyn"]=df["position"].map(rep).fillna(0.0)
df["vorp_dyn"]=(df["proj_pts"]-df["rep_dyn"]).clip(lower=0)
total_vorp=float(df["vorp_dyn"].sum())
dpp=(a.budget_per_team*a.league_size*a.spend_fraction)/total_vorp if total_vorp>0 else 0.0
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
    aav=pd.read_csv(aav_path)
    key=["fpl_id"] if "fpl_id" in aav.columns else ["full_name","position"]
    df=df.merge(aav,how="left",on=key)
else:
    df["aav"]=pd.NA
cols=["fpl_id","full_name","position","latest_team",prev_season,cur_season,f"min_{prev_season}",f"min_{cur_season}","proj_pts","rep_dyn","vorp_dyn","rec_bid_dyn","tier_dyn","aav"]
df[cols].sort_values(["position","rec_bid_dyn"],ascending=[True,False]).reset_index(drop=True).to_csv(a.out,index=False)
print(a.out)
