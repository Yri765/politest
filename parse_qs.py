import re
import json

def parse_questions(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by double newlines or more to get chunks, but it's risky if options have paragraphs.
    # Better to iterate line by line.
    
    questions = []
    current_q = None
    
    # Regex to identify a question start: "1. Text"
    q_start_pattern = re.compile(r'^(\d+)\.\s+(.*)')
    
    lines = content.split('\n')
    
    buffer = []
    
    def flush_option(q_obj, text_buffer):
        if not text_buffer:
            return
        text = ' '.join(text_buffer).strip()
        # Remove trailing semicolon or period if it looks like a list item end, 
        # but be careful not to remove needed punctuation.
        # The file format has semicolons at the end of options usually.
        if text.endswith(';') or text.endswith('.'):
            text = text[:-1]
        
        q_obj['options'].append(text)

    # We need a state machine
    # State 0: Looking for Question
    # State 1: Reading Question Text (until empty line? or until options start?)
    # actually the format is:
    # N. Question text
    # <empty line>
    # Option 1
    # <empty line>
    # Option 2 ...
    
    # Let's try to split the whole text by the question pattern matches
    # This might be easier.
    
    # Re-read fully
    text_content = content.replace('\r\n', '\n')
    
    # Split by pattern "\n\d+\. "
    # Note: the first line might not have \n before it.
    
    # Let's clean the text first to standardize newlines
    
    # Find all start indices of questions
    q_matches = list(re.finditer(r'(^|\n)(\d+)\.\s+', text_content))
    
    for i in range(len(q_matches)):
        start_idx = q_matches[i].start()
        # The actual start of the question text is after the number
        # text_content[matches[i].end():]
        
        if i < len(q_matches) - 1:
            end_idx = q_matches[i+1].start()
            block = text_content[start_idx:end_idx].strip()
        else:
            block = text_content[start_idx:].strip()
            
        # Parse the block
        # The block starts with "N. Question Text..."
        # We need to separate Question Text from Options.
        # Usually Question Text is the first paragraph.
        
        parts = re.split(r'\n\s*\n', block)
        # parts[0] is proper question line (contains "N. ...")
        
        # Extract number and text
        header = parts[0].replace('\n', ' ')
        m = re.match(r'^(\d+)\.\s+(.*)', header)
        if not m:
            continue
            
        q_id = int(m.group(1))
        q_text = m.group(2).strip()
        
        options = []
        for p in parts[1:]:
            opt = p.replace('\n', ' ').strip()
            if not opt: continue
            if opt.endswith(';') or opt.endswith('.'):
                opt = opt[:-1]
            options.append(opt)
            
        if options:
            questions.append({
                "id": q_id,
                "text": q_text,
                "options": options,
                "correctAnswer": options[0] # First option is correct
            })

    return questions

try:
    qs = parse_questions('c:/Users/User/Downloads/zip/tests_numbered.md')
    with open('c:/Users/User/Downloads/zip/questions.json', 'w', encoding='utf-8') as f:
        json.dump(qs, f, indent=2, ensure_ascii=False)
    print(f"Successfully wrote {len(qs)} questions to questions.json")
except Exception as e:
    print(f"Error: {e}")
