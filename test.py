import cv2
import numpy as np
import sys

# ASCII characters used to build the output (from darkest to lightest)
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    (old_height, old_width) = image.shape
    aspect_ratio = old_height / old_width
    new_height = int(aspect_ratio * new_width / 2)  # Divided by 2 to account for character aspect ratio
    return cv2.resize(image, (new_width, new_height))

def pixels_to_ascii(image):
    pixels = image.flatten()
    ascii_str = ""
    for pixel in pixels:
        # Convert pixel to integer before calculation
        pixel_value = int(pixel)
        # Map pixel value (0-255) to our ASCII_CHARS (0-len(ASCII_CHARS)-1)
        index = min(pixel_value * len(ASCII_CHARS) // 256, len(ASCII_CHARS) - 1)
        ascii_str += ASCII_CHARS[index]
    return ascii_str

def main():
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        sys.exit()
    
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Resize and convert to ASCII
            resized = resize_image(gray, new_width=100)
            ascii_str = pixels_to_ascii(resized)
            
            # Format the ASCII string
            img_width = resized.shape[1]
            ascii_str_len = len(ascii_str)
            ascii_img = ""
            
            # Split the string based on width of the image
            for i in range(0, ascii_str_len, img_width):
                ascii_img += ascii_str[i:i+img_width] + "\n"
            
            # Clear the terminal and print ASCII art
            print("\033[H\033[J")  # ANSI escape codes to clear screen
            print(ascii_img)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()