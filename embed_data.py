"""
embed_data.py — Embed JSON data files inline into PHFL index.html.
Run this whenever any data file in data/ is updated.

Usage:
    python embed_data.py
"""
import json, sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

# Core files (always present)
CORE_FILES = ['standings', 'matchups', 'draft_picks', 'champions',
              'team_yearly', 'head_to_head', 'playoff_games']

# Optional 2025 files (only embed if they exist)
OPTIONAL_FILES = ['weekly_scores_2025', 'player_stats_2025', 'transactions', 'rosters']

DATA_INIT = 'let DATA={standings:[],matchups:[],draft_picks:[],champions:[],team_yearly:[],head_to_head:[],playoff_games:[],weekly_scores_2025:[],player_stats_2025:{},transactions:[],rosters:[]};'

# Old DATA init lines to migrate
OLD_INITS = [
    'let DATA={standings:[],matchups:[],draft_picks:[],champions:[],team_yearly:[],head_to_head:[],playoff_games:[]};',
    'let DATA={standings:[],matchups:[],draft_picks:[],champions:[],team_yearly:[],head_to_head:[],playoff_games:[],weekly_scores_2025:[],player_stats_2025:{},transactions:[]};',
]

BEGIN = '/*BEGIN_INLINE_DATA*/'
END   = '/*END_INLINE_DATA*/'

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. Migrate old DATA init lines (idempotent)
for old in OLD_INITS:
    if old in html:
        html = html.replace(old, DATA_INIT)
        print('Migrated DATA init')

if DATA_INIT not in html:
    print('WARNING: DATA init line not found — check index.html')

# 2. Remove any existing inline data block
html = re.sub(re.escape(BEGIN) + r'.*?' + re.escape(END), '', html, flags=re.DOTALL)

# 3. Build new inline assignments
data_lines = [BEGIN]
files_to_embed = CORE_FILES + [f for f in OPTIONAL_FILES if Path(f'data/{f}.json').exists()]

for name in files_to_embed:
    path = Path(f'data/{name}.json')
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    data_lines.append(f'DATA["{name}"]={data_json};')
    print(f'  Embedded {name}.json ({len(data_json):,} chars)')
data_lines.append(END)

inline_block = '\n'.join(data_lines)

# 4. Insert immediately after the DATA init line
if DATA_INIT in html:
    html = html.replace(DATA_INIT, DATA_INIT + '\n' + inline_block, 1)
    print(f'Inserted {len(files_to_embed)} data blocks')
else:
    print('ERROR: Could not find DATA init anchor')
    sys.exit(1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done!')
