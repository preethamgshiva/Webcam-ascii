import cv2
import numpy as np

# ASCII characters used to build the output (from darkest to lightest)
ASCII_CHARS = "@%#*+=-:.!$^&:;() "

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

def create_ascii_image(ascii_str, img_shape, font_scale=0.5, thickness=1):
    # Create a blank image with white background
    ascii_img = 255 * np.ones((img_shape[0]*15, img_shape[1]*8, 3), dtype=np.uint8)
    
    # Position for text
    y = 15
    x = 0
    
    # Split the ASCII string into lines
    lines = [ascii_str[i:i+img_shape[1]] for i in range(0, len(ascii_str), img_shape[1])]
    
    # Draw each line of ASCII text
    for line in lines:
        cv2.putText(ascii_img, line, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
        y += 15  # Line spacing
    
    return ascii_img

def main():
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    # Create a window
    cv2.namedWindow("ASCII Webcam", cv2.WINDOW_NORMAL)
    
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
            
            # Create ASCII image
            ascii_img = create_ascii_image(ascii_str, resized.shape)
            
            # Display the resulting frame
            cv2.imshow("ASCII Webcam", ascii_img)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()