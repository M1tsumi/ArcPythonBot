#!/usr/bin/env python3

import sys
sys.path.append('.')
from cogs.avatar_play_system import parse_avatar_trivia_questions

questions = parse_avatar_trivia_questions()

# Find questions with different answer indices
for i, q in enumerate(questions):
    if q["answer_index"] != 0:
        print(f'Q{i+1}: Answer index {q["answer_index"]} - Question: {q["question"]}')
        print(f'Options: {q["options"]}')
        print()

print(f'Total questions with non-zero answer index: {len([q for q in questions if q["answer_index"] != 0])}')
