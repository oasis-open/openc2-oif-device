# Utils

## Installing
- Note: update `PACKAGE` to the appropriate package being installed
  - sb_utils-->root
  - sb_utils.actuator-->actuator

### On a standalone System via pip
- Install requires Python 3.7+ and pip

- Install via pip
    - Base package
    ```bash
    pip install git+https://github.com/ScreamBun/SB_utils.git#subdirectory=RACKAGE
    ```

- To update if already installed
    ```bash
    pip install --update git+https://github.com/ScreamBun/SB_utils.git#subdirectory=PACKAGE
    ```

### On a standalone System via requirements
- Install requires Python 3.7+ and pip

- Installing via requirements.txt
    - Add `SB-Utils@git+https://github.com/ScreamBun/SB_utils.git#subdirectory=PACKAGE` to the requirements file