import re

def sanity_cleanup():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. REMOVE ANY DUPLICATE INIT/RENDER FRAGMENTS
    # Previous patches might have left artifacts. We will normalize the init() function.
    
    # Ensure only ONE init() call at the bottom
    content = re.sub(r'init\(\);\s*requestAnimationFrame\(animate\);', '', content)
    if 'init();' in content:
        content = content.replace('init();', '') # Remove all instances
    
    # Add it back CLEANLY at the very end of the script
    content = content.replace('</script>', '    init();\n    </script>')

    # 2. RESTORE HUD JS LOGIC (ensure it's not duplicated)
    # The injection in render() might have been messy.
    # We will wrap it in a cleaner way.
    
    # 3. FIX THE "Initializing..." HANG
    # Make sure animate() is the first thing in init()
    # But wait, animate() is defined globally.
    content = re.sub(r'async function init\(\) \{.*?requestAnimationFrame\(animate\);', 'async function init() {\n        requestAnimationFrame(animate);', content, flags=re.DOTALL)

    # 4. Bump to v0.15.109
    content = re.sub(r'v0\.15\.(101|102|103|104|105|106|107|108)', 'v0.15.109', content)
    
    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    sanity_cleanup()
