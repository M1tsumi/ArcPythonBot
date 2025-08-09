#!/usr/bin/env python3
"""
Debug script for trivia questions parsing on Termux
"""

import sys
from pathlib import Path

def check_trivia_file():
    """Check trivia file existence and content."""
    print("=== Trivia File Debug ===")
    
    # Check file paths
    trivia_file = Path("data") / "game" / "text_data" / "trivia-questions.txt"
    print(f"Trivia file path: {trivia_file}")
    print(f"Absolute path: {trivia_file.absolute()}")
    print(f"File exists: {trivia_file.exists()}")
    
    if trivia_file.exists():
        try:
            # Check file size
            file_size = trivia_file.stat().st_size
            print(f"File size: {file_size} bytes")
            
            # Try to read first few lines
            with open(trivia_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]
                print(f"Total lines: {len(f.readlines()) + len(lines)}")
                print("First 10 lines:")
                for i, line in enumerate(lines, 1):
                    print(f"  {i}: {line.strip()[:50]}...")
                    
        except Exception as e:
            print(f"Error reading file: {e}")
    else:
        # Check if directory exists
        data_dir = Path("data")
        game_dir = data_dir / "game"
        text_dir = game_dir / "text_data"
        
        print(f"data/ exists: {data_dir.exists()}")
        print(f"data/game/ exists: {game_dir.exists()}")
        print(f"data/game/text_data/ exists: {text_dir.exists()}")
        
        if text_dir.exists():
            print("Files in text_data/:")
            for file in text_dir.iterdir():
                print(f"  {file.name}")

def test_trivia_parsing():
    """Test the trivia parsing function."""
    print("\n=== Testing Trivia Parsing ===")
    
    try:
        # Import the parsing function
        sys.path.append('.')
        from cogs.avatar_play_system import parse_avatar_trivia_questions
        
        questions = parse_avatar_trivia_questions()
        print(f"Parsed questions: {len(questions)}")
        
        if questions:
            print("First question:")
            q = questions[0]
            print(f"  Question: {q.get('question', 'N/A')}")
            print(f"  Options: {q.get('options', [])}")
            print(f"  Answer index: {q.get('answer_index', 'N/A')}")
            print(f"  Category: {q.get('category', 'N/A')}")
        else:
            print("No questions parsed!")
            
    except Exception as e:
        print(f"Error parsing trivia: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {Path.cwd()}")
    print()
    
    check_trivia_file()
    test_trivia_parsing()
