import os
from PIL import Image, ImageDraw

def create_black_and_white_image(circle_position, circle_radius):
    # Step 1: Create a black background image (1080x1920) in vertical format
    width, height = 1080, 1920
    image = Image.new("RGB", (width, height), "black")
    print("Step 1: Created a black background image with dimensions 1080x1920.")

    # Step 2: Draw a white circle at the specified position with the specified radius
    draw = ImageDraw.Draw(image)
    left_up_point = (circle_position[0] - circle_radius, circle_position[1] - circle_radius)
    right_down_point = (circle_position[0] + circle_radius, circle_position[1] + circle_radius)
    draw.ellipse([left_up_point, right_down_point], fill="white")
    print(f"Step 2: Drew a white circle at position {circle_position} with radius {circle_radius}.")

    # Step 3: Ensure the dataset directory exists
    dataset_dir = "dataset"
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
        print(f"Step 3: Created directory '{dataset_dir}'.")

    # Step 4: Save the image with a dynamic name based on circle parameters
    file_name = f"circle_{circle_radius}_{circle_position[0]}_{circle_position[1]}.png"
    file_path = os.path.join(dataset_dir, file_name)
    image.save(file_path)
    print(f"Step 4: Saved the image as '{file_path}'.")
