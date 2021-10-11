# playlist_app
## Author: Tarek El-Hajjaoui
### Starting template provided by Professor Rao Ali

## Description of Program
- A Python program that can query and modify a songs table of a sqlite3 database. **The program contains all of the bonus features**:
  - Bonus 1: Pre-processing methods take into account invalid IDs before inserting new songs.
  - Bonus 2: Option 7 - user can bulk update records based on album, artist, or genre name. 
  - Bonus 3: Option 6 -  remove all records.
from the table that have at least 1 NULL value
  - Bonus 4: Option 8 - Threshold and CSV output file functionality.

## Instructions to run the program:
- Run the program with this command: python3 main.py
- Look at the data.csv results

## Source Files:
- app.py
- db_operations.py
- helper.py
- songs_update.csv (example of how an update file is formatted)
- songs.csv (original file used to populate DB upon start if not already)
- README.md

## Sources referred to:
- sqlite3 pip package: https://docs.python.org/3/library/sqlite3.html
- Python3 open/IO: https://docs.python.org/3/library/functions.html#open
- Python open: https://www.w3schools.com/python/python_file_open.asp