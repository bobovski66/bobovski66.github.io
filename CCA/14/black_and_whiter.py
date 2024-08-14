import os
import cv2
import re

# Loop over all files in the current directory
for filename in os.listdir('.'):
    # Match files that start with 'photon' and end with '.png'
    match = re.match(r'photo(\d+)\.png', filename)
    if match:
        n = match.group(1)  # Extract the number N from the filename
        image_path = filename
        output_path = f'image{n}.png'
        
        # Load the image
        image = cv2.imread(image_path)
        
        # Convert to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply binary thresholding to create a black and white image
        _, bw_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        
        # Save the black and white image as imagenN.png
        cv2.imwrite(output_path, bw_image)
        
        print(f"Converted {image_path} to {output_path}")
