#!/usr/bin/env python3

from pathlib import Path

TRIVIA_FILE = Path('data') / 'game' / 'text_data' / 'trivia-questions.txt'
content = TRIVIA_FILE.read_text(encoding='utf-8', errors='ignore')
lines = content.splitlines()

# Check line 200 (index 199)
line = lines[199]
print(f'Line 200: "{line}"')
print(f'Last character: "{line[-1]}" (ord: {ord(line[-1])})')
print(f'Ends with ?: {line.endswith("?")}')

# Check a few lines around it
for i in range(195, 205):
    if i < len(lines):
        l = lines[i]
        print(f'Line {i+1}: "{l}" - ends with ?: {l.endswith("?")}')
