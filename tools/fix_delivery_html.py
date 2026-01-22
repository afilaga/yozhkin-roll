import re
import os

HTML_FILE = 'PRODUCTION/pages/delivery.html'

def fix_newlines():
    if not os.path.exists(HTML_FILE):
        print(f"File not found: {HTML_FILE}")
        return

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find multiline description strings in the JSON object
    # Matches: "description": "Line1 [newline] [whitespace] Line2"
    pattern = r'"description":\s*"(.*?)\n\s*(.*?)"'
    
    # Replacement function to join with \n escape sequences
    def replace_func(match):
        line1 = match.group(1)
        line2 = match.group(2)
        print(f"Fixing: {line1} [...] {line2}")
        return f'"description": "{line1}\\n{line2}"'

    new_content = re.sub(pattern, replace_func, content)

    if new_content != content:
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Fixed broken multiline strings.")
    else:
        print("ℹ️ No broken strings found.")

if __name__ == "__main__":
    fix_newlines()
