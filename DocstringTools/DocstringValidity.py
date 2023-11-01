import ast
import re

def is_docstring_valid(func_node):

    errors = []
    docstring = ast.get_docstring(func_node)
    
    if docstring:
        lines = docstring.split('\n')
        # Check if any line in the docstring exceeds 120 characters
        for i, line in enumerate(lines, start=1):
            if len(line) > 120:
                errors.append(f"E105: Line {i} in docstring of function '{func_node.name}' at line {func_node.lineno} exceeds 120 characters.")
                # return False
            
        # Checking if the docstring has a summary        
        if not lines[0].strip():
            errors.append(f"E101: Missing summary in docstring of function '{func_node.name}' at line {func_node.lineno}")
            # return False
        
        # Checking if parameters are documented
        params_in_doc = {match.group(1) for match in re.finditer(r":param (\w+):", docstring)}
        params_in_def = {arg.arg for arg in func_node.args.args if arg.arg != 'self'}
        if params_in_def != params_in_doc:
            errors.append(f"E102: Parameters mismatch in docstring of function '{func_node.name}' at line {func_node.lineno}")
            # return False
        
        # Checking if return is documented (if the function returns something)
        if func_node.returns is not None:
            if ':return:' not in docstring:
                errors.append(f"E103: Return not documented in function '{func_node.name}' at line {func_node.lineno}")
                # return False
                
        # Check if exceptions are raised and documented with exception names
        exceptions_raised = set()
        for node in ast.walk(func_node):
            if isinstance(node, ast.Raise) and node.exc:
                exc_type = node.exc
                if isinstance(exc_type, ast.Call):
                    exc_type = exc_type.func
                if isinstance(exc_type, ast.Name):
                    exceptions_raised.add(exc_type.id)
                    
        exceptions_documented = set(re.findall(r":raises (\w+):", docstring))
        
        if exceptions_raised != exceptions_documented:
            errors.append(f"E104: Exception names mismatch in function '{func_node.name}' at line {func_node.lineno}")
            # return False

        # Check for an empty line after the summary [Only handle one line summary]
        if len(lines) > 1 and lines[1].strip():
            errors.append(f"E106: No empty line after the summary in docstring of function '{func_node.name}' at line {func_node.lineno}.")
            # return False

        # Check for an empty line after the summary [Handles multi-line summary. But doesnt recognize if there is no empty line before :param and takes it as summary]
        # summary_end = next((i for i, line in enumerate(lines) if not line.strip()), None)
        # if summary_end is None or (summary_end + 1 < len(lines) and not lines[summary_end + 1].strip()):
        #     errors.append(f"No empty line after the summary in docstring of function '{func_node.name}' at line {func_node.lineno}.")
            # return False
        
        # Check for empty lines after summary, parameters, and return sections
        sections = [":param", ":return:", ":raises:"]
        for section in sections:
            indices = [i for i, line in enumerate(lines) if section in line]
            if indices:
                last_index = indices[-1]
                if last_index + 1 >= len(lines) or lines[last_index + 1].strip():
                    errors.append(f"E106: No empty line after '{section}' section in docstring of function '{func_node.name}' at line {func_node.lineno}.")
                    # return False
                
    else:
        errors.append(f"Missing docstring in function '{func_node.name}' at line {func_node.lineno}")
        # return False
        
    for error in errors:
        print(error)
    
    return not errors
