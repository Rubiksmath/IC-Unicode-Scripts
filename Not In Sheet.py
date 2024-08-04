import tkinter as tk
from tkinter import filedialog
import json
import csv
import os

class FileData():
    def __init__(self, json_file, csv_files):
        self.json_file = json_file
        self.csv_files = csv_files
        self.unobtained_characters = []

        with open(self.json_file, 'r', encoding='utf-8') as f:
            self.raw_data = json.load(f)

        self.check_characters()

    def check_characters(self):
        json_uni_chars = set(i for i in self.raw_data['recipes'])

        for csv_file in self.csv_files:
            with open(csv_file, 'r', encoding='utf-8') as f:
                csv_data = list(csv.reader(f))

            for row in csv_data[1:]:  # Skip the header row
                name, unicode_hex, _, char, obtained = row[:5]
                if char in json_uni_chars and obtained.upper() == 'FALSE':
                    self.unobtained_characters.append((name, unicode_hex))

        with open('unobtained_characters.txt', 'w', encoding='utf-8') as f:
            for name, unicode_hex in self.unobtained_characters:
                s = f'{name}: {unicode_hex}\n'
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
            print(f"Unsupported file type: {file_path}")
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
