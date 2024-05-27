"""
# Timestamp Extraction and verification

## Pre-requisite

Install dependencies from requirements file `pip install -r ./requirements.txt`

## Usage

timestamp_extractor = TimestampExtractor()
are_timestamps_same = timestamp_extractor.check_timestamp_is_same("./example_data/output3/timestamps/")
print(f"Are timestamps same: {are_timestamps_same}")
"""
import pytesseract
from PIL import Image
import re
from dateutil import parser
import os
import json


class TimestampChecker:
    def __init__(self):
        self.results = {}

    @staticmethod
    def get_date(img_path):
        try:
            img = Image.open(img_path)
            ocr_text = pytesseract.image_to_string(img)

            date_regexes = [
                r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b',  # e.g., 01/31/2024 or 1-1-23
                r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{2,4}\b',  # e.g., 1 Jan 2024
                r'\b\d{4}[./-]\d{2}[./-]\d{2}\b',  # e.g., 2024-01-31
                r'\b\d{2}/\d{2}/\d{4}\b',  # e.g., 31/01/2024
                r'\b\d{2}-\d{2}-\d{4}\b',  # e.g., 31-01-2024
                r'\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4} \d{1,2}:\d{2} (?:AM|PM)\b',  # e.g., 01/31/2024 12:30 PM
                r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b',  # e.g., 2024-01-31 12:30:45
                r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\b',  # e.g., 2024-01-31T12:30:45
                r'\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) '
                r'\d{4}\b',
                # e.g., January 31, 2024
                r'\b\d{8}\b',  # e.g., 20240131
                r'\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}\b',
                # e.g., Wed, 31 Jan 2024
                r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}\b',  # e.g., 2024-01-31 12:30:45+00:00
                r'\b\d{2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2}\b',  # e.g., 31 Jan 24
                r'\b\d{1,2}/\d{1,2}/\d{2}\b',  # e.g., 31/1/24
                r'\b\d{1,2}-\d{1,2}-\d{2}\b',  # e.g., 1/31/24
                r'\b\d{4}[.]\d{2}[.]\d{2}\b',  # e.g., 2024.01.31
                r'\b\d{2}-\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4}\b',  # e.g., 31-Jan-2024
                r'\b\d{2}-\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{2}\b',  # e.g., 31-Jan-24
            ]

            extracted_dates = []
            for regex in date_regexes:
                matches = re.findall(regex, ocr_text)
                for match in matches:
                    extracted_dates.append(match)

            parsed_dates = []
            for date_str in extracted_dates:
                try:
                    parsed_date = parser.parse(date_str, fuzzy=True)
                    parsed_dates.append(parsed_date)
                except ValueError:
                    pass

            formatted_dates = [date.strftime("%d %b %Y %H:%M:%S") for date in parsed_dates]
            if len(formatted_dates) > 1:
                # Handle duplicate entries
                formatted_dates = formatted_dates[-1]
            else:
                formatted_dates = formatted_dates[0]
            print(f"Date {img_path} -> Timestamp: {formatted_dates}")

            return formatted_dates if formatted_dates else None

        except Exception as e:
            return f"Error: {str(e)}"

    def extract_timestamps(self, folder_path):
        files = os.listdir(folder_path)
        for file in files:
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                image_path = os.path.join(folder_path, file)
                dates = self.get_date(image_path)
                self.results[file] = dates
        return self.results

    def check_timestamp_is_same(self, folder_path):
        results = self.extract_timestamps(folder_path)
        values = list(results.values())
        unique_values = set(tuple(v) for v in values if v is not None)
        return len(unique_values) == 1

    @staticmethod
    def save_results_to_json(results, output_file):
        print(f"Saving results to JSON file: {output_file}")
        with open(output_file, 'w') as f:
            json.dump(results, f)
