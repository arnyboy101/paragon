import subprocess
import sys
import os

def generate_requirements(script_path):
    # Ensure the script path is absolute
    script_path = os.path.abspath(script_path)

    # Get the directory containing the script
    script_directory = os.path.dirname(script_path)

    # Run pipdeptree to generate a tree of dependencies
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pipdeptree'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=script_directory,
            check=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running pipdeptree: {e.stderr}")
        sys.exit(1)

    # Parse the output to extract dependencies
    dependencies = set()
    for line in result.stdout.split('\n'):
        if not line.startswith(' '):
            # Lines starting with a space are not package names
            package_name = line.split('==')[0].strip()
            if package_name:
                dependencies.add(package_name)

    # Write the dependencies to requirements.txt
    requirements_file = os.path.join(script_directory, 'requirements.txt')
    with open(requirements_file, 'w') as file:
        file.write('\n'.join(sorted(dependencies)))

    print(f"Requirements file generated at: {requirements_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_requirements.py your_script.py")
        sys.exit(1)

    script_path = sys.argv[1]
    if not os.path.isfile(script_path):
        print(f"Error: {script_path} does not exist.")
        sys.exit(1)

    generate_requirements(script_path)
