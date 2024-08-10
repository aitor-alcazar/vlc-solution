import os
import numpy as np
from PIL import Image, ImageDraw

def generate_pwm_pattern(width, duty_cycle, frequency):
    """
    Generate a PWM pattern with multiple cycles.

    :param width: Width of the image or circle
    :param duty_cycle: Duty cycle of the PWM pattern (0 to 100)
    :param frequency: Frequency of the PWM pattern (number of cycles to show)
    :return: A 2D numpy array representing the PWM pattern
    """
    # Calculate the width of one cycle
    cycle_width = width // frequency
    duty_cycle_width = int(cycle_width * duty_cycle / 100)
    
    pwm_pattern = np.zeros(width, dtype=np.uint8)
    for i in range(frequency):
        start = i * cycle_width
        pwm_pattern[start:start + duty_cycle_width] = 255  # White stripes
    return pwm_pattern

def create_black_and_white_image(circle_position, circle_radius, duty_cycle, frequency):
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

    # Step 3: Generate PWM pattern and apply it to the circle
    pwm_pattern = generate_pwm_pattern(circle_radius * 2, duty_cycle, frequency)
    for x in range(circle_position[0] - circle_radius, circle_position[0] + circle_radius):
        for y in range(circle_position[1] - circle_radius, circle_position[1] + circle_radius):
            if (x - circle_position[0]) ** 2 + (y - circle_position[1]) ** 2 <= circle_radius ** 2:
                pwm_value = pwm_pattern[x - (circle_position[0] - circle_radius)]
                if pwm_value == 255:
                    image.putpixel((x, y), (0, 0, 0))  # Draw black line

    # Step 4: Ensure the dataset directory exists
    dataset_dir = "dataset"
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
        print(f"Step 4: Created directory '{dataset_dir}'.")

    # Step 5: Save the image with a dynamic name based on circle parameters
    file_name = f"circle_{circle_radius}_{circle_position[0]}_{circle_position[1]}_{duty_cycle}_{frequency}.png"
    file_path = os.path.join(dataset_dir, file_name)
    image.save(file_path)
    print(f"Step 5: Saved the image as '{file_path}'.")
