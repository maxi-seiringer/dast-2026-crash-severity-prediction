import json
import os

# File names
requirements_file = "requirements.txt"
codemeta_file = "codemeta.json"

dependencies = []
if os.path.exists(requirements_file):
    with open(requirements_file, 'r') as req_file:
        for line in req_file:
            line = line.strip()
            # Ignore comments and empty lines
            if line and not line.startswith('#'):
                dependencies.append(line)
else:
    print(f"Error: {requirements_file} not found. Please generate your dependencies first.")
    exit(1)


with open(codemeta_file, 'r', encoding='utf-8') as json_file:
    codemeta_data = json.load(json_file)


codemeta_data["softwareRequirements"] = dependencies

with open(codemeta_file, 'w', encoding='utf-8') as json_file:
    json.dump(codemeta_data, json_file, indent=2, ensure_ascii=False)

print(f"Success: {len(dependencies)} dependencies injected into {codemeta_file}.")