from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import spotipy
import spotipy.oauth2
country = input("Input the country to get top 100 songs shahzamed:")

# Set up Chrome options
chrome_options = Options()

# Specify the path to chromedriver using the Service class
service = Service(r"C:\Users\abdue\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")

# Initialize the driver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the page
#urls
amazon ="https://www.amazon.ca/charts/2023-11-12/mostsold/nonfiction?ref=chrt_bk_dx_intra_nf_sd"
shahzam = f"https://www.shazam.com/charts/top-200/{country.lower()}"
driver.get(shahzam)

# Wait for the page to load and title elements to be present
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.title > a"))
)

# Now, we can safely use driver.page_source because the page has finished loading
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Use the correct CSS selector to find the song names (or book titles, etc.)
song_names_spans = soup.select(" div.title > a")
song_names = [song.getText().strip() for song in song_names_spans]

# Close the Selenium driver
driver.quit()

# Print out the song names

song_names = [song.getText().strip() for song in song_names_spans]
#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="c96901b2b001480cabe267495dbd8f9a",
        client_secret="3c72d4903eb545f38306bb2ec6c0e11c",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

#Searching Spotify for songs by title
song_uris = []
i = 0
for song in song_names:
    i+=1
    if i == 100:
        break
    simple_song_name = song.split(' (')[0]  # This assumes the format is "Track Name (feat. Artist)"
    result = sp.search(q=f"track:{simple_song_name} ", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{country.capitalize()} Shahzam top 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
