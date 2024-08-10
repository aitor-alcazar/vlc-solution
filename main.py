import os
from src.image_generator import create_dataset

def main():
    csv_file_path = os.path.join("dataset", "dataset_labels.csv")
    if not os.path.exists(csv_file_path):
        print("CSV file not found. Creating dataset...")
        create_dataset()
    else:
        print("CSV file already exists. Skipping dataset creation.")

if __name__ == "__main__":
    main()
