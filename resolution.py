import os
from PIL import Image

def generate_low_res_images(source_folder, output_folder, max_size=(2048, 1024)):
    """
    Generates low-resolution versions of images from the source_folder.
    Saves the resized images in the output_folder.

    Parameters:
    - source_folder (str): Path to the folder containing high-res images.
    - output_folder (str): Path to the folder where low-res images will be stored.
    - max_size (tuple): The maximum width and height (in pixels) for the low-res images.
    """
    # Create the output directory if it doesn't exist.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Determine the appropriate resampling filter based on Pillow version.
    if hasattr(Image, 'Resampling'):
        resample_filter = Image.Resampling.LANCZOS
    else:
        resample_filter = Image.ANTIALIAS

    # Process each image file in the source folder.
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            source_path = os.path.join(source_folder, filename)
            try:
                with Image.open(source_path) as img:
                    # Resize the image while preserving aspect ratio.
                    img.thumbnail(max_size, resample=resample_filter)
                    
                    # Save the low-res image.
                    low_res_path = os.path.join(output_folder, filename)
                    img.save(low_res_path)
                    print(f"Saved low-res image: {low_res_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Example usage:
if __name__ == "__main__":
    high_res_folder = 'static/images/'
    low_res_folder = 'static/images/low_res'
    generate_low_res_images(high_res_folder, low_res_folder)
