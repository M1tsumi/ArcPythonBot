#!/usr/bin/env python3

import sys
sys.path.append('.')

from pathlib import Path

TRIVIA_FILE = Path("data") / "game" / "text_data" / "trivia-questions.txt"

def parse_avatar_trivia_questions_debug():
    """Debug version of the parsing function."""
    if not TRIVIA_FILE.exists():
        return []

    try:
        content = TRIVIA_FILE.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    questions = []
    lines = content.splitlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
            
        # Try to parse question block
        if not line.endswith('?'):
            i += 1
            continue
            
        question_text = line
        options = []
        correct_answer = None
        
        # Check if this is the prison guards question
        is_target = "prison guards" in question_text.lower()
        
        # Also debug a few questions for context
        debug_this = is_target or question_text.startswith("What is the main power source")  or question_text.startswith("What type of bending does Combustion")
        if is_target:
            print(f"\n=== PROCESSING TARGET QUESTION ===")
            print(f"Line {i+1}: {question_text}")
        
        # Look for options in the next few lines
        j = i + 1
        while j < len(lines) and j < i + 5:  # Max 4 options
            option_line = lines[j].strip()
            if is_target:
                print(f"  Checking line {j+1}: '{option_line}'")
            
            if not option_line:
                if is_target:
                    print("    Empty line, breaking")
                break
                
            if option_line.startswith(('A)', 'B)', 'C)', 'D)')):
                option_text = option_line[2:].strip()
                if is_target:
                    print(f"    Found option: '{option_text}'")
                
                if '✅' in option_text:
                    correct_answer = len(options)  # This will be the index of the current option
                    if debug_this:
                        print(f"    This is the correct answer! Index will be: {correct_answer}")
                    option_text = option_text.replace('✅', '').strip()
                options.append(option_text)
            j += 1
        
        if len(options) >= 2 and correct_answer is not None:
            if is_target:
                print(f"  Final options: {options}")
                print(f"  Correct answer index: {correct_answer}")
                print("  QUESTION ADDED TO RESULTS")
            
            questions.append({
                "question": question_text,
                "options": options,
                "answer_index": correct_answer,
                "category": "General",
                "difficulty": "normal",
                "id": len(questions)
            })
        elif debug_this:
            print(f"  QUESTION REJECTED - options: {len(options)}, correct_answer: {correct_answer}")
        
        i = j

    return questions

# Run the debug version
questions = parse_avatar_trivia_questions_debug()
print(f"\n=== FINAL RESULTS ===")
print(f"Total questions parsed: {len(questions)}")

# Find the target question in results
target_found = False
for q in questions:
    if "prison guards" in q["question"].lower():
        print(f"Target question found with answer index: {q['answer_index']}")
        target_found = True
        break

if not target_found:
    print("Target question NOT found in final results!")
