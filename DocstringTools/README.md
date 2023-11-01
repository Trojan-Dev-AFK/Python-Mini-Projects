# DocstringTool:

This tool is used to verify if the docstrings of methods are in the correct format.

The format of a correct docstring is as below,

        def is_valid(self, name, age) -> bool:
            """
            Method to check if age is valid for a particular person
            
            :param name: Name of the person
            :param age: Age of the person

            :return: true or false
            
            :raises ValueError: if age is wrong
            """

## Basic Checks:

- Should take a dictionary as input with three rules. If a dictionary is not passed the default values for that dictionary will be used.
    `check_rules = {'check_dunder': True, 'check_private': True, 'check_protected': True}`
    - check_dunder (default: True) -> Check dunder (magic) methods [e.g. __init__(), __repr__(), etc...]
    - check_private (default: True) -> Check private methods [e.g __is_valid(), __is_present(), etc...]
    - check_protected (default: True) -> Check protected methods [e.g. _check_age(), _check_line_length(), etc...]
- Should check if a docstring is present
    - Raise error code [E100]
- Should check if a summary is present
    - Raise error code [E101]
- Should check if all the parameters are documented except 'self'
    - Raise error code [E102]
- Should check if return is documented
    - Raise error code [E103]
- Should check if the raised error is documented
    - Raise error code [E104]
- Should check if the length of a line is exceeding 120 characters
    - Raise error code [E105]
- Should check if there is an empty line after each section. The sections are [Summary, :param:, :return:, :raises:]
    - Raise error code [E106]
