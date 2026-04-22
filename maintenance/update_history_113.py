import json

history_path = '/Users/junichiakahori/Documents/Antigravity/arcade-angel/version_history_dev.json'
with open(history_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_version = "v0.15.113"
new_date = "2026-04-18 08:45:00"

data['current_version'] = new_version
data['last_updated'] = new_date
data['history'].insert(0, {
    "version": new_version,
    "date": new_date,
    "notes": "CALIBRATION TWEAK (v0.15.113): Adjusted THRES U initial value from 11 to 2 to improve default mouth shape mapping for 'U' sounds, making the puppet's speech more expressive out of the box."
})

with open(history_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
