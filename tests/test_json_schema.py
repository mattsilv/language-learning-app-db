import json
import jsonschema
from jsonschema import validate
import pytest
import os
import glob

# Load the schema
with open(os.path.join(os.path.dirname(__file__), '../data-dictionary.json')) as schema_file:
    schema = json.load(schema_file)

# Function to load JSON files with "lesson" in their name and validate against the schema
def test_json_validation():
    errors = []
    for filepath in glob.glob('**/*lesson*.json', recursive=True):
        with open(filepath) as json_file:
            data = json.load(json_file)
        
        # Validate the JSON file against the schema
        try:
            validate(instance=data, schema=schema)
            print(f"{filepath} is valid.")
        except jsonschema.exceptions.ValidationError as err:
            errors.append(f"JSON validation error in {filepath}: {err.message}")

    if errors:
        for error in errors:
            print(error)
        pytest.fail("JSON validation errors occurred. See log for details.")

if __name__ == "__main__":
    pytest.main()
