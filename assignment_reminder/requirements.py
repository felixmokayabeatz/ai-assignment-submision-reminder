import os
import subprocess

def generate_requirements(requirements_file, requirements_no_version_file):
    subprocess.run(['pip', 'freeze'], stdout=open(requirements_file, 'w'))

    with open(requirements_no_version_file, 'w') as no_version_file:
        freeze_output = subprocess.check_output(['pip', 'freeze']).decode('utf-8')
        for line in freeze_output.splitlines():
            package_name = line.split('==')[0]
            no_version_file.write(package_name + '\n')

    print('Requirements files generated successfully.')

def install_requirements(requirements_file):
    print(f'Installing packages from {requirements_file}...')
    subprocess.run(['pip', 'install', '-r', requirements_file])
    print('Packages installed successfully.')

def main():
    requirements_dir = os.path.join(os.getcwd(), 'requirements_files')
    if not os.path.exists(requirements_dir):
        os.makedirs(requirements_dir)

    requirements_file = os.path.join(requirements_dir, 'requirements.txt')
    requirements_no_version_file = os.path.join(requirements_dir, 'requirements_no_version.txt')

    print('What would you like to do?')
    print('1. Create requirements files')
    print('2. Install packages from requirements files')
    
    choice = input('Enter the number (1 or 2): ').strip()

    if choice == '1':
        print('Generating requirements files...')
        generate_requirements(requirements_file, requirements_no_version_file)
        
    elif choice == '2':
        print('Which requirements file do you want to install from?')
        print('1. requirements.txt (with versions)')
        print('2. requirements_no_version.txt (without versions)')

        install_choice = input('Enter the number (1 or 2): ').strip()

        if install_choice == '1':
            install_requirements(requirements_file)
        elif install_choice == '2':
            install_requirements(requirements_no_version_file)
        else:
            print('Invalid choice. Exiting.')
    else:
        print('Invalid choice. Exiting.')

if __name__ == '__main__':
    main()
