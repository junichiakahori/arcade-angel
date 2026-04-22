import re

def fix():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. FIX HUD TEXT (It was raw template literal in HTML)
    # old: <div class="hud">${state.foxMode ? 'DIVINE: TENKO (天狐)' : 'UNIT: ARCADE_ANGEL' } v0.15.103 (2026-04-18 07:10:00)</div>
    # Replace with a span so JS can update it
    content = re.sub(r'<div class="hud">.*?</div>', '<div class="hud" id="hud_display">Initializing...</div>', content)

    # 2. UPDATE HUD IN RENDER LOOP
    # We need to find the render function and add hud update
    if 'document.getElementById("hud_display").innerText =' not in content:
        render_injection = """
            const hud = document.getElementById("hud_display");
            if(hud) {
                const status = state.foxMode ? 'DIVINE: TENKO (天狐)' : 'UNIT: ARCADE_ANGEL';
                hud.innerText = `${status} v0.15.105 (2026-04-18 07:30:00)`;
            }
        """
        # Inject at the start of render()
        content = content.replace('function render() {', 'function render() {' + render_injection)

    # 3. ENSURE ANIMATION STARTS EVEN IF FACE MESH FAILS
    # Put requestAnimationFrame(animate) at the very end of init OR ensure it's called
    # Current code has: cam.start(); ... requestAnimationFrame(animate); 
    # But if something before it fails, it never hits it.
    
    # 4. Fix Version and Timestamp to v0.15.105
    content = re.sub(r'v0\.15\.(101|102|103|104)', 'v0.15.105', content)
    content = re.sub(r'2026-04-18 07:(00|10|20):00', '2026-04-18 07:30:00', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix()
