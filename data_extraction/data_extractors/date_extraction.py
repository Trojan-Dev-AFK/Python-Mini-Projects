"""
# Date Extraction

## Pre-requisite

Install dependencies from requirements file `pip install -r ./requirements.txt`

## Usage

date_extractor = DateExtractor()
date_results = date_extractor.get_dates('./example_data/output2/dates/')
print(date_results)
"""
import json

import cv2
import pytesseract
import os
import re
from dateutil.parser import parse, ParserError
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import warnings
import logging

# Suppress specific warnings from transformers
warnings.filterwarnings('ignore', message='Using the model-agnostic default `max_length`')


class DateExtractor:
    def __init__(self, model_path=None):
        self.logger = None
        self.setup_logging()
        self.model, self.processor = self.load_model(model_path)

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def load_model(model_path=None):
        if model_path and os.path.isdir(model_path):
            model = VisionEncoderDecoderModel.from_pretrained(model_path)
            processor = TrOCRProcessor.from_pretrained(model_path)
        else:
            model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
            processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
        return model, processor

    def preprocess_image(self, image_path):
        self.logger.debug(f"Preprocessing image: {image_path}")
        img = cv2.imread(image_path)
        if img is None:
            return None
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        return img

    @staticmethod
    def find_date_in_text(text):
        patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
            r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',
            r'\b\d{2,4}-\d{1,2}-\d{1,2}\b',
            r'\b\d{1,2} \d{1,2} \d{4}\b',
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',
            r'\b\d{1,2}(st|nd|rd|th)? (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    parsed_date = parse(match.group(), fuzzy=True)
                    parsed_date = parsed_date.strftime('%m-%d-%Y')
                    return parsed_date
                except ParserError:
                    continue
        return None

    def recognize_system_date_from_images(self, preprocessed_image):
        if preprocessed_image is not None:
            extracted_system_text = pytesseract.image_to_string(preprocessed_image, config='--oem 3 --psm 6')
            extracted_system_date = self.find_date_in_text(extracted_system_text)
            if extracted_system_date:
                return extracted_system_date
        return None

    def recognize_handwritten_date_from_images(self, image_path):
        preprocessed_pil_image = Image.open(image_path).convert("RGB")
        if preprocessed_pil_image is not None:
            pixel_values = self.processor(images=preprocessed_pil_image, return_tensors="pt").pixel_values
            generated_ids = self.model.generate(pixel_values)
            extracted_handwritten_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            extracted_handwritten_date = self.find_date_in_text(extracted_handwritten_text)
            if extracted_handwritten_date:
                return extracted_handwritten_date
        return None

    def get_dates(self, folder_path):
        result = {}

        for file_name in os.listdir(folder_path):
            if file_name.endswith('.jpg') or file_name.endswith('.jpeg') or file_name.endswith('.png'):
                full_file_path = os.path.join(folder_path, file_name)
                try:
                    preprocessed_image = self.preprocess_image(full_file_path)
                    if preprocessed_image is None:
                        continue

                    predicted_date = self.recognize_system_date_from_images(preprocessed_image)
                    if predicted_date:
                        result[file_name] = predicted_date
                    else:
                        predicted_date = self.recognize_handwritten_date_from_images(full_file_path)
                        if predicted_date:
                            result[file_name] = predicted_date
                        else:
                            result[file_name] = None

                    self.logger.info(f"File: {full_file_path} -> Extracted Date: {predicted_date}")
                except Exception as e:
                    self.logger.debug(f"Error processing {full_file_path}: {e}")
                    continue
        return result

    def save_results_to_json(self, results, output_file):
        self.logger.info(f"Saving results to JSON file: {output_file}")
        with open(output_file, 'w') as f:
            json.dump(results, f)
