from src.image_generator import create_black_and_white_image

def main():
    print("Starting the image creation process...")

    # Example usage of the image creation function
    circle_position = (540, 960)  # Position of the circle (centered in the image)
    circle_radius = 200           # Radius of the circle

    create_black_and_white_image(circle_position, circle_radius)

if __name__ == "__main__":
    main()
