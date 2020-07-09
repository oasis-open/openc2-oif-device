# Screaming Bunny Utils

## Installing
### On a standalone System via pip
- Install requires Python 3.6+ and pip

- Install via pip
    ```bash
    pip install git+https://gitlab.labs.g2-inc.net/ScreamingBunny/Utils.git
    ```
        
- To update if already installed
	 
   ```bash
   pip install --upgrade git+https://gitlab.labs.g2-inc.net/ScreamingBunny/Utils.git
   ```

### On a standalone System via submodule source
- Install requires Python 2.7+ and pip

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

   
### Gitlab CI
- Submodule init and update are handled by the CI Runner
- The submodule will be available where its folder is specified
- This repo is recommended to be used as a python pkg, the following is how to install and use it
	- Standalone
		- See the Installing on a standalone system via submodule source

	- Docker
		- Add the submodule directory to the image, a tmp directory is preferred
		- See the Installing on a standalone system via submodule source
		- Cleanup the tmp directory and remove the submodule directory
