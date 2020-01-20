# project-liberation
This application is CodePoets home page.

## Software requirements
   - Python >= 3.7.6
   - Django >= 2.2.8
   - npm >= 6.7.0
   - PostgreSQL >= 10

## Development setup

### Preparing your environment for development

1.  Install `node_modules`. In project directory:
    ```
    $ npm install
    ```

1.  Install pipenv on your machine. Do not create any virtualenv, just install pipenv globally on your operation system:

    Arch:
    ```
    $ sudo pacman -Syu python-pipenv
    ```

    Debian:
    ```
    $ sudo apt install pipenv
    ```

1.  Create new virtual environment for project with all development packages.
    ```
    $ pipenv install --dev
    ```

1.  Activate newly created virtualenv:
    ```
    $ pipenv shell
    ```

1.  Create local settings in `project_liberation/settings/local_settings.py`.
    ```python
    from .development import *
    ```
    For more details please see description in `project_liberation/settings/__init__`


1.  Create database for application:
    ```
    $ createdb -U postgres project_liberation
    ```

### Running tests and code analysis

You can run automated tests and code analysis with:
```
$ ./full_check.sh
```
For details please see `full_check.py` file.
