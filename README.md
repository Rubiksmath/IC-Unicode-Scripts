# Welcome
Hi, This is a repository where I am storing some scripts for convenience for the Unicode project in Infinite Craft. I will provide a brief explanation of how to use both scripts in this document.
## Undoc_chars
This file tells you all the characters you have in your save that aren't in the sheet.
### Steps to run:
1. Download Save File
   - To do this, you need to have Infinite Craft Helper installed. If you do not have it installed, you can install it [here](https://github.com/InfiniteCraftCommunity/userscripts/tree/master/userscripts/InfiniteCraftHelper).
   - Once installed, click on the settings icon in the top right and click 'Export Save File'. This will download a JSON file which contains information from your save onto your computer.
2. Download Database
   -  Open the database on Google Sheets (most recent version is found [here](https://docs.google.com/spreadsheets/d/1PRtlXvjbHs4ulct6gSbYc6VYrQegU7HZ5SdhThkHuoY/))
   -  Click on Unicode Characters on the bottom
   -  Click File -> Download -> Comma Separated Values (.csv). This will download this portion of the database to your computer as a csv file. Make sure you know where it got saved to, or move it to a convenient location in your PC file directory.
   -  Click on Hangul on the bottom
   -  Repeat download process
   -  Click on CJK Unified Ideographs on the bottom
   -  Repeat download process
3. Install Python
   - If you do not already have a recent version of Python installed on your system (tested for 3.11+), you can do so [here](https://www.python.org/downloads/). It is recommended to also set the PATH environment variable so that Python can be accessed throughout your entire file system.
4. Download script
   - The script can be downloaded directly from this repository.
5. Open an IDE or command line to run the script
   - To run from command line:
     1. Open directory that contains the script
     2. Highlight folder path in top left (if on Windows)
     3. Delete the file path and type in `cmd`
     4. Press Enter. This should spawn the Command Prompt terminal, with the current file path being the current directory.
     5. Type `python undoc_chars.py`
     6. Press Enter
   - To run from IDE (instructions are for IDLE, but you can use any IDE capable of running Python):
     1. Right click the script
     2. Select Edit With IDLE
     3. Click Run at the top of the IDLE window.
6. Once script starts, a dialog asking for you to select files should pop up.
   - While holding down Ctrl key, select all the files you want to use. Usually, this will be the save file you just exported with Infinite Craft Helper, and the three CSV files you just downloaded from the Google Sheets database. However, you can select other save files and other CSV files if you wish to compare to older versions of the database or other save files you may have. **IMPORTANT**: You must select at least one JSON file, and at least one CSV file, or else the program cannot run and it will raise an error.
   - The results are then printed to screen in the same place you ran it from (e.g. IDLE shell or command line shell). Additionally, the results are also written to a .txt file called `undocumendted_characters.txt`, which is saved in the same directory you ran the script from. Note that if you ran from command line, it might end up in the same folder as the Python executable file itself, so make sure to check there if you can't find it. In any case, the printed output to the screen is identical to what is saved in the file, so if you can't find the file, you can just use the printed output instead.
