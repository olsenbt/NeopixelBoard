import time
import board
import neopixel
from PIL import Image
import pytz
from datetime import datetime

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

# Load number images for hours and minutes
number_images = {}
for i in range(10):
    number_images[str(i)] = Image.open(f"{i}.png").convert("RGB")

# Define 3x5 pixel art for seconds and "AM/PM"
small_art = {
    '0': [
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    '1': [
        [0, 1, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 1],
    ],
    '2': [
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
    ],
    '3': [
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    '4': [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
    ],
    '5': [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    '6': [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    '7': [
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 0],
    ],
    '8': [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ],
    '9': [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
    ],
    'P': [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 0],
        [1, 0, 0],
    ],
    'A': [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
    ],
    'M': [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
    ],
}

def create_time_image():
    # Create a blank image with the size of your LED board
    image = Image.new('RGB', (cols, rows), color=(0, 0, 0))
    
    # Get the current time in PST
    tz = pytz.timezone('America/Los_Angeles')
    current_time = datetime.now(tz)
    formatted_time = current_time.strftime("%I%M%S %p")
    hours = formatted_time[:2].lstrip('0')  # Remove leading zero from hour
    if len(hours) == 1:  # If hours is single digit, pad with space
        hours = '0' + hours
    minutes = formatted_time[2:4]
    seconds = formatted_time[4:6]
    period = formatted_time[-2:]  # AM or PM


    # TODO: Fix below
    image.paste(number_images[hours[0]], (0, 0))
    image.paste(number_images[hours[1]], (8, 0))
    
    # Place minutes
    image.paste(number_images[minutes[0]], (0, 13))
    image.paste(number_images[minutes[1]], (8, 13))
    
    # Place seconds (3x5 pixel art)
    for idx, char in enumerate(seconds):
        if char in small_art:
            for y, row in enumerate(small_art[char]):
                for x, pixel in enumerate(row):
                    if pixel:
                        if idx == 0:
                            image.putpixel((17 + x, 18 + y), (255, 255, 255))
                        else:
                            image.putpixel((21 + x, 18 + y), (255, 255, 255))

    # Place AM/PM
    for y, row in enumerate(small_art[period[0]]):
        for x, pixel in enumerate(row):
            if pixel:
                image.putpixel((17 + x, 6 + y), (255, 255, 255))
    for y, row in enumerate(small_art[period[1]]):
        for x, pixel in enumerate(row):
            if pixel:
                image.putpixel((21 + x, 6 + y), (255, 255, 255))

    return image

def display_image(image):
    for i in range(PIXEL_COUNT):
        x, y = coords[i]
        if x < cols and y < rows:
            r, g, b = image.getpixel((x, y))
            pixels[i] = (g, r, b)  # Change to (g, r, b) for GRB pixel order
    # Show pixels
    pixels.show()

try:
    while True:
        start_time = time.time()
        # Create an image with the current time
        image = create_time_image()
        # Display the image
        display_image(image)
        end_time = time.time()
        elapsed_time = end_time - start_time
        remaining_sleep = max(1 - elapsed_time, 0)
        # Wait for one second before updating
        time.sleep(remaining_sleep)

except KeyboardInterrupt:
    pixels.fill((0, 0, 0))  # Turn off all LEDs when the program is interrupted
    pixels.show()
    print("Program canceled by the user. All NeoPixels turned off.")
