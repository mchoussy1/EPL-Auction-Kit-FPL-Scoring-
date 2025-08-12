<<<<<<< HEAD
# EPL-Auction-Kit-FPL-Scoring-
End-to-end Python scripts to build an EPL fantasy auction board and printable draft pack using the official Fantasy Premier League (FPL) scoring. No accounts or API keys required.
=======
# EPL Auction Kit (FPL Scoring)

End-to-end Python scripts to build an EPL fantasy **auction board** and printable **draft pack** using the official **Fantasy Premier League (FPL) scoring**. No accounts or API keys required.

---

## Quick start

### 1) Clone & set up Python
```bash
git clone <your-repo-url> epl-auction-kit
cd epl-auction-kit
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Edit the constants at the top of auction_values.py
```bash
league_size           # Number of teams in your league. Default: 10
pos_slots             # Starting roster slots per team by position. Changes REP and therefore VORP/bids.
budget_per_team       # Auction budget per team (in dollars). Default: 200
spend_fraction        # Fraction of league budget allocated to starters in the VORP pricing model. 
                      # Default: 0.7 (reserves the rest for bench/streamers and in-room effects)
```

### 3) Generate all datasets and sheets
```bash
python fpl_pull.py            # builds data/fpl_season_totals.csv
python espn_scoring.py        # builds data/fpl_espn_scored.csv (FPL total_points + minutes by season)
python auction_values.py      # builds data/auction_board.csv (projections, VORP, bids)
python make_cheatsheets.py    # writes cheatsheets/top_200_overall.csv + positional sheets
python make_draft_pack.py     # writes cheatsheets/draft_pack.xlsx (multi-tab draft workbook)
```
>>>>>>> 090eed6 (Initial commit: EPL Auction Kit (FPL scoring))
