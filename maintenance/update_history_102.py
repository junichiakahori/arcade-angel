import json

history_path = '/Users/junichiakahori/Documents/Antigravity/arcade-angel/version_history_dev.json'
with open(history_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_version = "v0.15.102"
new_date = "2026-04-18 07:00:00"

data['current_version'] = new_version
data['last_updated'] = new_date
data['history'].insert(0, {
    "version": new_version,
    "date": new_date,
    "notes": "LOCAL ACCESSIBILITY (v0.15.102): Added an overlay trigger and immediate render loop launch. This ensures the puppet is visible even when accessed via file:// protocol where camera access is restricted."
})

with open(history_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
