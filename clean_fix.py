import re

def clean_index():
    path = 'c:/Users/User/Downloads/zip/index.tsx'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We are looking for "]; = ["
    # And then a bunch of objects and "];"
    
    # Let's find the specific garbage string
    pattern = r'\]; = \[\s+\{ id: 1, text: "What is the capital of France\?",.*?\];'
    
    # We need dotall to match across lines
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        print(f"Found garbage from {match.start()} to {match.end()}")
        # We want to replace it with just "];"
        # The match starts with "]; = ["
        # So we keep the first "];"
        
        new_content = content[:match.start()] + "];" + content[match.end():]
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Fixed index.tsx")
    else:
        print("Garbage pattern not found. Maybe manual intervention needed or pattern is slightoff.")
        # Fallback: look for "]; = [" and cut until "const SHUFFLE_COUNT"
        p2 = re.search(r'\]; = \[.*?(?=const SHUFFLE_COUNT)', content, re.DOTALL)
        if p2:
             print(f"Found garbage (fallback) from {p2.start()} to {p2.end()}")
             new_content = content[:p2.start()] + "];\n\n" + content[p2.end():]
             with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
             print("Fixed index.tsx with fallback")
        else:
             print("Could not find garbage to clean.")

clean_index()
