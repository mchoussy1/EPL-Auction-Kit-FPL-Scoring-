import os,pandas as pd
os.makedirs("cheatsheets",exist_ok=True)
df=pd.read_csv("data/auction_board.csv")
df=df.sort_values(["rec_bid_dyn","proj_pts"],ascending=[False,False]).reset_index(drop=True)
df[["full_name","position","latest_team","proj_pts","rep_dyn","vorp_dyn","rec_bid_dyn","tier_dyn"]].head(200).to_csv("cheatsheets/top200.csv",index=False)
for p in ["GK","DEF","MID","FWD"]:
    d=df[df["position"]==p].copy()
    d[["full_name","latest_team","proj_pts","rep_dyn","vorp_dyn","rec_bid_dyn","tier_dyn"]].to_csv(f"cheatsheets/{p}.csv",index=False)
df[["full_name","position","latest_team","rec_bid_dyn"]].to_csv("cheatsheets/board_print.csv",index=False)
