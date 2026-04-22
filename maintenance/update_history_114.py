import json

history_path = '/Users/junichiakahori/Documents/Antigravity/arcade-angel/version_history_dev.json'
with open(history_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_version = "v0.15.114"
new_date = "2026-04-18 08:50:00"

data['current_version'] = new_version
data['last_updated'] = new_date
data['history'].insert(0, {
    "version": new_version,
    "date": new_date,
    "notes": "FORMATTING FIX (v0.15.114): Standardized THRES I's initial value to 14 (integer) instead of 14.0 (float) for UI consistency and cleaner data handling."
})

with open(history_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
