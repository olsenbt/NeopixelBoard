# NeoPixel LED Matrix Project

### Table of Contents
- [Introduction](#introduction)
- [Image Rendering](#image-rendering)
- [Clock](#clock)
- [PokeAPI Integration](#pokeapi-integration)
- [Spotify Web API Integration](#spotify-web-api-integration)
- [Conclusion](#conclusion)
## Introduction

This project involves the creation of a custom LED matrix using **600 NeoPixel RGB LEDs** arranged in a 24x25 grid, embedded into a white pegboard. By pushing the NeoPixels into the pegboard, I created a interactive LED display capable of rendering complex visuals and animations.

A key feature of the project is the `coords.txt` file, which maps the X and Y coordinates of each individual LED. This allows for accurate rendering of images and animations on the board, overcoming the physical limitations of the LED string layout. With this coordinate mapping, I can control each LED based on its exact position, making it possible to display intricate designs and dynamic patterns.


## Image Rendering

The `image.py` script allows users to render an image onto the 24x25 NeoPixel LED matrix by specifying the path to an image file. The script utilizes the `coords.txt` file to accurately map the X and Y coordinates of each LED, ensuring that the image is displayed correctly on the matrix.

### Key Features

1. **Coordinate Mapping**: The `coords.txt` file provides the exact X and Y positions of each LED in the matrix. This mapping allows the script to convert a 2D image into individual pixel data that corresponds to the layout of the LEDs.
   
2. **Image Processing**: The script uses the Pillow (`PIL`) library to load and process images. It automatically resizes the image to fit the 24x25 grid and converts it to RGBA format. This ensures that the image is rendered in the correct resolution and supports transparency.

3. **Rendering Logic**:
   - The script reads the image pixel-by-pixel and assigns color values to the corresponding LEDs.
   - The NeoPixel library is used to set the colors for each LED, following the GRB (Green, Red, Blue) order.
   - Transparency is taken into account, turning off LEDs where the image has fully transparent pixels.

### Example Workflow

- The user is prompted to input the path to an image.
- The image is processed and resized to the 24x25 matrix dimensions.
- The colors from the image are displayed on the corresponding LEDs using the `coords.txt` file for accurate mapping.

This script provides a dynamic way to display images on the NeoPixel matrix.

## Clock

This script displays the current time on a NeoPixel LED matrix using digit images for hours and minutes, with 3x5 pixel art for seconds and "AM/PM". It updates every second and handles the Pacific Time zone.

## Key Features

1. **Small Pixel Art**
   - A 3x5 grid determines how to render the seconds (`0-9`) and "AM/PM"
   Example: "0"
   ```
       '0': [
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
   ```

2. **Time Image Creation**
   - Retrieves current time in Pacific Time (`%I%M%S %p` format).
   - Pastes number images for hours and minutes into a blank matrix.
   - Adds seconds and "AM/PM" indicators using pixel art.
   - Renders image on neopixel board like in image.py

## PokeAPI Integration

The `pokemon.py` script uses the PokeAPI to fetch and display the sprite of a specified Pokémon on the 24x25 NeoPixel LED matrix. By passing a Pokédex number as an argument, the script retrieves the sprite, processes it, and renders it on the LED grid.

### Key Features

1. **Pokémon Sprite Fetching**: The script queries the PokeAPI for the specified Pokémon’s sprite. The API supports all generations of pokemon.
   
2. **Image Processing**:
   - **Cropping**: Removes unnecessary whitespace around the sprite.
   - **Resizing and Centering**: The image is resized to fit the matrix and centered for display.

3. **LED Rendering**: The sprite is displayed on the NeoPixel matrix, accounting for transparency to ensure clean rendering.

### Usage

To display a Pokémon sprite:
```bash
python pokemon.py <pokedex_number>
```

## Spotify Web API Integration

This script displays the current Spotify album art on the LED matrix, utilizing the `Spotipy` library to fetch the currently playing track's album cover. The program continuously updates the display with the album art while handling transparency and pixel mapping.

## Key Features

1. **Spotify Integration**
   - Uses the `Spotipy` library to connect to the Spotify API, requiring user credentials and appropriate permissions.
   - Fetches the currently playing track’s album art URL and downloads the image.

2. **Image Loading and Resizing**
   - Uses the Pillow library to load and resize album art images to fit the matrix dimensions (24x25 pixels).
   - Ensures images are in RGBA format to handle transparency correctly.

## Conclusion

This project tested my knowledge of image rendering and coordinate mapping. I also got to utilize two web APIs to further expand the functionality of the board. I look to continue development on future projects utilizing these LED lights and further integration of different APIs. 

### Ideas for Future Development
- Implementing a weather API to display a realtime forecast
- Creating a simple game that utilizes the LED matrix for display
- Creating a webapp to interface with the LED matrix similar to what was developed in my [XmasLights ](https://github.com/olsenbt/XmasLights)project