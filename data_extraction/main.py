from date_extraction import DateExtractor


if __name__ == "__main__":
    date_extractor = DateExtractor()
    results = date_extractor.get_dates('./example_data/output2/dates/')
    print(results)
