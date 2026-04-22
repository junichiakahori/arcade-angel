import json

history_path = '/Users/junichiakahori/Documents/Antigravity/arcade-angel/version_history_dev.json'
with open(history_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_version = "v0.15.116"
new_date = "2026-04-18 09:15:00"

data['current_version'] = new_version
data['last_updated'] = new_date
data['history'].insert(0, {
    "version": new_version,
    "date": new_date,
    "notes": "STABILITY PATCH (v0.15.116): Fixed 'resetState is not defined' ReferenceError by exposing the reset function to the global window object. Resolved 'addEventListener of null' TypeError by adding defensive existence checks for all UI control elements, ensuring the script doesn't crash if certain DOM nodes are missing."
})

with open(history_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
