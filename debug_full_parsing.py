#!/usr/bin/env python3

# Let's trace through the parsing algorithm for that specific question
from pathlib import Path

TRIVIA_FILE = Path("data") / "game" / "text_data" / "trivia-questions.txt"

try:
    content = TRIVIA_FILE.read_text(encoding="utf-8", errors="ignore")
except Exception:
    print("Failed to read file")
    exit(1)

lines = content.splitlines()

# Find the question about prison guards
target_question_line = None
for i, line in enumerate(lines):
    if "prison guards" in line:
        target_question_line = i
        break

if target_question_line is None:
    print("Question not found")
    exit(1)

print(f"Processing question at line {target_question_line + 1}")
print(f"Question: {lines[target_question_line]}")

# Simulate the parsing logic
question_text = lines[target_question_line].strip()
options = []
correct_answer = None

# Look for options in the next few lines  
j = target_question_line + 1
while j < len(lines) and j < target_question_line + 5:  # Max 4 options
    option_line = lines[j].strip()
    print(f"  Checking line {j+1}: '{option_line}'")
    
    if not option_line:
        print("    Empty line, breaking")
        break
        
    if option_line.startswith(('A)', 'B)', 'C)', 'D)')):
        option_text = option_line[2:].strip()
        print(f"    Found option: '{option_text}'")
        if '✅' in option_text:
            correct_answer = len(options)
            print(f"    This is the correct answer! Index will be: {correct_answer}")
            option_text = option_text.replace('✅', '').strip()
        options.append(option_text)
    j += 1

print(f"\nFinal result:")
print(f"Question: {question_text}")
print(f"Options: {options}")
print(f"Correct answer index: {correct_answer}")
