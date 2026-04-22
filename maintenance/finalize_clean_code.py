import re
import textwrap

def finalize_clean_code():
    with open('dev.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. SPLIT HUGE BASE64 STRINGS
    # We find strings starting with "data:image/png;base64," and ending with "
    def split_string(match):
        full_str = match.group(0) # Includes quotes
        quote_char = full_str[0]
        actual_content = full_str[1:-1]
        
        # Split into 80-char chunks
        chunks = textwrap.wrap(actual_content, 80)
        wrapped = (' ' + quote_char + '\n' + ' ' * 16 + ' + ').join([quote_char + c + quote_char for c in chunks])
        return wrapped

    # Finding base64 strings (approximate but should catch the big ones)
    content = re.sub(r'["\']data:image/png;base64,.*?["\']', split_string, content, flags=re.DOTALL)

    # 2. TYPO FIXES
    content = content.replace('thres0:', 'thresO:') # Seen in screenshot
    content = content.replace('thresU: 0.02', 'thresU: 2') # Correct value is 2
    content = content.replace('thresI: 0.14', 'thresI: 14') # Correct value is 14
    content = content.replace('thresA: 0.27', 'thresA: 30') # Defaults reset to integers
    content = content.replace('thresE: 0.18', 'thresE: 20') 

    # 3. ENSURE NO STRAY ARTIFACTS
    content = content.replace('*L for Agent', '')
    content = content.replace('L for Agent', '')
    
    # 4. FINAL STRUCTURAL SYNC
    # Ensure window.resetState and init() are properly separated and closed
    # We use a safer approach: ensure one closing brace before init() and no extra open (
    content = re.sub(r'\}\s*\(\s*window\.resetState', '} window.resetState', content)
    
    # 5. Bump version to v0.15.119
    content = re.sub(r'v0\.15\.(101|102|103|104|105|106|107|108|109|110|111|112|113|114|115|116|117|118)', 'v0.15.119', content)

    with open('dev.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    finalize_clean_code()
