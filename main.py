"""
This is a program that handels a youtube playlist for easier usage.
After YouTube removed function (actually is back now) to sort by oldest vids, I created this little program to help me watch my fav. ytber.
This software is helpful with a big or gigantic playlist, in my case I work with 6000+ videos.
It does work fine with any type of playlist on YT

Created by rakx | 2022-...
"""
import pickle as DATA
import configparser
import webbrowser
import platform
import pytube
import os


# importing and reading .ini file
conf = configparser.ConfigParser()
conf.read("config.ini")


# Cheking OS and applying some functions for specific system
if platform.system().lower() == "windows":
    clear_console = lambda: os.system("cls")

    def open_web(url:str) -> None:
        webbrowser.open(url)

else:
    clear_console = lambda: os.system("clear")

    def open_web(url:str) -> None:
        """Made for linux based distros, 'cause of some dificulties with opening a page with python
        """
        print(f"Enjoy -> {url}")


changes:int = 0
file_name:str = conf["CHANNEL"]["channel"].replace('"', "")


def save(dict:dict) -> None:
    """Saves a dict into specific file
    """
    with open(f"{file_name}.yt", "wb") as file_:
        DATA.dump(dict, file_)


def load_file() -> DATA:
    """Loads data from a specifict data file
    """
    with open(f"{file_name}.yt", "rb") as file_:
        return DATA.load(file_)
    

def progress_bar(prog, total) -> None:
    """Progress bar functon.
    Creates a progress bar depending on code below
    """
    percent = 100 * (prog / float(total))
    bar = "#" * int(percent) + "-" * (100 - int(percent))
    print(f"\r[{bar}] {percent:.2f}%", end="\r")


if not os.path.isfile(file_name+".yt") and os.path.isfile("main.py"):

    new_file_data:dict = {  "t_vid": 0,  "w_ed": [],  "names": [] }
    save(new_file_data)


get_data = load_file() # loads dict with data from a file
playlist_url = conf["CHANNEL"]["playlist"].replace('"', "")
playlist = pytube.Playlist(playlist_url) # loads playlist from given url


watched:list = get_data["w_ed"]                         # loading list of INTs (playlist video ids) from a file
preloaded_p_len:int = get_data["t_vid"]                 # loading length of a playlist since last usage, to update list
preloaded_v_names:list = get_data["names"]              # loading (list STR) video names from a file

# temporary urls for faster usage under runtime. Never changes under runtime
temp_urls:list = []
# progress bar counter    
prog_bar_counter:int = 0

clear_console()


print("(!) Loading videos, may take time...")
progress_bar(prog_bar_counter, playlist.length)


# preloads and put all videos from playlist to temporary url list
for url in playlist.video_urls:
    temp_urls.append(url)
    progress_bar(prog_bar_counter + 1, playlist.length)
    prog_bar_counter += 1


# checks if preloaded length isn't matches with existent playlist length to syncronize video ids
if preloaded_p_len != len(temp_urls): 
    new_vids = len(temp_urls) - preloaded_p_len
    preloaded_p_len = len(temp_urls)
    k=0

    for video_id in watched:
        video_id += new_vids
        watched[k] = video_id
        k+=1
    
    changes = 1


prog_bar_counter:int = 0
clear_console()


print("(!) Loading names, may take time...") 
 

# checks if it a new file or not
if len(watched) != 0:

    progress_bar(prog_bar_counter, len(watched))

    for video_id in watched: # Video names loader

        if video_id in watched: continue # if new videos in a playlist does not exists: skips name loading for faster star up (big playlists)

        else: # loades new video names
            preloaded_v_names.append(pytube.YouTube(temp_urls[video_id]).title)
            progress_bar(prog_bar_counter + 1, len(watched))
            prog_bar_counter += 1


clear_console()    


if changes: print("(i) Changes was made. Successfully updated list!")

print(f"(i) Videos are loaded, total -> {preloaded_p_len}")

file_data:dict = {  "t_vid": preloaded_p_len,  "w_ed": watched,  "names": preloaded_v_names  } # dict stored in a specific file


if __name__ == "__main__":
    while 1:
        try:
            save(file_data) # on each loop changes saves into file
            print(f"Watching > {playlist.title} by {playlist.owner} | Total: {preloaded_p_len}")

            user_input = input("[> ").lower().split() # user input

            if len(user_input) == 1 and user_input[0] == "help":

                print("""
            (?) Type 'help' for help
            (?) Type 'watch [video id]' to watch a specific video
            (?) Type 'watched' to see a list of videos you have watched
                """)
            

            elif len(user_input) == 2:
                if user_input[0] == "watch":
                    i = 0

                    # checks if entered video was already watched for dublicate prevention
                    if int(user_input[1]) in watched:

                        for url in temp_urls:
                            if i == int(user_input[1]):

                                open_web(url)
                                break

                            i+=1
                        continue

                    i = 0

                    # finds video by ID and searchs for it in the temporary ulr list
                    for url in temp_urls:
                        if i == int(user_input[1]):

                            preloaded_v_names.append(pytube.YouTube(temp_urls[i]).title) # adds new video name to watched videos dict
                            watched.append(i) # adds to watched list
                            open_web(url) # open youtube video
                            break

                        i += 1

            # list all watched videos
            elif len(user_input) == 1:
                if user_input[0] == "watched":
                    i = 0
                    for video_id in watched:

                        print(f"Video id: {video_id}\t||\t{preloaded_v_names[i]}") # prints video_id and name of the video
                        i+=1

                    print(f"(i) You have watched {len(watched)}/{preloaded_p_len} videos\n") # some stats


            elif len(user_input) == 1 and user_input[0] == "clear": clear_console()

            elif len(user_input) == 1 and user_input[0] == "q": break


        except KeyError as e:
            print(f"Bad key: {e}")
            

    else:
        print("Exiting!")
