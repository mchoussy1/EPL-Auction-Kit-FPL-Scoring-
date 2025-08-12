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
