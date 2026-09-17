from pathlib import Path

home_dir = Path.home()

# Navigate directly into the Documents folder using the '/' operator
documents_dir = home_dir / "Documents"

print(f"Current Target Path: {documents_dir}")

# Check if the folder exists
if documents_dir.exists():
    # Iterate through and list files inside Documents
    for file in documents_dir.iterdir():
        if file.is_file():
            print(f"Found file: {file.name}")


# Get the directory where this script is located
current_dir = Path(__file__).resolve().parent

# Find all .py files in that directory
# Use current_dir.rglob("*.py") instead if you want to search subdirectories too
py_files = list(current_dir.glob("*.py"))

# Print every file found except this specific script
for file in py_files:
    if file != Path(__file__).resolve():
        print(file.name)
