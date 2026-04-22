import json

history_path = '/Users/junichiakahori/Documents/Antigravity/arcade-angel/version_history_dev.json'
with open(history_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_version = "v0.15.112"
new_date = "2026-04-18 08:40:00"

data['current_version'] = new_version
data['last_updated'] = new_date
data['history'].insert(0, {
    "version": new_version,
    "date": new_date,
    "notes": "ABSOLUTE DEDUPLICATION (v0.15.112): Resolved persistent 'hud' redeclaration errors by performing a full-file line scan and stripping all redundant variable definitions. Verified only one 'hud' constant exists in the global/render scope."
})

with open(history_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
