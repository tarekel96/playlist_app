# module defines an application to curate a playlist
# with a sqlite3 db as a backend for data storage

from helper import helper
from db_operations import db_operations

data = helper.data_cleaner("songs.csv")

# modify to your chinook db connection
db_ops = db_operations("../chinook.db")

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
    if is_empty():
        attribute_count = len(data[0])
        placeholders = ("?,"*attribute_count)[:-1]
        query = "INSERT INTO songs VALUES("+placeholders+")"
        db_ops.bulk_insert(query,data)


def start_screen():
    print("Welcome to your playlist!")


# show user options
def options():
    print("Select from the following menu options:\n1 Find songs by artist\n" \
    "2 Find songs by genre\n3 Find songs by feature\n4 Exit")
    return helper.get_choice([1,2,3,4])

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
        print("Goodbye!")
        break



db_ops.destructor()
