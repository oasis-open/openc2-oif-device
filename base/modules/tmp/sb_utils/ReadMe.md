# Utils

## Installing
### On a standalone System via pip
- Install requires Python 3.6+ and pip

- Install via pip
    - Base package
    ```bash
    pip install git+https://github.com/ScreamBun/SB_utils.git#subdirectory=root
    ```
  
    - Actuator package
    ```bash
    pip install git+https://github.com/ScreamBun/SB_utils.git#subdirectory=root
    pip install git+https://github.com/ScreamBun/SB_utils.git#subdirectory=actuator
    ```

- To update if already installed
    - Base package
    ```bash
    pip install --update git+https://github.com/ScreamBun/SB_utils.git#subdirectory=root
    ```
  
    - Actuator package
    ```bash
    pip install --update git+https://github.com/ScreamBun/SB_utils.git#subdirectory=root
    pip install --update git+https://github.com/ScreamBun/SB_utils.git#subdirectory=actuator
    ```

### On a standalone System via submodule source
- Install requires Python 3.6+ and pip

- Add the submodule to the repo
    - Add `--branch=BRANCH` to use a branch instead of master
    - DIR - the directory to add the submodule to, recommended to use `./module/NAME`
    - After adding a submodule, it is recommended to edit the `./.gitmodules` file and change the absolute url to a relative url unless the git server is not the same

    ```bash
    git submodule add "REPO-URL.git" "DIR"
    ```
    
- Initialize the submodule and pull the repo
	
	```bash
	git submodule init
	git submodule update
	```

	- Updating the submodule
		- The submodule is a nested repo, using `git fetch` and `git merge` will work within submodule directory
		- For easier updating, especially if their are multiple submodules, use th efollowing command to update the submodule to the latest commit
			
			```bash
			git submodule update --remote
			```

- Installing via source
	- Be sure to be in the submodule directory to be installed
	- Updating is running the same command again, it will override the currently installed version

	```bash
	python setup.py install
	```