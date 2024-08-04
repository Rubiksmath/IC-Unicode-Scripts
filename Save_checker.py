import json
import tkinter as tk
from tkinter import filedialog
import os

class FileData():
    
    def __init__(self, file):
        
        self.charlistrecipes = {}
        self.charlistelements = {}
        self.top = 0
        self.file = file
        self.total_unicodes = 0
        
        with open(self.file, 'r', encoding = 'utf-8') as f:
            self.raw_data = json.load(f)

        for name in self.raw_data['recipes']:
            if len(name) == 1:
                self.total_unicodes += 1
                self.charlistrecipes[ord(name)] = name
                if ord(name) > self.top:
                    self.top = ord(name)

        for element in self.raw_data['elements']:
            name = element['text']
            discovered = element['discovered']
            if len(name) == 1:
                self.charlistelements[ord(name)] = name, discovered

        self.sortedcharlist = sorted(list(self.charlistrecipes.items()), key = lambda x: x[0])
        print(f"You have {self.total_unicodes} unicode characters!\n")




    def perform_search(self, nstart, nend, onlydiscovered):

        ctr2 = 0    
        for index in range(nstart, nend):
            
            if onlydiscovered:
                info = self.charlistelements.get(index)
                if info:
                    if info[1]:
                        ctr2 += 1
                        print(f'U+{index:04x} -> {chr(index)}')
                
            elif index in self.charlistrecipes:

                ctr2 += 1
                print(f'U+{index:04x} -> {chr(index)}')

        return ctr2
        
                
    def search(self, start, end, onlydiscovered = False):
     
        discoverstring = ["", " (counting first discoveries only)"][onlydiscovered]
    
        if start == -1:
            nstart = 0
            nend = self.top + 1
            ctr2 = self.perform_search(nstart, nend, onlydiscovered)
            print(f"Total: {ctr2}{discoverstring}")
            
        else:
            nstart = max(start, 0)
            nend = min(self.top + 1, end + 1)
            ctr2 = self.perform_search(nstart, nend, onlydiscovered)
            print(f'{ctr2} unicode characters found in your save between U+{nstart:04x} and U+{nend - 1:04x}{discoverstring}')


def select_file(filetypes):
    """Open a file dialog to select multiple files and return a list of file paths."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_paths = filedialog.askopenfilenames(filetypes=filetypes)
    return file_paths


def find_files():
    file_paths = select_file([("Json File", "*.json")])
    json_filename = ''
    if not file_paths:
        print("No files selected.")
        return

    # Process each selected file
    for file_path in file_paths:
        _, ext = os.path.splitext(file_path)
        if ext.lower() == '.json':
            json_filename = file_path
            print(f"Selecting JSON file: {file_path}\n")
            break

        else:
            print(f"Ignoring non-JSON file: {file_path}\n")
    if not json_filename:
        raise FileNotFoundError("No JSON selected.")

    return json_filename

def ask_for_input():
    
    while 1:
        onlydiscovered = input("Only list first discoveries? y/n: ").upper() == 'Y'
        try:
            
            start = int(input("Start of range (-1 means all): "), base = 16)
            if start == -1:
                
                end = None
                break
            
            end = int(input("End of range: "), base=16)
            break
        except:
            print("Please input a valid base 16 codepoint")
            
    return start, end, onlydiscovered


def main():
    # Change this to yours, make sure it is in same directory you are running
    # this from or just point to it directly via C:/full/path/here DO NOT USE BACKSLASH PLEASE
    file = find_files()
    
    filedata = FileData(file)
    
    
    start, end, onlydiscovered = ask_for_input()
    filedata.search(start, end, onlydiscovered)

    while input("Run again? y/n ").upper() == 'Y':
        start, end, onlydiscovered = ask_for_input()
        filedata.search(start, end, onlydiscovered)
        
if __name__ == '__main__':
    main()
        
    
