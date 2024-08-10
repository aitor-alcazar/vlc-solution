import os
from src.image_generator import create_dataset
from src.ai_model import train_model, test_model

def main():
    # Paths
    csv_file_path = os.path.join("dataset", "dataset_labels.csv")
    model_file_path = 'circle_classifier_model.h5'
    
    # Check if CSV file exists and create dataset if not
    if not os.path.exists(csv_file_path):
        print("CSV file not found. Creating dataset...")
        create_dataset()
    else:
        print("CSV file already exists. Skipping dataset creation.")
    
    # Check if model exists and train if not
    if not os.path.exists(model_file_path):
        print("Model file not found. Training model...")
        train_model()  # Train the model and save it
    else:
        print("Model file already exists. Skipping model training.")
    
    # Test the model
    if os.path.exists(model_file_path):
        print("Loading and testing the model...")
        test_model(model_file_path)

if __name__ == "__main__":
    main()
