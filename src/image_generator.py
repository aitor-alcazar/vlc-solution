import os
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from tqdm import tqdm  # For progress bar

def generate_pwm_pattern(width, duty_cycle, frequency):
    """
    Generate a PWM pattern with multiple cycles.

    :param width: Width of the image or circle
    :param duty_cycle: Duty cycle of the PWM pattern (0 to 100)
    :param frequency: Frequency of the PWM pattern (number of cycles to show)
    :return: A 2D numpy array representing the PWM pattern
    """
    cycle_width = width // frequency
    duty_cycle_width = int(cycle_width * duty_cycle / 100)
    
    pwm_pattern = np.zeros(width, dtype=np.uint8)
    for i in range(frequency):
        start = i * cycle_width
        pwm_pattern[start:start + duty_cycle_width] = 255  # White stripes
    return pwm_pattern

def create_black_and_white_image(circle_position, circle_radius, duty_cycle, frequency, image_id):
    """
    Create an image with a black background, a white circle, and black vertical stripes 
    following a PWM pattern.

    :param circle_position: Tuple (x, y) for the circle center
    :param circle_radius: Radius of the circle
    :param duty_cycle: Duty cycle of the PWM pattern (0 to 100)
    :param frequency: Frequency of the PWM pattern (number of cycles to show)
    :param image_id: Unique identifier for the image file
    """
    # Step 1: Create a black background image (1080x1920) in vertical format
    width, height = 1080, 1920
    image = Image.new("RGB", (width, height), "black")

    # Step 2: Draw a white circle at the specified position with the specified radius
    draw = ImageDraw.Draw(image)
    left_up_point = (circle_position[0] - circle_radius, circle_position[1] - circle_radius)
    right_down_point = (circle_position[0] + circle_radius, circle_position[1] + circle_radius)
    draw.ellipse([left_up_point, right_down_point], fill="white")

    # Step 3: Generate PWM pattern and apply it to the circle
    pwm_pattern = generate_pwm_pattern(circle_radius * 2, duty_cycle, frequency)
    for x in range(circle_position[0] - circle_radius, circle_position[0] + circle_radius):
        for y in range(circle_position[1] - circle_radius, circle_position[1] + circle_radius):
            if (x - circle_position[0]) ** 2 + (y - circle_position[1]) ** 2 <= circle_radius ** 2:
                pwm_value = pwm_pattern[x - (circle_position[0] - circle_radius)]
                if pwm_value == 255:
                    # Ensure coordinates are within the image bounds
                    if 0 <= x < width and 0 <= y < height:
                        image.putpixel((x, y), (0, 0, 0))  # Draw black line

    # Step 4: Ensure the dataset directory exists
    dataset_dir = "dataset"
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    # Step 5: Save the image with a dynamic name based on circle parameters
    file_name = f"circle_{circle_radius}_{circle_position[0]}_{circle_position[1]}_{duty_cycle}_{frequency}_{image_id}.png"
    file_path = os.path.join(dataset_dir, file_name)
    image.save(file_path)

def create_dataset():
    """
    Create a dataset of images with varying parameters and save the dataset labels to a CSV file.
    """
    # Define ranges for parameters
    circle_positions = [(x, y) for x in range(300, 1081, 300) for y in range(300, 1921, 300)]
    circle_radii = range(50, 401, 50)  # Radii from 50 to 400 in steps of 50
    duty_cycles = range(10, 101, 10)  # Duty cycles from 10% to 100%
    frequencies = range(1, 11)  # Frequencies from 1 to 10

    # Prepare a list to collect CSV data
    csv_data = []

    # Create images and collect data with progress bar
    total_samples = len(circle_positions) * len(circle_radii) * len(duty_cycles) * len(frequencies)
    with tqdm(total=total_samples) as pbar:
        image_id = 0
        for circle_position in circle_positions:
            for circle_radius in circle_radii:
                for duty_cycle in duty_cycles:
                    for frequency in frequencies:
                        create_black_and_white_image(circle_position, circle_radius, duty_cycle, frequency, image_id)
                        csv_data.append({
                            'image_id': image_id,
                            'circle_position_x': circle_position[0],
                            'circle_position_y': circle_position[1],
                            'circle_radius': circle_radius,
                            'duty_cycle': duty_cycle,
                            'frequency': frequency
                        })
                        image_id += 1
                        pbar.update(1)

    # Save CSV file
    csv_file_path = os.path.join("dataset", "dataset_labels.csv")
    df = pd.DataFrame(csv_data)
    df.to_csv(csv_file_path, index=False)
    print(f"Dataset CSV file saved as '{csv_file_path}'.")