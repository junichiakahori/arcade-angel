import json

history_path = '/Users/junichiakahori/Documents/Antigravity/arcade-angel/version_history_dev.json'
with open(history_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_version = "v0.15.109"
new_date = "2026-04-18 08:15:00"

data['current_version'] = new_version
data['last_updated'] = new_date
data['history'].insert(0, {
    "version": new_version,
    "date": new_date,
    "notes": "SOURCE INTEGRITY (v0.15.109): Sanitized dev.html by removing duplicate function calls and normalizing the execution flow. Fixed code corruption caused by improper string replacements during asset embedding."
})

with open(history_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
