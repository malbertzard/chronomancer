import subprocess

def run_job(command):
    try:
        print(f"Running: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print("Output:\n", result.stdout)
        if result.stderr:
            print("Errors:\n", result.stderr)
    except Exception as e:
        print(f"Failed to run command: {e}")
