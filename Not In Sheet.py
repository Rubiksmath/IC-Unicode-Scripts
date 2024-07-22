import json
import csv

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

def main():
    json_file = 'infinitecraft (94).json'
    csv_files = ['Unicode Characters (1).csv', 'CJK Unified Ideographs (1).csv', 'Hangul (1).csv']  # List of CSV files
    filedata = FileData(json_file, csv_files)

if __name__ == '__main__':
    main()
