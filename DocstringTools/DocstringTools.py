import ast
from DocstringValidity import is_docstring_valid as DocstringValidityCheck

def has_docstring(node):
    """
    Check if a function or method node has a docstring.
    """
    return isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str)

def should_check(name, check_rules):
    """
    Determine whether to check a method based on its name and the check_rules.
    """
    if name.startswith('__') and name.endswith('__'):
        if check_rules["check_dunder"] is False:
            return False
        else:
            return True
    if name.startswith('__'):
        if check_rules["check_private"] is False:
            return False
        else:
            return True
    if name.startswith('_') and not name.startswith('__'):
        if check_rules["check_protected"] is False:
            return False
        else:
            return True
    return True

def check_docstrings(filename, check_rules=None):
    if check_rules is None:
        check_rules = {'check_dunder': True, 'check_private': True, 'check_protected': True}

    with open(filename, "r") as file:
        source = file.read()

    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and should_check(node.name, check_rules):
            if has_docstring(node):
                if not DocstringValidityCheck(node):
                    # All the errors are handled inside DocstringValidityCheck
                    pass
            else:
                print(f"E100: Docstring missing for '{node.name}' in '{filename}' at line {node.lineno}")


if __name__ == "__main__":
    check_rules = {'check_dunder': True, 'check_private': True, 'check_protected': True}
    check_docstrings('SampleFile.py', check_rules)
