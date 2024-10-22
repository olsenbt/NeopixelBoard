import time
import board
import neopixel
import re
import math
from PIL import Image  # Pillow library for image processing
import requests
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth  # Add this import statement

# Import coords
with open('coords.txt', 'r') as file:
    lines = file.readlines()

coords = []

# Extract X and Y and store them
for line in lines:
    x, y = map(int, line.strip().split(','))
    coords.append((x, y))

# Neopixel Params
PIXEL_COUNT = 600
BRIGHTNESS = 0.15

pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False, brightness=BRIGHTNESS)

rows = 25
cols = 24

def load_image(image_path):
    # Load the image
    image = Image.open(image_path)
    # Resize the image to fit the 24x25 matrix
    image = image.resize((cols, rows))
    # Ensure image is in RGBA format
    image = image.convert("RGBA")
    return image

def display_image(image):
    for i in range(PIXEL_COUNT):
        x, y = coords[i]
        if x < cols and y < rows:
            if image.mode == 'RGBA':  # Check if the image has an alpha channel
                r, g, b, a = image.getpixel((x, y))
                if a > 0:  # Check alpha value to account for transparency
                    pixels[i] = (g, r, b)  # Change to (g, r, b) for GRB pixel order
                else:
                    pixels[i] = (0, 0, 0)  # Turn off the pixel if alpha is 0
            elif image.mode == 'RGB':  # If no alpha channel, assume RGB
                r, g, b = image.getpixel((x, y))
                pixels[i] = (g, r, b)  # Change to (g, r, b) for GRB pixel order
    # Show pixels
    pixels.show()


def get_spotify_album_art():
    # Add your credentials here
    SPOTIPY_CLIENT_ID = '####'
    SPOTIPY_CLIENT_SECRET = '####'
    SPOTIPY_REDIRECT_URI = '####'
    USERNAME = '####'
    SCOPE = "user-read-currently-playing"

    # Create Spotify object with permissions
    oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                         client_secret=SPOTIPY_CLIENT_SECRET,
                         redirect_uri=SPOTIPY_REDIRECT_URI,
                         username=USERNAME,
                         scope=SCOPE,
                         open_browser=False)

    token_info = oauth.get_cached_token()

    # Check if token needs to be refreshed
    if token_info and oauth.is_token_expired(token_info):
        token_info = oauth.refresh_access_token(token_info['refresh_token'])

    sp = spotipy.Spotify(auth_manager=oauth)

    # Get current playing
    current_playing = sp.current_user_playing_track()

    # Ensure that a track is playing
    if current_playing is not None:
        # Get the album art URL
        album_art_url = current_playing['item']['album']['images'][0]['url']
        return album_art_url
    else:
        return None

try:
    while True:
        # Get Spotify album art URL
        album_art_url = get_spotify_album_art()
        
        if album_art_url:
            # Download the image
            response = requests.get(album_art_url)
            image = Image.open(BytesIO(response.content))
            # Resize the image
            image = image.resize((cols, rows))
            # Display the image
            display_image(image)
        else:
            print("No track is currently playing.")
        
        # Delay to allow viewing the image
        time.sleep(1)  # Adjust the delay as needed

except KeyboardInterrupt:
    pixels.fill((0, 0, 0))  # Turn off all LEDs when the program is interrupted
    pixels.show()
    print("Program canceled by the user. All NeoPixels turned off.")
