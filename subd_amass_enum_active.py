import sys
import re
import subprocess
import time
import os

def clean_output(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        line = line.strip()
        parts = line.split(' ', 6)
        if len(parts) > 5:
            cleaned_line = parts[5].strip()
            if re.match(r'\d+\.\d+\.\d+\.\d+/\d+', cleaned_line):
                cleaned_lines.append(cleaned_line)
            elif re.search(r'\.', cleaned_line):
                if cleaned_line.split('.', 1)[1]:
                    cleaned_lines.append(cleaned_line)
        else:
            if '.' in line:
                cleaned_lines.append(line)

    with open(output_file, 'w') as f:
        f.write('\n'.join(sorted(cleaned_lines)))

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 subd_amass_enum_active.py <url> -t <time_in_minutes>")
        sys.exit(1)

    url = sys.argv[1]
    if url.startswith('http://') or url.startswith('https://'):
        url = url.split('://')[1]

    for i in range(2, len(sys.argv)):
        if sys.argv[i] == '-t':
            timer = int(sys.argv[i+1])
            break
        else:
            print("Invalid command-line argument: " + sys.argv[i])
            sys.exit(1)

    output_file = f"subd_amass_enum_active_{url}.txt"

    start_time = time.time()
    process = subprocess.Popen(['amass', 'enum', '-active', '-d', url, '-o', 'subd_amass_enum_active_temp.txt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        if time.time() - start_time > timer * 60:
            process.terminate()
            break

    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error: {error.decode('utf-8')}")

    clean_output('subd_amass_enum_active_temp.txt', output_file)

    # Delete the temporary file when all process is over
    os.remove('subd_amass_enum_active_temp.txt')

if __name__ == '__main__':
    main()