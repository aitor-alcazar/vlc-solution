from src.image_generator import create_black_and_white_image

def main():
    print("Starting the image creation process...")

    # Example usage of the image creation function
    circle_position = (540, 960)  # Position of the circle (centered in the image)
    circle_radius = 200           # Radius of the circle
    duty_cycle = 50               # Duty cycle of the PWM pattern (0 to 100)
    frequency_hz = 200            # Frequency of the PWM pattern in Hz

    create_black_and_white_image(circle_position, circle_radius, duty_cycle, frequency_hz)

if __name__ == "__main__":
    main()
