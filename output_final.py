import os
import re
import shutil
import sys

# Check if a filename was provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python3 output_final.py <name>")
    sys.exit(1)

filename = sys.argv[1]

# Set the directory path for the cores folder
cores_dir = 'cores'

# Set the directory path for the script
script_dir = os.path.dirname(__file__)

# Create a new directory with the same name as the script's name
directory_name = os.path.splitext(filename)[0]
new_dir = os.path.join(script_dir, directory_name)
os.mkdir(new_dir)

# Initialize an empty list to store the contents of all .txt files
all_text = []

# Loop through all files in the new directory
for file in os.listdir(cores_dir):
    if file.endswith('.txt'):
        # Open the file and read its contents
        with open(os.path.join(cores_dir, file), 'r') as f:
            file_text = f.read()
            # Clean the text by removing special characters, punctuation, and converting to lowercase
            cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', file_text).lower()
            # Add the cleaned text to the list
            all_text.append(cleaned_text)

# Join all the cleaned text into a single string, separating each word with a new line
merged_text = '\n'.join(set(all_text))

# Write the merged text to a file with the same name as the input filename
with open(os.path.join(new_dir, filename + '.txt'), 'w') as f:
    f.write(merged_text)

# Move the final file to the tools directory
shutil.move(os.path.join(new_dir, filename + '.txt'), os.path.join(new_dir, filename + '.txt'))

# Delete all .txt files in the cores directory
for filename in os.listdir(cores_dir):
    if filename.endswith('.txt'):
        os.remove(os.path.join(cores_dir, filename))