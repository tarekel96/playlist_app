# module defines an application to curate a playlist
# with a sqlite3 db as a backend for data storage


from datetime import date
from helper import helper
from db_operations import db_operations

data = helper.data_cleaner("songs.csv")

DB_PATH = "/Users/Tarek/Documents/CPSC_Courses/CPSC_408/chinook.db"
# modify to your chinook db connection
db_ops = db_operations(DB_PATH)

# function checks if the table is empty or not
def is_empty():
    query = '''
    SELECT COUNT(*)
    FROM songs;
    '''
    result = db_ops.single_record(query)
    return result == 0

# function inserts data into table if it is empty
def pre_process():
    print("Would you like to upload the new songs into the songs table?\n1 Continue without updating songs\n2 Upload songs")
    pre_process_res = helper.get_choice([1,2])
    # ****** New Song Data Update ******
    if pre_process_res == 2:
        try:
            pre_process_new_songs()
        except Exception as e:
            print(f"Error: Cannot add new songs.\n{e}")

    if is_empty():
        attribute_count = len(data[0])
        # [:-1] --> Want every element, except the last one which is a comma
        placeholders = ("?,"*attribute_count)[:-1]
        query = "INSERT INTO songs VALUES("+placeholders+")"
        db_ops.bulk_insert(query,data)

def pre_process_new_songs():    
    file_path = helper.get_file_path()
    insert_new_songs(file_path)
    
def insert_new_songs(file_path = './songs.csv'):
    new_data = helper.data_cleaner(file_path)
    STARTING_AMT = len(new_data)
    # BONUS 1
    # Before inserting each new song, the application shouldcheck if the song with that ID already exists or not. 
    # If it does, then you don’t need to insert that song in the table. 
    query = '''
    SELECT songID
    FROM songs;
    '''
    # Get list of song IDs
    SONG_IDs = db_ops.name_placeholder_query(query=query, dictionary={})
    # Get list of new song IDs 
    new_song_ids = [i[0] for i in new_data]
    # Check if each new song ID is valid and remove if not.
    for new_id in new_song_ids:
        if new_id in SONG_IDs:
            new_data = [record for record in new_data if record[0] != new_id]
    # If there are no new songs left after ID checks, then let user know
    if len(new_data) == 0:
        print("Results: All of the new records have invalid IDs. No new songs were added.")
        return
    # Inform the user of how many songs were added and how many were not
    else:
        print(f"Results: {len(new_data)} song(s) were added and {STARTING_AMT - len(new_data)} song(s) were rejected because of invalid IDs.")
    
    # Insert New Records
    attribute_count = len(new_data[0])
    placeholders = ("?,"*attribute_count)[:-1]
    query = "INSERT INTO songs VALUES("+placeholders+")"
    db_ops.bulk_insert(query, new_data)

# Option 4. Update Song by Name
def update_song_by_name():
    song_name = get_valid_song_name()
    results_list = get_song_record(song_name=song_name)
    query = '''
        SELECT *
        FROM songs
        WHERE Name=:song_name;
        '''
    dictionary = {"song_name": song_name}
    names = db_ops.get_record_col_names(query, dictionary)
    SONG_ID = results_list[0]
    attr_list = ["Name", "Artist", "Album", "releaseDate", "Explicit" ]
    data_types = [str, str, str, date, bool]
    for index, name in enumerate(names):
        if name not in attr_list:
            names.remove(name)
            results_list.pop(index)
    print("Pick a choice of which attriibute to update: ")
    helper.pretty_print_attr(attr_list=attr_list, results_list=results_list)
    res = helper.get_choice([i for i in range(len(attr_list))])
    res_col_name = names[res]
    res_attr_value = results_list[res]
    res_data_type = data_types[res]
    update_value = helper.get_update_value(msg=f"Enter the new value for {res_col_name} : ", \
        original_value=res_attr_value, data_type=res_data_type)
    update_song(SONG_ID, res_col_name, update_value)

# Option 5. Delete Song by Name
def delete_song_by_name():
    song_name = get_valid_song_name()
    results_list = get_song_record(song_name=song_name)
    SONG_ID = results_list[0]
    print(f"Deleting {song_name}...")
    n_delete = delete_song(SONG_ID)
    if n_delete == 1:
         print(f"Successfully deleted {song_name}")
    elif n_delete == -1:
        print(f"Error: Did not delete {song_name}")  
    

def start_screen():
    print("Welcome to your playlist!")


# show user options
def options():
    print("Select from the following menu options:\n1 Find songs by artist\n" \
    "2 Find songs by genre\n3 Find songs by feature\n4 Update song by name\n" \
    "5 Delete song by name\n6 Remove all records that contain an empty attribute.\n"\
    "7 Bulk delete records.\n0 Exit")
    return helper.get_choice([i for i in range(0, 8)])

# option 1, search table to show songs by artist
def search_by_artist():
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    print("Artists in playlist:")
    artists = db_ops.single_attribute(query)

    # show artists in table, also create dictionary for choices
    choices = {}
    for i in range(len(artists)):
        print(i,artists[i])
        choices[i] = artists[i]
    index = helper.get_choice(choices.keys())

    # user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for",choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    # prepare query and show results
    query = "SELECT DISTINCT name FROM songs WHERE Artist=:artist ORDER BY RANDOM()"
    dictionary = {"artist":choices[index]}
    if num != 0:
        query +=" LIMIT:lim"
        dictionary["lim"] = num
    helper.pretty_print(db_ops.name_placeholder_query(query,dictionary))


# option 2, search table for songs by genre
def search_by_genre():
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    print("Genres in playlist:")
    genres = db_ops.single_attribute(query)

    # show genres in table, also create dictionary for choices
    choices = {}
    for i in range(len(genres)):
        print(i,genres[i])
        choices[i] = genres[i]
    index = helper.get_choice(choices.keys())

    # how many records
    print("How many songs do you want returned for",choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    # run query and show results
    query = "SELECT DISTINCT name FROM songs WHERE Genre =:genre ORDER BY RANDOM()"
    dictionary = {"genre":choices[index]}
    if num != 0:
        query +=" LIMIT:lim"
        dictionary["lim"] = num
    helper.pretty_print(db_ops.name_placeholder_query(query,dictionary))

# option 3, search songs by asc,desc order of audio feature
def search_by_feature():
    features = ['Danceability','Liveness','Loudness'] # features to show the user
    choices = {}
    for i in range(len(features)):
        print(i,features[i])
        choices[i] = features[i]
    index = helper.get_choice(choices.keys())

    # how many records
    print("How many songs do you want returned for "+choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    # order  by ascending or descending
    print("Do you want results sorted by the feature in ascending or descending order?")
    order = input("ASC or DESC: ")

    # prepare query and show results
    query = "SELECT DISTINCT Name FROM songs ORDER BY "+choices[index]+" "+order
    dictionary = {}
    if num!=0:
        query+=" LIMIT :lim"
        dictionary['lim'] = num
    helper.pretty_print(db_ops.name_placeholder_query(query,dictionary))

def get_song_record(song_name):
        query = '''
        SELECT *
        FROM songs
        WHERE Name=:song_name;
        '''
        dictionary = {"song_name": song_name}
        return list(db_ops.single_record_options(query, dictionary))

def update_song(song_id, col_name, attr_value):
    query = f'''
    UPDATE songs
    SET {col_name} = :attr_value
    WHERE songID = :song_id;
    '''
    dictionary = {'attr_value': attr_value, 'song_id': song_id}
    db_ops.update_records(query, dictionary)

def delete_song(song_id):
    query = f'''
    DELETE FROM songs
    WHERE songID = :song_id;
    '''
    dictionary = {'song_id': song_id}
    try:
        db_ops.update_records(query, dictionary)
    except Exception as e:
        print(f"Error: Cannot delete song.\n{e}")
        #  return -1 if not successful
        return -1
    # return 1 if successful
    return 1

def get_valid_artist_name():
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    ARTIST_NAMES = db_ops.name_placeholder_query(query=query, dictionary={})
    artist_name = input("Enter artist name: ")
    isValid = artist_name in ARTIST_NAMES
    while isValid == False:
        print(f"Error: song name - {artist_name} - does not exist. Please try again.")
        artist_name = input("Enter 0 to view all of the artist names or enter an artist name: ")
        if artist_name == '0':
            print(f"Artists:\n{ARTIST_NAMES}")
            continue
        isValid = artist_name in ARTIST_NAMES
    return artist_name

def get_valid_album_name():
    query = '''
    SELECT DISTINCT Album
    FROM songs;
    '''
    ALBUM_NAMES = db_ops.name_placeholder_query(query=query, dictionary={})
    album_name = input("Enter album name: ")
    isValid = album_name in ALBUM_NAMES
    while isValid == False:
        print(f"Error: album name - {album_name} - does not exist. Please try again.")
        album_name = input("Enter 0 to view all of the album names or enter an album name: ")
        if album_name == '0':
            print(f"Albums:\n{ALBUM_NAMES}")
            continue
        isValid = album_name in ALBUM_NAMES
    return album_name

def get_valid_genre_name():
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    GENRE_NAMES = db_ops.name_placeholder_query(query=query, dictionary={})
    genre_name = input("Enter genre name: ")
    isValid = genre_name in GENRE_NAMES
    while isValid == False:
        print(f"Error: genre name - {genre_name} - does not exist. Please try again.")
        genre_name = input("Enter 0 to view all of the genre names or enter an genre name: ")
        if genre_name == '0':
            print(f"Genres:\n{GENRE_NAMES}")
            continue
        isValid = genre_name in GENRE_NAMES
    return genre_name

def get_valid_song_name():
    query = '''
    SELECT DISTINCT Name
    FROM songs;
    '''
    SONG_NAMES = db_ops.name_placeholder_query(query=query, dictionary={})
    song_name = input("Enter song name: ")
    isValid = song_name in SONG_NAMES
    while isValid == False:
        print(f"Error: song name - {song_name} - does not exist. Please try again.")
        song_name = input("Enter 0 to view all of the songs or enter a song name: ")
        if song_name == '0':
            print(f"Songs:\n{SONG_NAMES}")
            continue
        isValid = song_name in SONG_NAMES
    return song_name

# BONUS 3: remove all records from the table that have atleast 1 NULL value.
# Option 6. Remove Records with NULL values.
def delete_incomplete_records():
    query = '''
    SELECT *
    FROM songs;
    '''
    col_names = db_ops.get_record_col_names(query, {})
    print(f"Col Names: {col_names}")
    for col in col_names:
        query=f'''
        DELETE FROM
        songs WHERE {col} IS NULL;
        '''
        db_ops.update_records(query, {})
    print("Successfully deleted NULL records")

# Option 7. Delete Records in Bulk by a condition.
def delete_by_bulk():
    attr_list = ["Album", "Artist", "Genre"]
    for index, attr in enumerate(attr_list):
        print(f"({index}) ***** {attr}")
    res = helper.get_choice([0,1,2])
    chosen_attr = attr_list[res]
    new_value = None
    if res == 0:
        new_value = get_valid_album_name()
    elif res == 1:
        new_value = get_valid_artist_name()
    elif res == 2:
        new_value = get_valid_genre_name()
    query = f'''
    DELETE FROM songs
    WHERE {chosen_attr} = :new_value
    '''
    dictionary = {"new_value": new_value}
    db_ops.update_records(query, dictionary)
        
def main():
    # main program
    pre_process()
    start_screen()
    while True:
        user_choice = options()
        if user_choice == 1:
            search_by_artist()
        elif user_choice == 2:
            search_by_genre()
        elif user_choice == 3:
            search_by_feature()
        elif user_choice == 4:
            update_song_by_name()
        elif user_choice == 5:
            delete_song_by_name()
        elif user_choice == 6:
            delete_incomplete_records()
        elif user_choice == 7:
            delete_by_bulk()
        elif user_choice == 0:
            print("Goodbye!")
            break



    db_ops.destructor()

if __name__ == "__main__":
    main()
