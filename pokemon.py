import time
import board
import neopixel
import sys
import requests
from PIL import Image
from io import BytesIO

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

pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False, brightness=BRIGHTNESS, pixel_order=neopixel.GRB)

rows = 25
cols = 24

def get_pokemon_sprite(pokedex_number):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokedex_number}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        sprite_url = data['sprites']['versions']['generation-viii']['icons']['front_default']
        if sprite_url:
            return sprite_url, False
        else:
            return data['sprites']['front_default'], True

    return None, False

def load_image_from_url(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    # Ensure image is in RGBA format
    image = image.convert("RGBA")
    return image

def crop_image(image):
    width, height = image.size
    left, top = width, height
    right, bottom = 0, 0
    for x in range(width):
        for y in range(height):
            _, _, _, a = image.getpixel((x, y))
            if a > 0:
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)
    return image.crop((left, top, right + 1, bottom + 1))

def resize_and_center_image(image):
    # Resize image to fit within the 24x25 dimensions while maintaining aspect ratio
    image.thumbnail((cols, rows), Image.LANCZOS)
    # Create a new transparent image with 24x25 dimensions
    new_image = Image.new("RGBA", (cols, rows), (0, 0, 0, 0))
    # Get the size of the resized image
    resized_width, resized_height = image.size
    # Calculate position to center the resized image on the new image
    x_offset = (cols - resized_width) // 2
    y_offset = (rows - resized_height) // 2
    # Paste the resized image onto the new image
    new_image.paste(image, (x_offset, y_offset))
    return new_image

def display_image(image):
    width, height = image.size
    for i in range(PIXEL_COUNT):
        x, y = coords[i]
        if x < width and y < height:
            try:
                r, g, b, a = image.getpixel((x, y))
                if a > 0:  # Check alpha value to account for transparency
                    pixels[i] = (g, r, b)  # Change to (g, r, b) for GRB pixel order
                else:
                    pixels[i] = (0, 0, 0)  # Turn off the pixel if alpha is 0
            except IndexError:
                pixels[i] = (0, 0, 0)  # Turn off the pixel if coordinates are out of range
        else:
            pixels[i] = (0, 0, 0)  # Turn off the pixel if it's out of range
    # Show pixels
    pixels.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pokemon.py <pokedex number>")
        sys.exit(1)
        
    pokedex_number = sys.argv[1]

    try:
        # Fetch the sprite URL from PokeAPI
        sprite_url, is_fallback = get_pokemon_sprite(pokedex_number)
        if sprite_url:
            # Load the image from the URL
            image = load_image_from_url(sprite_url)
            # Crop the image to remove whitespace
            cropped_image = crop_image(image)
            if is_fallback:
                # Resize and center the image to fit on the LED board
                final_image = resize_and_center_image(cropped_image)
            else:
                final_image = cropped_image

            # Display the image
            display_image(final_image)
            if is_fallback:
                print(f"Displaying fallback sprite for Pokémon #{pokedex_number}")
            else:
                print(f"Displaying sprite for Pokémon #{pokedex_number}")
        else:
            print(f"Could not find sprite for Pokémon #{pokedex_number}")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        pixels.show()
