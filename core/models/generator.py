import os

# Directory where the field files are stored
fields_dir = "fields"
init_file_path = os.path.join(fields_dir, "__init__.py")

# Ensure the output directory exists
os.makedirs(fields_dir, exist_ok=True)

# List all Python files in the fields directory, excluding __init__.py itself
field_files = [
    f for f in os.listdir(fields_dir) 
    if f.endswith(".py") and f != "__init__.py"
]

# Write the import statements to __init__.py
with open(init_file_path, "w") as init_file:
    for field_file in field_files:
        # Remove the .py extension to get the module name
        module_name = os.path.splitext(field_file)[0]
        # Convert snake_case file names to CamelCase class names
        class_name = ''.join(word.capitalize() for word in module_name.split('_'))
        class_name = class_name.replace("field", "Field")
        # Write the import statement
        init_file.write(f"from .{module_name} import {class_name}\n")
        print(class_name)

print(f"__init__.py generated successfully in '{fields_dir}' directory.")