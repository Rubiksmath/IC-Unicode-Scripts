import json
import csv
import glob

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
                f.write(f'{name}: {unicode_hex}\n')


def find_files():
    files = []
    json_files = glob.glob('*.json')
    if not json_files:
        raise FileNotFoundError("No JSON file found in the current directory.")
    
    print(f"JSON file detected: \"{json_files[0]}\", this will be used as the savefile.\n")
    
    csv_files = glob.glob('*.csv')
    if not csv_files:
        raise FileNotFoundError("No CSV file found in the current directory.")

    for file in csv_files:
        print(f"CSV file detected: \"{file}\", this will be used as part of the database to compare against.\n")
        
    return json_files[0], csv_files  # Return the first JSON file found

def main():
    json_file, csv_files = find_files()
    filedata = FileData(json_file, csv_files)

if __name__ == '__main__':
    main()
