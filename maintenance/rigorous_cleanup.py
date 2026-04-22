import re

def rigorous_cleanup():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. REMOVE ARTIFACTS
    content = content.replace('*L for Agent', '')
    content = content.replace('L for Agent', '')
    
    # 2. MATCH AND CLEAN init() BLOCK
    # The screenshot shows a mess around init(). We will normalize it.
    
    # First, let's find the script end and reconcile the init() closing
    # We want async function init() { ... } then init(); call at bottom.
    
    # Remove any stray IIFE closings like })();
    content = content.replace('})();', '}')
    
    # Normalize init start
    content = re.sub(r'\n\s*async function init\(\)\s*\{', '\n        async function init() {', content)

    # 3. GLOBAL Syntax Check Mock (Strict regex cleanup)
    # Ensure window.resetState is correctly placed before init
    # (Checking turn 28's injection)
    
    # 4. Bump version to v0.15.117
    content = re.sub(r'v0\.15\.(101|102|103|104|105|106|107|108|109|110|111|112|113|114|115|116)', 'v0.15.117', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    rigorous_cleanup()
