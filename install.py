import subprocess
import sys
import pkg_resources
import os

def install_dependencies():
    # Check if Python and pip are installed
    try:
        python_version = subprocess.check_output(['python', '--version'])
        pip_version = subprocess.check_output(['pip', '--version'])
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Python and pip are installed.")
        sys.exit(1)

    # Read requirements.txt and install packages
    try:
        # check if requirements.txt exists and continue if it doesn't
        if not os.path.exists('requirements.txt'):
            print("requirements.txt does not exist.")
            return
        
        with open('requirements.txt', 'r') as f:
            required_packages = f.read().splitlines()

        installed_packages = {pkg.key for pkg in pkg_resources.working_set}
        to_install = [pkg for pkg in required_packages if pkg.split('==')[0].lower() not in installed_packages]
        print('Installed packages:', installed_packages)
        print('Required packages:', required_packages)
        print('To install:', to_install)

        if to_install:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *to_install])
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to install one or more packages.")
        sys.exit(1)

if __name__ == '__main__':
    install_dependencies()