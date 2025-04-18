import os
import re
import sys

def detect_and_update_requirements():
    project_name = os.path.basename(os.getcwd())
    py_files = []

    # Collect all Python files
    for root, _, files in os.walk(project_name):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))

    # Extract imported modules
    imports = set()
    for file in py_files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                match = re.match(r'^(?:import|from) (\w+)', line)  # FIXED: Using raw string
                if match:
                    module = match.group(1)
                    # Ignore built-in modules
                    if module not in sys.builtin_module_names:
                        imports.add(module)

    # Read existing requirements
    existing_reqs = set()
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            existing_reqs = set(line.strip() for line in f)

    # Update requirements.txt if needed
    new_reqs = imports - existing_reqs
    if new_reqs:
        with open("requirements.txt", "a") as f:
            for req in new_reqs:
                f.write(f"{req}\n")
        print(f"✅ Added new dependencies: {', '.join(new_reqs)}")
    else:
        print("✅ No new dependencies detected.")

if __name__ == "__main__":
    detect_and_update_requirements()
