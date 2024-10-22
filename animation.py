import time
import board
import neopixel
import sys
from PIL import Image, ImageSequence

# Read coordinates from file
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
FPS = 10  # Adjust the frame rate as needed

pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False, brightness=BRIGHTNESS, pixel_order=neopixel.GRB)

def display_frame(image):
    for i, (x, y) in enumerate(coords):
        r, g, b = image.getpixel((x, y))
        # Switch green and red channels
        pixels[i] = (g, r, b)
    pixels.show()

def play_animation(gif_file):
    try:
        # Open the GIF file
        gif = Image.open(gif_file)
        # Infinite loop for continuous playback
        while True:
            # Iterate through each frame of the GIF
            for frame in ImageSequence.Iterator(gif):
                # Convert the frame to RGB mode (if not already)
                frame_rgb = frame.convert("RGB")
                # Display the frame
                display_frame(frame_rgb)
                # Wait for the specified time to achieve the desired frame rate
                time.sleep(1 / FPS)
            # After reaching the end of the GIF, reset the iterator to loop
            gif.seek(0)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python animate.py <gif_file>")
        sys.exit(1)

    gif_file = sys.argv[1]

    play_animation(gif_file)
