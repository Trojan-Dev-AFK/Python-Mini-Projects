"""
# Signature Detection

## Pre-requisite

Install dependencies from requirements file `pip install -r ./requirements.txt`

## Usage

signature_detector = SignatureDetector('./output_models/best_signature_vs_text_model.h5')
signature_results = signature_detector.process_images('./example_data/output3/timestamps/')
print(signature_results)
"""
import json
import os
import cv2
import numpy as np
import logging
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array


class SignatureDetector:
    def __init__(self, model_path):
        self.logger = None
        self.setup_logging()
        self.model = self.load_model_for_inference(model_path)

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def load_model_for_inference(self, model_path):
        self.logger.info(f"Loading model from {model_path}")
        return load_model(model_path)

    def preprocess_image(self, image_path):
        self.logger.debug(f"Preprocessing image: {image_path}")
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image not found: {image_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
        image = cv2.resize(image, (64, 64))
        image = img_to_array(image) / 255.0
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        return image

    def predict_signature(self, image_path):
        image = self.preprocess_image(image_path)
        prediction = self.model.predict(image)
        return bool(prediction[0] > 0.5)

    def process_images(self, base_dir):
        results = {}
        self.logger.info(f"Processing images in directory: {base_dir}")
        for filename in os.listdir(base_dir):
            if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                image_path = os.path.join(base_dir, filename)
                try:
                    prediction = self.predict_signature(image_path)
                    self.logger.info(f"Filename: {filename} -> Signature: {prediction}")
                    results[filename] = prediction
                except ValueError as e:
                    self.logger.error(e)
                    continue
        return results

    def save_results_to_json(self, results, output_file):
        self.logger.info(f"Saving results to JSON file: {output_file}")
        with open(output_file, 'w') as f:
            json.dump(results, f)
