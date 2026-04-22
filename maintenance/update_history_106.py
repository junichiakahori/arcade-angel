import json

history_path = '/Users/junichiakahori/Documents/Antigravity/arcade-angel/version_history_dev.json'
with open(history_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_version = "v0.15.106"
new_date = "2026-04-18 07:45:00"

data['current_version'] = new_version
data['last_updated'] = new_date
data['history'].insert(0, {
    "version": new_version,
    "date": new_date,
    "notes": "LOOP RESILIENCE (v0.15.106): Decoupled the animation/render loop from the camera initialization. This fixes the issue where the application would hang at 'Initializing...' if the browser blocked or delayed camera access."
})

with open(history_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
