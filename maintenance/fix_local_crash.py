import re

def fix():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. WRAP FETCH CALLS IN TRY-CATCH TO PREVENT SCRIPT CRASH ON file://
    # Find the init function start
    init_func_pattern = r'\(async function init\(\) \{'
    # We want to make the json fetches optional
    # old: const assets = await (await fetch('assets.json?v=' + Date.now())).json();
    # old: v_data = await (await fetch('version_history_dev.json?v=' + Date.now())).json();

    content = content.replace(
        "const assets = await (await fetch('assets.json?v=' + Date.now())).json();",
        "let assets = {}; try { assets = await (await fetch('assets.json?v=' + Date.now())).json(); } catch(e) { console.warn('Local fetch blocked (assets.json). Using embedded assets.'); }"
    )
    content = content.replace(
        "v_data = await (await fetch('version_history_dev.json?v=' + Date.now())).json();",
        "try { v_data = await (await fetch('version_history_dev.json?v=' + Date.now())).json(); } catch(e) { console.warn('Local fetch blocked (version_history).'); }"
    )

    # 2. Add local server helper to the overlay message so it's visible to user
    content = content.replace(
        '<p style="font-size:12px; opacity:0.7">※file:// 起動時はカメラが動きません。HTTPサーバー経由を推奨します。</p>',
        '<p style="font-size:12px; opacity:0.7">※file:// 起動時はカメラが動きません。<br>解決策: このフォルダで <b>python3 -m http.server</b> を実行し localhost:8000 を開いてください。</p>'
    )

    # 3. Update Version and Timestamp to v0.15.104
    content = re.sub(r'v0\.15\.103', 'v0.15.104', content)
    content = re.sub(r'2026-04-18 07:10:00', '2026-04-18 07:20:00', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix()
