import json

history_path = '/Users/junichiakahori/Documents/Antigravity/arcade-angel/version_history_dev.json'
with open(history_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_version = "v0.15.108"
new_date = "2026-04-18 08:00:00"

data['current_version'] = new_version
data['last_updated'] = new_date
data['history'].insert(0, {
    "version": new_version,
    "date": new_date,
    "notes": "ZERO-HANG PORTABILITY (v0.15.108): Stripped all network-dependent logic that caused startup hangs. Render loop now prioritizes immediate drawing of embedded assets over all other initialization, ensuring the puppet is visible even in offline/restricted local environments."
})

with open(history_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
