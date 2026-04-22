def check_syntax(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract script content
    try:
        start_idx = content.find('<script>') + len('<script>')
        end_idx = content.rfind('</script>')
        js_code = content[start_idx:end_idx]
    except Exception:
        return "Error: Could not find script tags."

    stack = []
    pairs = {'{': '}', '(': ')', '[': ']'}
    quotes = {'"': '"', "'": "'", '`': '`'}
    
    in_quote = None
    line_num = 1
    char_num = 0
    
    for i, char in enumerate(js_code):
        if char == '\n':
            line_num += 1
            char_num = 0
            continue
        char_num += 1
        
        if in_quote:
            if char == in_quote and (i == 0 or js_code[i-1] != '\\'):
                in_quote = None
            continue
        
        if char in quotes:
            in_quote = char
            continue
            
        if char in pairs:
            stack.append((char, line_num, char_num, js_code[max(0, i-20):i+20].replace('\n', ' ')))
        elif char in pairs.values():
            if not stack:
                context = js_code[max(0, i-20):i+20].replace('\n', ' ')
                return f"Syntax Error: Unmatched '{char}' at line {line_num}, col {char_num}. Context: ...{context}..."
            top_char, top_line, top_col, top_context = stack.pop()
            if pairs[top_char] != char:
                context = js_code[max(0, i-20):i+20].replace('\n', ' ')
                return f"Syntax Error: Mismatched '{char}' at line {line_num} (expected closing for '{top_char}' from line {top_line}). Context: ...{context}..."

    if stack:
        top_char, top_line, top_col, top_context = stack.pop()
        return f"Syntax Error: Unclosed '{top_char}' from line {top_line}, col {top_col}. Context: ...{top_context}..."
    
    if in_quote:
        return f"Syntax Error: Unclosed quote {in_quote}"

    return "SYNTAX OK"

if __name__ == '__main__':
    result = check_syntax('dev.html')
    print(result)
    if result != "SYNTAX OK":
        exit(1)
