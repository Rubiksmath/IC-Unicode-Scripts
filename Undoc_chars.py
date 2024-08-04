import tkinter as tk
from tkinter import filedialog
import json
import csv
import os

class FileData():
    def __init__(self, json_file, csv_files):
        self.json_file = json_file
        self.csv_files = csv_files
        self.character_statuses = {}
        self.undocumented_characters = []

        with open(self.json_file, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)

        self.check_characters()

    def check_characters(self):
        json_uni_chars = {i for i in self.raw_data['recipes']} | {i['text'] for i in self.raw_data['elements']}

        for csv_file in self.csv_files:
            with open(csv_file, 'r', encoding='utf-8') as f:
                csv_data = list(csv.reader(f))

            for row in csv_data[1:]:  # Skip the header row
                name, unicode_hex, _, char, obtained = row[:5]
                status = self.character_statuses.get(char, 0)
                
                # If not yet added to statuses, add it
                if not status:
                    self.character_statuses[char] = {'name': name, 'hex': unicode_hex, 'obtained': obtained.upper()}
                    
                # Override FALSE if its been found in a later version
                elif status['obtained'] == 'FALSE' and obtained.upper() == 'TRUE':
                    self.character_statuses[char]['obtained'] = 'TRUE'

                
        for char, status in self.character_statuses.items():
            if status['obtained'] == 'FALSE' and char in json_uni_chars:
                self.undocumented_characters.append((status['name'], status['hex'], char))

        with open('undocumented_characters.txt', 'w', encoding='utf-8') as f:
            for name, unicode_hex, char in self.undocumented_characters:
                s = f'{name}\t{unicode_hex}\t{char}\n'
                f.write(s)
                print(end=s)

def select_files(filetypes):
    """Open a file dialog to select multiple files and return a list of file paths."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_paths = filedialog.askopenfilenames(filetypes=filetypes)
    return file_paths


def find_files():
    file_paths = select_files([("All files", "*.*")])
    json_filename = ''
    csv_filenames = []
    if not file_paths:
        print("No files selected.")
        return

    # Process each selected file
    for file_path in file_paths:
        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.json':
            json_filename = file_path
        elif ext.lower() == '.csv':
            csv_filenames.append(file_path)
        else:
            print(f"Ignoring non-JSON and non-CSV file: {file_path}")
    if not json_filename:
        raise FileNotFoundError("No JSON selected.")
    if not csv_filenames:
        raise FileNotFoundError("No CSV selected.")

    return json_filename, csv_filenames

def main():
    json_filename, csv_filenames = find_files()
    filedata = FileData(json_filename, csv_filenames)

if __name__ == '__main__':
    main()
