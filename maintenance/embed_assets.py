import json
import re

def heavy_fix():
    # 1. Load the big assets
    with open('assets.json', 'r', encoding='utf-8') as f:
        assets_data = json.load(f)
    
    embedded_js = "const embeddedAssets = " + json.dumps(assets_data, ensure_ascii=False) + ";"

    # 2. Load dev.html
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. Inject the data before the state object
    content = content.replace('const state = {', embedded_js + '\n        const state = {')

    # 4. Replace the fetch logic in init()
    # old logic (v106): let assets = {}; try { assets = await (await fetch('assets.json?v=' + Date.now())).json(); } catch(e) { console.warn('Local fetch blocked (assets.json). Using embedded assets.'); }
    # new logic: let assets = embeddedAssets;
    
    pattern = r"let assets = \{\}; try \{ assets = await \(await fetch\('assets.json.*? catch\(e\) \{ .*? \}"
    content = re.sub(pattern, "let assets = embeddedAssets;", content)

    # 5. Fix version and timestamp
    content = re.sub(r'v0\.15\.(101|102|103|104|105|106)', 'v0.15.107', content)
    content = re.sub(r'2026-04-18 07:(00|10|20|30|45):00', '2026-04-18 07:55:00', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    heavy_fix()
