import json
import re

def update_index_tsx():
    # Read questions
    with open('c:/Users/User/Downloads/zip/questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    # Format questions as TypeScript
    # JSON dump is valid JS/TS.
    questions_ts = json.dumps(questions, indent=2, ensure_ascii=False)
    
    # Read index.tsx
    ts_path = 'c:/Users/User/Downloads/zip/index.tsx'
    with open(ts_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace QUESTION_POOL
    # Pattern: const QUESTION_POOL: Question[] = \[...\];
    # We use non-greedy match for the content inside brackets, but since brackets can be nested (inside strings etc),
    # we should be careful.
    # However, standard formatting suggests it allows using DOTALL.
    # Let's simple find the start and end indices manually to be safe or use specific pattern.
    
    start_marker = "const QUESTION_POOL: Question[] = ["
    end_marker = "];"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Could not find QUESTION_POOL start")
        return

    # Find the closing element. Since there might be nested arrays in options, we have to be careful.
    # But since the options are strings, there are no nested brackets except inside strings (unlikely in this context to confuse logic if we search carefully).
    # Actually, we can just look for the next "];" that appears at the start of a line or after the block.
    # The existing code ends on line 69 with "];".
    
    # Let's scan from start_idx
    open_brackets = 0
    in_string = False
    quote_char = ''
    escape = False
    
    # A simple parser to find the matching bracket is safer.
    
    # Find the '[' of the array
    array_start = content.find('[', start_idx)
    
    i = array_start
    depth = 0
    found_end = False
    
    while i < len(content):
        char = content[i]
        
        if in_string:
            if char == '\\':
                escape = not escape
            elif char == quote_char and not escape:
                in_string = False
            else:
                escape = False
        else:
            if char == '"' or char == "'":
                in_string = True
                quote_char = char
            elif char == '[':
                depth += 1
            elif char == ']':
                depth -= 1
                if depth == 0:
                    found_end = True
                    break
        i += 1
        
    if not found_end:
        print("Could not find end of QUESTION_POOL array")
        return
        
    end_idx = i + 1 # Include the ']'
    
    # Check if there is a semicolon after
    if content[end_idx] == ';':
        end_idx += 1
        
    new_content = content[:start_idx] + "const QUESTION_POOL: Question[] = " + questions_ts + ";" + content[end_idx:]
    
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Successfully updated QUESTION_POOL in index.tsx")

try:
    update_index_tsx()
except Exception as e:
    print(f"Error: {e}")
