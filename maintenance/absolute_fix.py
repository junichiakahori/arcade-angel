import re

def absolute_fix():
    with open('dev.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    found_first_hud = False
    
    for line in lines:
        if 'const hud =' in line:
            if not found_first_hud:
                # Keep the first one but update it to latest version
                # Ensure it's the right ID-based one
                new_line = '            const hud = document.getElementById("hud_display");\n'
                new_lines.append(new_line)
                found_first_hud = True
            else:
                # COMMENT OUT or REMOVE any subsequent declarations
                new_lines.append('            // Duplicate hud declaration removed in v112\n')
        else:
            new_lines.append(line)

    # Bump version and fix HUD text in the loop
    content = "".join(new_lines)
    content = re.sub(r'v0\.15\.(101|102|103|104|105|106|107|108|109|110|111)', 'v0.15.112', content)
    content = re.sub(r'2026-04-18 08:(20|30|35):00', '2026-04-18 08:40:00', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    absolute_fix()
