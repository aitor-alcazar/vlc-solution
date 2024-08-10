import os
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Force TensorFlow to use CPU only
tf.config.set_visible_devices([], 'GPU')

def load_data(csv_file_path, image_dir):
    """
    Load the dataset from CSV and image files.

    :param csv_file_path: Path to the CSV file with labels
    :param image_dir: Directory where images are stored
    :return: Features and labels arrays
    """
    df = pd.read_csv(csv_file_path)
    
    # Load images and extract features
    X = []
    y = []
    for index, row in df.iterrows():
        image_path = os.path.join(image_dir, f"circle_{row['circle_radius']}_{row['circle_position_x']}_{row['circle_position_y']}_{row['duty_cycle']}_{row['frequency']}_{row['image_id']}.png")
        if os.path.exists(image_path):
            image = tf.keras.preprocessing.image.load_img(image_path, color_mode='grayscale', target_size=(1080, 1920))
            image_array = tf.keras.preprocessing.image.img_to_array(image)
            X.append(image_array.flatten())  # Flatten image to 1D array
            y.append([
                row['circle_radius'],
                row['frequency'],
                row['circle_position_x'],
                row['circle_position_y']
            ])
    return np.array(X), np.array(y)

def build_model(input_shape):
    """
    Build a simple neural network model.

    :param input_shape: Shape of the input features
    :return: Compiled Keras model
    """
    model = Sequential([
        Dense(128, activation='relu', input_shape=input_shape),
        Dense(64, activation='relu'),
        Dense(4)  # 4 outputs: radius, frequency, position_x, position_y
    ])
    
    model.compile(optimizer=Adam(), loss='mse', metrics=['mae'])
    return model

def train_model():
    """
    Train the neural network model.
    """
    csv_file_path = 'dataset/dataset_labels.csv'
    image_dir = 'dataset'
    
    # Load and prepare data
    X, y = load_data(csv_file_path, image_dir)
    
    # Normalize data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    # Split the data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = build_model((X_train.shape[1],))
    
    history = model.fit(
        X_train, y_train,
        epochs=10,
        batch_size=32,
        validation_data=(X_val, y_val),
        verbose=1
    )
    
    # Save the model
    model.save('circle_classifier_model.h5')
    print("Model trained and saved as 'circle_classifier_model.h5'.")

def test_model(model_file_path):
    """
    Test the trained model with the dataset.

    :param model_file_path: Path to the trained model file
    """
    # Load the model
    model = tf.keras.models.load_model(model_file_path)

    csv_file_path = 'dataset/dataset_labels.csv'
    image_dir = 'dataset'
    
    # Load images and extract features
    X, y = load_data(csv_file_path, image_dir)
    
    # Normalize data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    # Predict using the trained model
    predictions = model.predict(X)
    
    # Display or process predictions
    print("Sample predictions:")
    for i, prediction in enumerate(predictions[:5]):  # Show first 5 predictions
        print(f"Image {i}: Predicted - Radius: {prediction[0]}, Frequency: {prediction[1]}, Position X: {prediction[2]}, Position Y: {prediction[3]}")
