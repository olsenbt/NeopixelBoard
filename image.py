import time
import board
import neopixel
import re
import math
from PIL import Image  # Pillow library for image processing

# Import coords
with open('coords.txt', 'r') as file:
    lines = file.readlines()

coords = []

# Extract X and Y and store them
for line in lines:
    x, y = map(int, line.strip().split(','))
    coords.append((x, y))

# Neopixel Params
PIXEL_COUNT = len(coords)
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
            r, g, b, a = image.getpixel((x, y))
            if a > 0:  # Check alpha value to account for transparency
                pixels[i] = (g, r, b)  # Change to (g, r, b) for GRB pixel order
            else:
                pixels[i] = (0, 0, 0)  # Turn off the pixel if alpha is 0
    # Show pixels
    pixels.show()

try:
    while True:
        # Prompt user for image path
        image_path = input("Enter the path to the image: ")
        # Load the image
        image = load_image(image_path)
        # Display the image
        display_image(image)
        # Delay to allow viewing the image
        time.sleep(1)  # Adjust the delay as needed

except KeyboardInterrupt:
    pixels.fill((0, 0, 0))  # Turn off all LEDs when the program is interrupted
    pixels.show()
    print("Program canceled by the user. All NeoPixels turned off.")