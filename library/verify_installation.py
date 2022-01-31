"""
Check if the python environment has the libraries correctly installed

Author: Antonio Barbosa
E-mail: cunha.barbosa@gmail.com
Version: 2022-01-31

HELP:
Generate requirements.txt file for any project based on imports
https://github.com/bndr/pipreqs
> pipreqs --encoding=utf8 --force --print

Check packages installed in environment
> pip freeze
"""
import pkg_resources


def check_dependencies(dependencies: list) -> None:
    """ Verifies that the work environment has all installed libraries to the proper functioning """
    # dependencies can be any iterable with strings,
    # e.g. file line-by-line iterator
    # dependencies = {
    #     'selenium==3.141.0',
    #     'holidays==0.11.2',
    #     'python-telegram-bot==13.7'
    # }

    try:
        print(pkg_resources.require(dependencies))
        print("All project dependencies were correctly installed!\n")
        # input("Press any key to continue ...")
    except pkg_resources.VersionConflict as version_error:
        print("The following modules caused an error:")
        print("Version installed :", version_error.dist)
        print("Version required  :", version_error.req)
        exit()
    except pkg_resources.DistributionNotFound as error:
        print(error)
        exit(-1)


if __name__ == '__main__':
    requirements_filename = 'requirements.txt'
    requirements_dependencies = []
    try:
        with open(requirements_filename) as my_file:
            for line in my_file:
                if not line.startswith('#'):                        # Ignore comments
                    requirements_dependencies.append(line.strip())  # Strip \n (carriage return)
    except FileNotFoundError as requirements_error:
        print(requirements_error)
        print("Using the default values!!! \n")

        requirements_dependencies = {
            'pykeepass == 4.0.1',
            'python - telegram - bot == 13.10',
            'pywin32 == 303'
        }
    except Exception as requirements_error:
        print(requirements_error)
        exit(-1)

    check_dependencies(requirements_dependencies)
