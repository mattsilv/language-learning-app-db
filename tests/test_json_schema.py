import json
import fastjsonschema
import pytest
import os
import glob
from multiprocessing import Pool, cpu_count

# Load the schema and compile it using fastjsonschema
def load_and_compile_schema():
    with open(os.path.join(os.path.dirname(__file__), '../data-dictionary.json')) as schema_file:
        schema = json.load(schema_file)
    return fastjsonschema.compile(schema)

validate_json_schema = load_and_compile_schema()

# Function to validate a single JSON file
def validate_json(filepath):
    try:
        with open(filepath) as json_file:
            data = json.load(json_file)
        validate_json_schema(data)
        return (filepath, None)
    except fastjsonschema.JsonSchemaException as err:
        return (filepath, f"JSON validation error in {filepath}: {err.message}")

# Function to load and validate JSON files in parallel
def test_json_validation():
    errors = []
    files_to_check = glob.glob('**/*lesson*.json', recursive=True)
    
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(validate_json, files_to_check)
    
    for filepath, error in results:
        if error:
            errors.append(error)
        else:
            print(f"{filepath} is valid.")
    
    if errors:
        for error in errors:
            print(error)
        pytest.fail("JSON validation errors occurred. See log for details.")

if __name__ == "__main__":
    pytest.main()
