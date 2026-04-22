import re

def fix_redeclare():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. REMOVE DUPLICATE HUD DECLARATIONS
    # We will look for the redundant blocks added in previous turns
    # and replace them with a single clean logic.
    
    # First, let's find the render function start and clean it
    render_start = 'function render() {'
    if render_start in content:
        # Find everything inside render() from start until the next logical block
        # We'll just replace the whole leading part of render() with one clean HUD update
        new_hud_logic = """
            const hud = document.getElementById("hud_display");
            if(hud) {
                const status = state.foxMode ? 'DIVINE: TENKO (天狐)' : 'UNIT: ARCADE_ANGEL';
                hud.innerText = `${status} v0.15.110 (2026-04-18 08:20:00) | PORTABLE`;
            }
        """
        
        # Regex to find all previously injected HUD logic blocks and remove them
        content = re.sub(r'const hud = document\.getElementById\("hud_display"\);.*?PORTABLE`;\s*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'const hud = document\.getElementById\("hud_display"\);.*?07:30:00\);?\s*\}', '', content, flags=re.DOTALL)
        
        # Inject the clean one
        content = content.replace('function render() {', 'function render() {' + new_hud_logic)

    # 2. Bump Version to v0.15.110
    content = re.sub(r'v0\.15\.(101|102|103|104|105|106|107|108|109)', 'v0.15.110', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix_redeclare()
