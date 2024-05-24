import json
import jsonschema
from jsonschema import validate
import pytest
import os
import glob
from multiprocessing import Pool, cpu_count

# Load the schema
def load_schema():
    with open(os.path.join(os.path.dirname(__file__), '../data-dictionary.json')) as schema_file:
        return json.load(schema_file)

schema = load_schema()

# Function to validate a single JSON file
def validate_json(filepath):
    try:
        with open(filepath) as json_file:
            data = json.load(json_file)
        validate(instance=data, schema=schema)
        return (filepath, None)
    except jsonschema.exceptions.ValidationError as err:
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
