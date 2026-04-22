import json

history_path = '/Users/junichiakahori/Documents/Antigravity/arcade-angel/version_history_dev.json'
with open(history_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_version = "v0.15.107"
new_date = "2026-04-18 07:55:00"

data['current_version'] = new_version
data['last_updated'] = new_date
data['history'].insert(0, {
    "version": new_version,
    "date": new_date,
    "notes": "FULL PORTABILITY (v0.15.107): Embedded all Base64 assets (body, hair, costumes) directly into dev.html. No external asset fetch required. This completely fixes the 'white/invisible puppet' bug on local file:// access."
})

with open(history_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
