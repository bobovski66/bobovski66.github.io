import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv
import re

# Function to extract relative points from the image
def generate_relative_points(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    _, binary_dynamic = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY_INV)

    edges_sobel = cv2.Sobel(binary_dynamic, cv2.CV_64F, 1, 0, ksize=5) + cv2.Sobel(binary_dynamic, cv2.CV_64F, 0, 1, ksize=5)
    edges_canny = cv2.Canny(binary_dynamic, threshold1=50, threshold2=150)
    edges_laplacian = cv2.Laplacian(binary_dynamic, cv2.CV_64F)

    edges_combined = np.uint8(np.absolute(edges_sobel) + edges_canny + edges_laplacian)

    contours, _ = cv2.findContours(edges_combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    points = np.vstack(contours)

    center = np.array(image.shape) / 2
    relative_points = points[:, 0, :] - center

    return relative_points

# Function to save points to an image
def save_points_as_image(points, output_path, shape):
    points_image = np.ones(shape, dtype=np.uint8) * 255  # Create a white image
    for point in points:
        x, y = np.int32(point + np.array(shape) / 2)
        if 0 <= x < shape[1] and 0 <= y < shape[0]:
            points_image[y, x] = 0  # Plot the points as black
    cv2.imwrite(output_path, points_image)

# Function to load relative points from the image
def load_relative_points(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    points = np.column_stack(np.where(image < 255))
    center = np.array(image.shape) / 2
    relative_points = points - center
    return relative_points

# Function to calculate centroidal distances and angular distribution
def calculate_distributions(points):
    distances = np.sqrt(points[:, 0]**2 + points[:, 1]**2)
    angles = np.degrees(np.arctan2(points[:, 1], points[:, 0]))
    return distances, angles

# Function to save distributions to CSV
def save_distributions_to_csv(distances, angles, output_csv_path):
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Distance", "Angle"])
        for dist, ang in zip(distances, angles):
            writer.writerow([dist, ang])

# Function to plot histograms and return the path to the combined image
def plot_histograms(distances, angles, output_dir, n):
    plt.figure(figsize=(10, 5))
    
    # Plotting absolute centroidal distances
    plt.subplot(1, 2, 1)
    plt.hist(distances, bins=30, color='blue', alpha=0.7)
    plt.title('Centroidal Distances (Absolute)')
    plt.xlabel('Distance from Center')
    plt.ylabel('Frequency')
    plt.grid(True)

    # Plotting absolute angular distribution
    plt.subplot(1, 2, 2)
    plt.hist(angles, bins=36, range=(-180, 180), color='green', alpha=0.7)
    plt.title('Angular Distribution (Absolute)')
    plt.xlabel('Angle (degrees)')
    plt.ylabel('Frequency')
    plt.grid(True)

    # Save the combined image
    combined_hist_img = os.path.join(output_dir, f'combined_hist{n}.png')
    plt.savefig(combined_hist_img)
    plt.close()

    return combined_hist_img

def create_html_summary(image1, points_img, combined_hist_img, csv_file, output_dir, n):
    html_content = f"""
    <html>
    <head>
        <title>Crop Circle Analysis Summary {n}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            img {{
                width: 100%;
                max-width: 500px;
                margin-bottom: 20px;
            }}
            .content {{
                max-width: 800px;
                margin: auto;
            }}
        </style>
    </head>
    <body>
        <div class="content">
            <h1>Crop Circle Analysis Summary {n}</h1>
            <h2>Original Image</h2>
            <img src="{os.path.basename(image1)}" alt="Original Image">
            <h2>Points Image</h2>
            <img src="{os.path.basename(points_img)}" alt="Points Image">
            <h2>Histogram Summary</h2>
            <img src="{os.path.basename(combined_hist_img)}" alt="Histogram Summary">
            <h2>Download CSV Data</h2>
            <a href="{os.path.basename(csv_file)}" download>Download CSV</a>
            <br><br>
            <a href="../index.html">Back to Index</a>
        </div>
    </body>
    </html>
    """
    
    html_file = os.path.join(output_dir, f'summary{n}.html')
    with open(html_file, 'w') as file:
        file.write(html_content)

    return f'summary{n}.html'

# Function to create a thumbnail for the image
def create_thumbnail(image_path, thumbnail_path, size=(100, 100)):
    image = cv2.imread(image_path)
    thumbnail = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
    cv2.imwrite(thumbnail_path, thumbnail)

def run_analysis_in_directory(directory):
    # Ensure to change back to the base directory in case of an error
    base_directory = os.getcwd()

    try:
        os.chdir(directory)

        # Find the image file in the directory (imagen.png)
        image_file = None
        for filename in os.listdir('.'):
            if filename.startswith('image') and filename.endswith('.png'):
                image_file = filename
                break
        
        if not image_file:
            print(f"Error: No image file found in the directory {directory}.")
            return
        
        # Extract the number from the image file (e.g., "2" from "image2.png")
        n = re.search(r'\d+', image_file).group()
        
        # Generate the points file
        points_output_path = f'points{n}.png'
        points = generate_relative_points(image_file)
        image_shape = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE).shape
        save_points_as_image(points, points_output_path, image_shape)
        print(f'Generated {points_output_path} from {image_file}.')
        
        # Analyze the generated points
        points_img_path = points_output_path
        output_csv_path = f'data{n}.csv'  # CSV file with data
        
        # Load relative points from the image
        points = load_relative_points(points_img_path)
        
        # Calculate distributions
        distances, angles = calculate_distributions(points)
        
        # Plot and save histograms
        combined_hist_img = plot_histograms(distances, angles, '.', n)
        
        # Create thumbnails for the original image and the combined histogram
        thumbnail_image_path = f'thumbnail_image{n}.png'
        thumbnail_hist_path = f'thumbnail_hist{n}.png'
        create_thumbnail(image_file, thumbnail_image_path)
        create_thumbnail(combined_hist_img, thumbnail_hist_path)
        
        # Create HTML summary
        summary_html = create_html_summary(image_file, points_img_path, combined_hist_img, output_csv_path, '.', n)

        print(f'Analysis completed for directory: {directory}')
        return os.path.join(directory, summary_html), thumbnail_image_path, thumbnail_hist_path
    finally:
        # Ensure to change back to the base directory even if an error occurs
        os.chdir(base_directory)

def create_index_html(base_directory, summary_links):
    index_content = """
    <html>
    <head>
        <title>Crop Circle Analysis Index</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            .content {
                max-width: 800px;
                margin: auto;
            }
            .entry {
                margin-bottom: 20px;
                display: flex;
                align-items: center;
            }
            .entry img {
                margin-right: 10px;
                width: 100px;
                height: 100px;
                object-fit: cover;
            }
            .entry a {
                font-size: 18px;
            }
        </style>
    </head>
    <body>
        <div class="content">
            <h1>Crop Circle Analysis Index</h1>
    """

    for idx, (summary_link, thumbnail_image, thumbnail_hist) in enumerate(summary_links, start=1):
        # Ensure that all paths are relative to the base directory
        summary_directory = os.path.relpath(os.path.dirname(summary_link), base_directory)
        relative_thumbnail_image_path = os.path.join(summary_directory, os.path.basename(thumbnail_image))
        relative_thumbnail_hist_path = os.path.join(summary_directory, os.path.basename(thumbnail_hist))
        relative_summary_link = os.path.relpath(summary_link, base_directory)

        # Convert backslashes to forward slashes for HTML compatibility
        relative_thumbnail_image_path = relative_thumbnail_image_path.replace("\\", "/")
        relative_thumbnail_hist_path = relative_thumbnail_hist_path.replace("\\", "/")
        relative_summary_link = relative_summary_link.replace("\\", "/")

        index_content += f'''
        <div class="entry">
            <img src="{relative_thumbnail_image_path}" alt="Image Thumbnail">
            <img src="{relative_thumbnail_hist_path}" alt="Histogram Thumbnail">
            <a href="{relative_summary_link}">Summary {idx}</a>
        </div>
        '''

    index_content += """
        </div>
    </body>
    </html>
    """

    with open(os.path.join(base_directory, 'index.html'), 'w') as file:
        file.write(index_content)

# Function to traverse and analyze all subdirectories
def traverse_and_analyze(base_directory):
    summary_links = []

    # Sort the directories based on the number in imagen.png
    subdirectories = sorted(
        [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))],
        key=lambda d: int(re.search(r'\d+', d).group())
    )

    for dir_name in subdirectories:
        directory_path = os.path.join(base_directory, dir_name)
        # Updated to expect 3 return values
        summary_html, thumbnail_image, thumbnail_hist = run_analysis_in_directory(directory_path)
        if summary_html and thumbnail_image and thumbnail_hist:
            summary_links.append((summary_html, thumbnail_image, thumbnail_hist))
        os.chdir(base_directory)  # Go back to the base directory

    # Create the index.html file
    create_index_html(base_directory, summary_links)
    print("Index page created with links to all summary pages.")


if __name__ == "__main__":
    base_directory = os.getcwd()  # Start in the current directory
    traverse_and_analyze(base_directory)
