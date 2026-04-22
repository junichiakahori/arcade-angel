import json

history_path = '/Users/junichiakahori/Documents/Antigravity/arcade-angel/version_history_dev.json'
with open(history_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_version = "v0.15.101"
new_date = "2026-04-18 06:50:00"

data['current_version'] = new_version
data['last_updated'] = new_date
data['history'].insert(0, {
    "version": new_version,
    "date": new_date,
    "notes": "SMILE GENTLENESS (v0.15.101): Reduced happy eye scale (0.88 -> 0.76) and lowered positioning to eliminate facial 'uncanniness' and restore a gentle, modest expression."
})

with open(history_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
