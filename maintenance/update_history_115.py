import json

history_path = '/Users/junichiakahori/Documents/Antigravity/arcade-angel/version_history_dev.json'
with open(history_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_version = "v0.15.115"
new_date = "2026-04-18 09:00:00"

data['current_version'] = new_version
data['last_updated'] = new_date
data['history'].insert(0, {
    "version": new_version,
    "date": new_date,
    "notes": "CORE FIX (v0.15.115): Restored 'RESET DEFAULTS' button functionality. Added a complete state-to-UI synchronization loop that updates all 16 sliders immediately when defaults are restored, ensuring internal logic and visual controls are always in sync."
})

with open(history_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
