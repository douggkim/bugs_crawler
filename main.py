from bs4 import BeautifulSoup
from SpotifyManager import spotifyManager
import requests
from selenium import webdriver
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime

# TODO 0 : get all the credentials
with open("bugs_crawler/CONFIG.txt") as file:
    SPOTIFY_CLIENT_ID = file.readline().strip()
    SPOTIFY_CLIENT_TOKEN = file.readline().strip()
    USER_ID = file.readline().strip()
    SPOTIFY_REDIRECT_URI = "http://example.com"

# TODO 1 : Set up selenium driver
chrome_driver_path = "/Users/dougkim/dev/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get("https://music.bugs.co.kr/")


# TODO 2: Login
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                        '/html/body/div[2]/header/div[3]/div[2]/div/div[1]/a')))
login_regi_button = driver.find_element(By.XPATH,"/html/body/div[2]/header/div[3]/div[2]/div/div[1]/a")
login_regi_button.click()

login_with_bugs_button = driver.find_element(By.XPATH,"/html/body/div[2]/header/div[3]/div[2]/div/div[1]/aside/div[3]/form/div/a[1]")
login_with_bugs_button.click()

id_input = driver.find_element(By.XPATH,"/html/body/div[2]/header/div[3]/div[2]/div/div[1]/aside/fieldset/form/div/div[1]/p/span[1]/input")
pw_input = driver.find_element(By.XPATH,"/html/body/div[2]/header/div[3]/div[2]/div/div[1]/aside/fieldset/form/div/div[1]/p/span[2]/input")


id_input.send_keys("slakingex")
pw_input.send_keys("evlngood2!")

login_confirm = driver.find_element(By.XPATH,"/html/body/div[2]/header/div[3]/div[2]/div/div[1]/aside/fieldset/form/div/div[1]/button")
login_confirm.click()


# TODO 3 : choose the playlist
WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH,
                                                                        '/html/body/div[2]/div[1]/div/div/div[1]/nav/ul/li[10]/div/ul/li[1]/a')))
target_playlist = driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div/div/div[1]/nav/ul/li[10]/div/ul/li[1]/a")
target_playlist.click()



# TODO 4 : Target the playlist items 
WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#USER_ALBUM_TRACK26085855 > table')))

playlist_table = driver.find_element(By.CSS_SELECTOR, '#USER_ALBUM_TRACK26085855 > table')

playlist_elements = playlist_table.find_elements(By.TAG_NAME,"tr")

playlist = []

# start iterating from the second element because the first element is the song/artist label 
for song in playlist_elements[1:]: 
    song_title = song.find_element(By.CLASS_NAME, "title")
    # sometimes there are [권리없는 곡] labels, so remove it 
    song_title = song_title.text.replace("[권리없는 곡] ", "")
    # songs with featuring has the featured artists btw the parenthese, so remove them 
    song_title = song_title.split("(")[0]
    
    song_artist = song.find_element(By.CLASS_NAME,"artist")
    # sometimes there are multiple artists who participated in one song, so remove them based on line change 
    song_artist = song_artist.text.split("\n")[0]
    # korean pronounciation is written for foreign artists after parenthese, so remove them 
    song_artist = song_artist.split("(")[0]
    
    playlist_element = [song_title, song_artist]
    playlist.append(playlist_element)

print(playlist)

# TODO 5 : load spotify manager
spotifymanager = spotifyManager(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_TOKEN, SPOTIFY_REDIRECT_URI)

# TODO 4 : create a playlist=
playlist_id = spotifymanager.create_playlist(user_id=USER_ID, playlist_name=f"Drive Music {datetime.datetime.now()}")

# TODO 5 : search songs on spotify
song_id_list = []
for song in playlist:
    track_id = spotifymanager.search(track=song[0], artist=song[1])
    if track_id is None:
        print(f"No song found for {song[0]} / {song[1]}")
        continue
    else:
        song_id_list.append(track_id)
        print(f"{len(song_id_list)} / {len(playlist)} songs added to playlist.")
print(f"Number of Songs found on Spotify: {len(song_id_list)}")

# TODO 6 : add_songs_to_the_playlist
for song in song_id_list:
    print(spotifymanager.add_items_to_playlist(track_id=[song], playlist_id=playlist_id))




