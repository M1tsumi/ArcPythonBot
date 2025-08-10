#!/usr/bin/env python3

# Let's debug the parsing step by step
from pathlib import Path

TRIVIA_FILE = Path("data") / "game" / "text_data" / "trivia-questions.txt"

try:
    content = TRIVIA_FILE.read_text(encoding="utf-8", errors="ignore")
except Exception:
    print("Failed to read file")
    exit(1)

lines = content.splitlines()

# Look for the specific question we know has B answer
for i, line in enumerate(lines):
    if "Fire Nation's elite prison guards" in line:
        print(f"Found question at line {i+1}: {line}")
        print("Next few lines:")
        for j in range(i+1, min(i+6, len(lines))):
            print(f"  {j+1}: {lines[j]}")
        break

# Also check for any B) answers with checkmarks
print("\nAll B) answers with checkmarks:")
for i, line in enumerate(lines):
    if line.strip().startswith("B)") and "✅" in line:
        print(f"Line {i+1}: {line}")
