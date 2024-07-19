import re
import os

def is_bilingual(text):
    return bool(re.search(r'[a-zA-Z]', text)) and bool(re.search(r'[\u0600-\u06FF]', text))

def add_unicode_control_chars(text):
    lines = text.split('\n')
    fixed_lines = []
    for line in lines:
        if is_bilingual(line):

            fixed_line = f'\u202B{line}\u202C'
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)
    return '\n'.join(fixed_lines)

def fix_subtitle(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    

    subtitle_pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
    

    fixed_content = subtitle_pattern.sub(lambda m: f"{m.group(1)}\n{m.group(2)}\n{add_unicode_control_chars(m.group(3))}\n\n", content)
    

    fixed_file_path = file_path.replace('.srt', '.srt')
    with open(fixed_file_path, 'w', encoding='utf-8') as file:
        file.write(fixed_content)
    
    print(f"Fixed subtitle saved as: {fixed_file_path}")

def fix_all_srt_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.srt'):
            file_path = os.path.join(directory, filename)
            fix_subtitle(file_path)


current_directory = os.getcwd()
fix_all_srt_files_in_directory(current_directory)
print('Finish')
os.system("pause")