import os,pandas as pd
os.makedirs("cheatsheets",exist_ok=True)
df=pd.read_csv("data/auction_board.csv")
df=df.sort_values(["rec_bid_dyn","proj_pts"],ascending=[False,False]).reset_index(drop=True)
top200=df[["full_name","position","latest_team","proj_pts","rep_dyn","vorp_dyn","rec_bid_dyn","tier_dyn"]].head(200)
top200.to_csv("cheatsheets/top200.csv",index=False)
for p in ["GK","DEF","MID","FWD"]:
    d=df[df["position"]==p].copy()
    d[["full_name","latest_team","proj_pts","rep_dyn","vorp_dyn","rec_bid_dyn","tier_dyn"]].to_csv(f"cheatsheets/{p}.csv",index=False)
board=df[["full_name","position","latest_team","rec_bid_dyn"]].copy()
board.to_csv("cheatsheets/board_print.csv",index=False)
with pd.ExcelWriter("cheatsheets/draft_pack.xlsx",engine="xlsxwriter") as xw:
    df.to_excel(xw,index=False,sheet_name="AuctionBoard")
    top200.to_excel(xw,index=False,sheet_name="Top200")
    for p in ["GK","DEF","MID","FWD"]:
        pd.read_csv(f"cheatsheets/{p}.csv").to_excel(xw,index=False,sheet_name=p)
    board.to_excel(xw,index=False,sheet_name="BoardPrint")
    meta=pd.DataFrame([{"league_size":10,"budget_per_team":200,"spend_fraction":0.7,"slots_GK":2,"slots_DEF":5,"slots_MID":5,"slots_FWD":3}])
    meta.to_excel(xw,index=False,sheet_name="Settings")
