import re

def ultimate_fix():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. CLEAN UP: Ensure 'fetch' based asset loading is GONE
    # Delete the logic for version_history_dev.json fetch which might be hanging
    content = re.sub(r"try \{ v_data = await \(await fetch\('version_history_dev\.json.*? catch\(e\) \{ .*? \}", "v_data = {history:[]};", content)

    # 2. FORCE RENDER LOOP START AT THE VERY TOP OF init()
    # Move requestAnimationFrame(animate) to be the first thing called when the user clicks or script runs
    # Find the init function and inject animate call
    if 'requestAnimationFrame(animate);' not in content:
        content = content.replace('async function init() {', 'async function init() {\n        requestAnimationFrame(animate);')

    # 3. FIX HUD TO REFLECT STATUS
    content = content.replace(
        'hud.innerText = `${status} v0.15.105 (2026-04-18 07:30:00)`;',
        'hud.innerText = `${status} v0.15.108 (2026-04-18 08:00:00) | PORTABLE`;'
    )

    # 4. Bump Global Version
    content = re.sub(r'v0\.15\.(101|102|103|104|105|106|107)', 'v0.15.108', content)
    
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    ultimate_fix()
