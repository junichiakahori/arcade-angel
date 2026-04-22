import re

def purge_mess():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. DELETE ANY STRAY "Agent" (Hallucination/Artifact)
    content = content.replace('\nAgent\n', '\n')
    content = content.replace('Agent', '') # Broadly remove it if it's there

    # 2. UNIFY HUD LOGIC (Surgical Regex to replace the mess)
    # This pattern matches the double block we saw in Turn 24
    pattern = r'function render\(\) \{.*?const stage = document\.getElementById\(\'stage\'\);'
    
    clean_render_start = """function render() {
            const hud = document.getElementById("hud_display");
            if(hud) {
                const status = state.foxMode ? 'DIVINE: TENKO (天狐)' : 'UNIT: ARCADE_ANGEL';
                hud.innerText = `${status} v0.15.111 (2026-04-18 08:35:00) | PORTABLE`;
            }
        
            const stage = document.getElementById('stage');"""
            
    content = re.sub(pattern, clean_render_start, content, flags=re.DOTALL)

    # 3. Bump version
    content = re.sub(r'v0\.15\.(101|102|103|104|105|106|107|108|109|110)', 'v0.15.111', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    purge_mess()
