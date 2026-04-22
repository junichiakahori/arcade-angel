import json

history_path = '/Users/junichiakahori/Documents/Antigravity/arcade-angel/version_history_dev.json'
with open(history_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_version = "v0.15.105"
new_date = "2026-04-18 07:30:00"

data['current_version'] = new_version
data['last_updated'] = new_date
data['history'].insert(0, {
    "version": new_version,
    "date": new_date,
    "notes": "HUD & VISIBILITY FIXED (v0.15.105): Corrected a bug where HUD text was displayed as raw code. Moved HUD updates to the render loop. Re-prioritized render initiation to ensure Tenko-chan and Arcade Angel appear even if network fetches fail."
})

with open(history_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
