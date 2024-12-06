import subprocess

# Path to Krita executable (adjust according to your OS)
krita_path = "C:/Program Files/Krita (x64)/bin/krita.exe"  # Windows example
# krita_path = "/usr/bin/krita"  # Linux example

# Path to your Krita Python script
script_path = "C:/users/stevent/learning_krita.py"

# Build the command to run Krita with the Python script
#command = [krita_path, '--nosplash', '--pyfile', script_path]
command = [krita_path, '--nosplash', '--script', script_path]

try:
    # Run the command and capture output and errors
    process = subprocess.run(command, capture_output=True, text=True, check=True)

    # Get the output and errors from the Krita process
    output = process.stdout
    errors = process.stderr
    print("Standard Output:", process.stdout)
  

    # Check if there is any output from the script
    if output:
        print("Krita Script Output:\n", output)

    # Check if there are any errors
    if errors:
        print("Krita Script Errors:\n", errors)

    # Check the return code to determine success or failure
    if process.returncode == 0:
        print("Krita script executed successfully.")
    else:
        print(f"Krita script failed with return code: {process.returncode}")

except subprocess.CalledProcessError as e:
    print(f"Error while running Krita script: {e.stderr}")
