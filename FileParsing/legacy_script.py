import sys
from guesslang import Guess

def detect_language_guesslang(file_path=None, text=None):
    guess = Guess()
    if file_path:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        # print(content)
        return guess.language_name(content)
    
    elif text:
        return guess.language_name(text)
    else:
        return "Unknown"
if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        lang = detect_language_guesslang(file_path=file_path)
        print(f"{lang}")
    else:
        input_text = sys.stdin.read()
        lang = detect_language_guesslang(text=input_text)
        print(f"{lang}") 