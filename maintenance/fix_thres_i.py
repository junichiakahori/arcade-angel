import re

def fix_thres_i():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update state.thresI in JS (handle both 14.0 and 14 just in case)
    content = content.replace('thresI: 14.0', 'thresI: 14')
    
    # 2. Update HTML input for thresI
    content = re.sub(r'id="thres-i"(.*?)value="14\.0"', r'id="thres-i"\1value="14"', content)

    # 3. Bump version to v0.15.114
    content = re.sub(r'v0\.15\.(101|102|103|104|105|106|107|108|109|110|111|112|113)', 'v0.15.114', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix_thres_i()
