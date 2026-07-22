import os
import shutil
from datetime import datetime

TARGET_FOLDER = 'test_messy'
LOG_FILE = 'organizer_log.txt'

CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Documents': ['.pdf', '.txt', '.docx'],
    'Data': ['.csv', '.xlsx', '.json'],
    'Code': ['.py', '.html', '.sql'],
    'Audio': ['.mp3', '.wav']
}

def find_category(filename):
    for category, extensions in CATEGORIES.items():
        for ext in extensions:
            if filename.lower().endswith(ext):
                return category
    return 'Other'

def get_plan():
    plan = []
    for filename in os.listdir(TARGET_FOLDER):
        full_path = os.path.join(TARGET_FOLDER, filename)
        if os.path.isfile(full_path):
            plan.append((filename, find_category(filename)))
    return plan

def organize():
    plan = get_plan()

    if len(plan) == 0:
        print('\nNothing to organize!')
        return

    print(f'\nPreview — {len(plan)} files to organize:\n')
    for filename, category in plan:
        print(f'  {filename}  →  {category}/')

    answer = input('\nMove these files? (yes/no): ')
    if answer.lower() != 'yes':
        print('Cancelled — nothing was moved.')
        return

    log_lines = []
    for filename, category in plan:
        destination_folder = os.path.join(TARGET_FOLDER, category)
        os.makedirs(destination_folder, exist_ok=True)

        old_path = os.path.join(TARGET_FOLDER, filename)
        new_path = os.path.join(destination_folder, filename)

        shutil.move(old_path, new_path)
        log_lines.append(f'{filename}|{category}')

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    log = open(LOG_FILE, 'a')
    log.write(f'--- Run at {timestamp} ---\n')
    for line in log_lines:
        log.write(line + '\n')
    log.close()

    print(f'\nDone! Moved {len(plan)} files. Log saved to {LOG_FILE}')

def undo():
    if not os.path.exists(LOG_FILE):
        print('\nNo log file found — nothing to undo.')
        return

    log = open(LOG_FILE, 'r')
    lines = log.readlines()
    log.close()

    # Find the last run in the log
    last_run = []
    for line in reversed(lines):
        line = line.strip()
        if line.startswith('---'):
            break
        if '|' in line:
            last_run.append(line)

    if len(last_run) == 0:
        print('\nNothing to undo.')
        return

    print(f'\nUndoing {len(last_run)} moves...')

    restored = 0
    for line in last_run:
        filename, category = line.split('|')
        current_path = os.path.join(TARGET_FOLDER, category, filename)
        original_path = os.path.join(TARGET_FOLDER, filename)

        if os.path.exists(current_path):
            shutil.move(current_path, original_path)
            print(f'  {filename}  ←  {category}/')
            restored = restored + 1

    print(f'\nRestored {restored} files to {TARGET_FOLDER}/')

# Menu
while True:
    print('\n=== FILE ORGANIZER 2.0 ===')
    print('1 - Organize files')
    print('2 - Undo last run')
    print('3 - Quit')
    choice = input('Choose: ')

    if choice == '1':
        organize()
    elif choice == '2':
        undo()
    elif choice == '3':
        break