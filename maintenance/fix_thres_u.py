import re

def fix_thres_u():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update state.thresU in JS
    content = content.replace('thresU: 11', 'thresU: 2')
    
    # 2. Update HTML input for thresU
    # Expected: <input type="range" id="thres-u" min="1" max="50" value="11" step="1">
    content = re.sub(r'id="thres-u"(.*?)value="11"', r'id="thres-u"\1value="2"', content)

    # 3. Bump version to v0.15.113
    content = re.sub(r'v0\.15\.(101|102|103|104|105|106|107|108|109|110|111|112)', 'v0.15.113', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix_thres_u()
