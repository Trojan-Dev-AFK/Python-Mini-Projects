from data_extractors.date_extraction import DateExtractor
from data_extractors.signature_detection import SignatureDetector
from data_extractors.timestamp_extraction import TimestampExtractor


def main():

    # Date Extraction
    date_extractor = DateExtractor()
    date_results = date_extractor.extract_dates('./example_data/output2/dates/')
    # Save the results to a JSON file
    output_file = './output_json/date_results.json'
    date_extractor.save_results_to_json(date_results, output_file)
    print(date_results)

    # Signature Detection
    signature_detector = SignatureDetector('./output_models/best_signature_vs_text_model.h5')
    signature_results = signature_detector.detect_signatures('./example_data/output3/signs/')
    # Save the results to a JSON file
    output_file = './output_json/signature_results.json'
    signature_detector.save_results_to_json(signature_results, output_file)
    print(signature_results)

    # Timestamp Extraction
    timestamp_extractor = TimestampExtractor()
    are_timestamps_same = timestamp_extractor.check_timestamp_is_same("./example_data/output3/timestamps/")
    print(f"Are timestamps same: {are_timestamps_same}")


if __name__ == "__main__":
    main()
