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
    for filepath in glob.glob('**/*lesson*.json', recursive=True):
        with open(filepath) as json_file:
            data = json.load(json_file)
        
        # Validate the JSON file against the schema
        try:
            validate(instance=data, schema=schema)
            print(f"{filepath} is valid.")
        except jsonschema.exceptions.ValidationError as err:
            pytest.fail(f"JSON validation error in {filepath}: {err.message}")

if __name__ == "__main__":
    pytest.main()
