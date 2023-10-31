# pip install pyflakes

import pyflakes.api
import pyflakes.reporter
import sys

def check_dead_code(filename):
    # Create a PyFlakes checker
    checker = pyflakes.api.checkPath(filename)

    # Create a reporter to capture the results
    reporter = pyflakes.reporter.Reporter(checker)

    # Run the checker to analyze the code
    checker.messages.sort(key=lambda m: m.lineno)
    checker.report_messages(reporter)

    # Print any warnings or errors (potential dead code)
    for message in reporter.messages:
        print(f"Dead code at line {message.lineno}: {message.message}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dead_code_checker.py <python_file.py>")
        sys.exit(1)

    filename = sys.argv[1]
    check_dead_code(filename)


# Call it by running the command -> python dead_code_checker.py your_python_file.py

