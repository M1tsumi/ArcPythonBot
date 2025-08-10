#!/usr/bin/env python3

import sys
sys.path.append('.')
from cogs.avatar_play_system import parse_avatar_trivia_questions

questions = parse_avatar_trivia_questions()

print(f'Parsed {len(questions)} questions successfully')
print()

print('First 5 questions with their answer indices:')
for i, q in enumerate(questions[:5]):
    print(f'Q{i+1}: Answer index {q["answer_index"]} - Options: {q["options"]}')

print()
answer_indices = [q['answer_index'] for q in questions]
print(f'Unique answer indices found: {set(answer_indices)}')
print(f'Range: {min(answer_indices)} to {max(answer_indices)}')
