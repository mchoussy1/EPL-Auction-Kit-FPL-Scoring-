# EPL Auction Kit (FPL Scoring)

Build an EPL fantasy **auction board** and printable **draft pack** using official **Fantasy Premier League (FPL) scoring**. No accounts or keys required.

---

## Quick Start

```bash
# 1) Clone and enter the repo
git clone <YOUR_REPO_URL> epl-auction-kit && cd epl-auction-kit

# 2) (Optional) create a virtualenv
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# 3) Install deps
pip install requirements.txt

# 4) Run the pipeline (in this order)
python fpl_pull.py
python espn_scoring.py
python auction_values.py
python make_cheatsheets.py
python make_draft_pack.py
```


## League Settings to Change
```bash
league_size         # teams in your league. Default: 10
pos_slots           # starting roster slots per team. Default: {"GK":2,"DEF":5,"MID":5,"FWD":3}
budget_per_team     # auction budget per team. Default: 200
spend_fraction      # fraction of total league budget allocated to starters in pricing. Default: 0.7
```
## Excel File Lingo

```bash
fpl_id        #The player’s official Fantasy Premier League ID (stable identifier).
full_name     # Player name
position      # FPL Position: GK, DEF, MID, or FWD
latest_team   # Club the player most recently played for in the seasons we pulled.
2023/24       # FPL total points from the 2023/24 Premier League season.
2024/25       # FPL total points from the 2024/25 season (from FPL’s past-season summary; 0 if not available)
min_2023/24   # Minutes played in 2023/24.
min_2024/25   # Minutes played in 2024/25.
proj_pts      # Our projected points for the upcoming season, built from a 70/30 blend of per-90 scoring rates (24/25, 23/24), 
              # shrunk toward the position median and scaled by a blended minutes projection.
rep_dyn       # The replacement level points for that player’s position, based on your league size and roster slots (the projected points of the “last starter” at that position)
              # Higher number means stronger replacement at that position, reduces VORP for players in that position. Vice versa for lower values
vorp_dyn      # Value Over Replacement Player = max(0, proj_pts − rep_dyn).
rec_bid_dyn   # Recommended auction bid ($) derived from VORP, scaled to your league budget and spend fraction.
              # Higher is better(more worth paying for). $0 means they're at/below replacement given league settings
tier_dyn      # Position-relative tier based on projected points quantiles (1 = top tier). 
aav           # Ignore I gotta delete this

Draft tip: sort by rec_bid_dyn when bidding, use tier_dyn to group targets, and glance at vorp_dyn to see the scarcity edge vs. a typical replacement at that position.
```
