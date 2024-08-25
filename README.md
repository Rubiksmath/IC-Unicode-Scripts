# Welcome
Hi, This is a repository where I am storing some scripts for convenience for the Unicode project in Infinite Craft. I will provide a brief explanation of how to use both scripts in this document.
## Before You Start
These steps must be followed before you can use any of the scripts in this repostiory. Most players will have already completed these or know how to complete them, but I will explain regardless.
1. **Install Python**
   - If you do not already have a recent version of Python installed on your system (tested for 3.11+), you can do so [here](https://www.python.org/downloads/). It is recommended to also set the PATH environment variable so that Python can be accessed throughout your entire file system.
2. **Download script/s**
   - The script/s of your choice can be downloaded directly from this repository, which will always be the latest available version.
3. **Download Save File**
   - To do this, you need to have Infinite Craft Helper installed. If you do not have it installed, you can install it [here](https://github.com/InfiniteCraftCommunity/userscripts/tree/master/userscripts/InfiniteCraftHelper).
   - Once installed, click on the settings icon in the top right and click 'Export Save File'. This will download a JSON file which contains information from your save onto your computer.
## Save_checker
This script looks at the provided savefile and provides information on the number of unicode characters in your save or a particular range, including functionality to filter by FD status.
### Steps to run:
1. **Open an IDE or command line to run the script**
   - To run from command line:
     1. Open directory that contains the script
     2. Highlight folder path in top left (if on Windows)
     3. Delete the file path and type in `cmd`
     4. Press Enter. This should spawn the Command Prompt terminal, with the current file path being the current directory.
     5. Type `python save_checker.py`
     6. Press Enter
   - To run from IDE (instructions are for IDLE, but you can use any IDE capable of running Python):
     1. Right click the script
     2. Select Edit With IDLE
     3. Click Run at the top of the IDLE window.
2. **Select Savefile**
   - A dialog will pop up once you run the script asking you to select a JSON file. Simply click on the file you want to use and click OK. If you pick more than one file, or pick some non-JSON files, it will use the first JSON it finds. If you do not pick any JSON files, it will throw an error.
3. **Specify FD Status**
   - The script will then display the number of characters in your save.
   - Then, it will ask you if you want to only check first discoveries. Type in "y" for Yes or "n" for No depending on whether you want only FD characters to be considered by the script.
4. **Specify Range Start**
   - The script will then ask you to specify the range of characters to check.
   - It will first ask you for the start of the range. Type in the hex code of the first character you want to be considered by the script. For example, if you type "0100" - the script will now only check for characters with hex code 0x0100 or above. The script also provides the option to type in "-1", in which case it will consider all characters in your save, depending of course on the FD status you previously selected.
5. **Specify Range End (if necessary)**
   - The script will then ask for the end of the range you want considered (provided you didn't type in "-1" for the range start). Type in the hex code of the last character you want to be considered by the script. For example, if you type in "0200" - then the script will consider characters with hex codes from the range start to 0x200 inclusive.
6. **Run Again (if you want)**
   - The script then provides the analysis and prints out the characters for you.
   - It then asks for if you want to run it again, for example to check a different range.
   - Type "y" for Yes or "n" for No and depending on what you type it will restart from step 3.
   - Note that checking a different save file is not yet supported. 
## Undoc_chars
This script tells you all the characters you have in your save that aren't in the sheet.
### Steps to run:
1. **Download Database**
   -  Open the database on Google Sheets (most recent version is found [here](https://docs.google.com/spreadsheets/d/1PRtlXvjbHs4ulct6gSbYc6VYrQegU7HZ5SdhThkHuoY/))
   -  Click on Unicode Characters on the bottom
   -  Click File -> Download -> Comma Separated Values (.csv). This will download this portion of the database to your computer as a csv file. Make sure you know where it got saved to, or move it to a convenient location in your PC file directory.
   -  Click on Hangul on the bottom
   -  Repeat download process
   -  Click on CJK Unified Ideographs on the bottom
   -  Repeat download process
   -  You do not need to download all the sheets if you don't want to, if you only want to compare to one subset then you can just download that one and the script will still "work" - it just won't be able to say anything about characters not contained in that section of the database.
2. **Open an IDE or command line to run the script**
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
3. **Select Savefile and Database Files**
   - While holding down Ctrl key, select all the files you want to use. Usually, this will be the save file you just exported with Infinite Craft Helper, and the three CSV files you just downloaded from the Google Sheets database. However, you can select other save files and other CSV files if you wish to compare to older versions of the database or other save files you may have. **IMPORTANT**: You must select at least one JSON file, and at least one CSV file, or else the program cannot run and it will raise an error.
   - The results are then printed to screen in the same place you ran it from (e.g. IDLE shell or command line shell). Additionally, the results are also written to a .txt file called `undocumendted_characters.txt`, which is saved in the same directory you ran the script from. Note that if you ran from command line, it might end up in the same folder as the Python executable file itself, so make sure to check there if you can't find it. In any case, the printed output to the screen is identical to what is saved in the file, so if you can't find the file, you can just use the printed output instead.
## Undoc_chars_auto
### Steps to run:
1. **Install Requests Module**
   - Open a terminal and type in `pip install requests`
   - This should hopefully install the `requests` module to allow you to download sheet automatically, if you have python set in PATH when you first installed it.
2. **Check settings in code**
   - Open the file with an IDE like IDLE or Visual Studio and scroll to the top where the parameter `AUTO_DOWNLOAD` should be visible.
   - Set this to whatver you prefer. `True` or `1` will make it download the database automatically, and `False` or `0` will make it ask you for the database files.
   - Scroll down to `def download_files():`
   - Check the `"filenames"` parameters for the database files - if you want them to be saved as another name, change the `"filenames"` parameters accordingly.
3. **Run Script***
   - From the IDE (or command line if you prefer) - the script should be able to be run like described for the other two scripts.
4. **Select Save File**
   - Once you start the script, a window should pop up asking for the save file. Click on the save file you want to use, and then press Open.
   - You must select a JSON file or else the script will error and exit.
   - That's it! (provided `AUTO_DOWNLOAD` is set to `True` or `1`)
