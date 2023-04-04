# Utils
[![Python 3.6](https://img.shields.io/badge/Python-3.7-blue)](https://www.python.org/downloads/release/python-370/)
[![Python 3.6](https://img.shields.io/badge/Python-3.8-blue)](https://www.python.org/downloads/release/python-380/)
[![Python 3.6](https://img.shields.io/badge/Python-3.9-blue)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/downloads/release/python-3100/)

## Installing
- Note: update `PACKAGE` to the appropriate package being installed

  | Package Name      | Subdirectory |
  | ----------------- | ------------ |
  | SB Utils          | root         |
  | SB Utils.Actuator | actuator     |
  | OSQuery ORM       | osquery_orm  |

### On a standalone System via pip
- Install requires Python 3.7+ and pip

- Install via pip
    ```bash
    pip install git+https://github.com/ScreamBun/SB_utils.git#subdirectory=PACKAGE
    ```

- To update if already installed
    ```bash
    pip install --update git+https://github.com/ScreamBun/SB_utils.git#subdirectory=PACKAGE
    ```

### On a standalone System via requirements
- Install requires Python 3.5+ and pip

- Installing via requirements.txt
    - Add `PACKAGE_NAME@git+https://github.com/ScreamBun/SB_utils.git#subdirectory=PACKAGE` to the requirements file.
