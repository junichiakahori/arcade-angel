import re

def fix():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. FORCE ANIMATE TO START IMMEDIATELY
    # Find cam.start() and ensure it doesn't block the loop
    # current: cam.start(); images.foxEars = ...;
    # we want to pull out requestAnimationFrame(animate) and run it separately or move it up
    
    # 2. Make init function more resilient
    content = content.replace(
        'cam.start();',
        'cam.start().then(()=>console.log("Cam Ready")).catch(e=>console.error("Cam Blocked:", e));'
    )
    
    # 3. Ensure animate() is called outside of any await/promise chains in init
    if 'requestAnimationFrame(animate);' not in content.split('init()')[1]:
        # Append it to the very bottom of the script or end of init
        content = content.replace('init();', 'init();\n        requestAnimationFrame(animate);')

    # 4. Bump version to v0.15.106
    content = re.sub(r'v0\.15\.(101|102|103|104|105)', 'v0.15.106', content)
    content = re.sub(r'2026-04-18 07:(00|10|20|30):00', '2026-04-18 07:45:00', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix()
