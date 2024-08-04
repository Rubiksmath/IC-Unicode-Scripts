# Welcome
Hi, This is a repository where I am storing some scripts for convenience for the Unicode project in Infinite Craft. I will provide a brief explanation of how to use both scripts in this document.
## Undoc_chars
This file tells you all the characters you have in your save that aren't in the sheet.
To use this file, simply run it either from command line (with `python undoc_chars.py`) or with an IDE like IDLE or Visual Studio by clicking run. A window should then pop up asking you which files you want to use for the search. 
### IMPORTANT
In this dialog, hold down the Ctrl key while selecting your files. This will allow you to select any number of files at once. You will need to use this technique to select all the CSV files which contain the database you are comparing against *and* also your save file JSON. If you do not select at least one CSV and at least one JSON, it will raise an error.
Once the files are selected, click OK and the script should do the rest for you. You should see lines printed to the console of wherever you ran it from (cmd, idle, etc) which corresponds to the characters not in the database you chose but present in the JSON you chose. The script also outputs a file, `unobtained_characters.txt`, which will be saved in the same directory it was ran from.
