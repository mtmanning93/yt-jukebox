import time
import gspread
from google.oauth2.service_account import Credentials

from simple_term_menu import TerminalMenu

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('playsong_jukebox')
JUKEBOX = SHEET.worksheet('library')

# Initial genre menu
GENRE_LIST = JUKEBOX.col_values(3)[1:]

# Initial user menu
SEARCH_MENU = {
    'A': 'Artist Name',
    'B': 'Song Title',
    'C': 'Genre',
    'D': 'Year'
}


def update_genre_list(data, inst):
    """
    Searches list of genres.
    Adds new genre input to list if not already in list.
    """
    for x in data:
        if data.count(x) > inst:
            while x in data:
                data.remove(x) 

    print(data)

    return data


def add_song():
    """
    Enables user to add songs to the library
    """
    print(
        "To add a song to the jukebox please follow the steps below. \n"
    )

    new_song = []

    # artist
    input_artist = input("Please enter artists name: \n")
    new_song.append(input_artist)
    print("")
    # title
    input_title = input("Please enter song title: \n")
    new_song.append(input_title)
    print("")
    # genre
    add_genre = input("Please enter genre: \n")
    new_song.append(add_genre.lower())
    print("")
    # print(new_song)

    if add_genre not in GENRE_LIST:
        GENRE_LIST.append(add_genre.lower())
    
    # year
    input_year = input("Please enter year of release: \n")
    new_song.append(input_year)
    print("")
    print("Adding:")
    print(' '.join(new_song).title())
    print("")

    new_song[3] = int(input_year)

    update_library(new_song)


def update_library(data):
    """
    Updates google sheet by adding new song to list
    """
    print("Updating library...\n")
    JUKEBOX.append_row(data)
    time.sleep(2)
    print("Library updated.\n")


add_song()
update_genre_list(GENRE_LIST, 1)