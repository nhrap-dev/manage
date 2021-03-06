# manage.py

`manage.py` handles all the updates for HazPy and the GUI for all the tools! Pretty cool hunh?

## How does it work?

### For the user

When the user opens the tool, manage.py will look to see if any new verison of the tool or HazPy exists on GitHub. If they do, it will automatically download and install them for the user.

### For the developer

**Workflow**

1. Update the manage.py script in the manage repository. manage.py can only be updated here.
2. In your tool, run `git push`. This fires the GitHub Action to update the manage.py script in your tool.
3. Wait about 30 seconds, then run `git pull`. This should pull the updated manage.py into your tool.

## To use

This contains setup instructions for developing open-source tools ontop of HazPy, using manage.py

### 1. src directory and config

1. Create a src directory in the root of your app.

   Diagram

   ```
   root/
   ├── .gitignore
   ├── LICENSE
   ├── README.md
   └── src/
   ```

2. Create a config.json file in the src directory with the following code. For production, change the `"release": "dev"` to `"release": "prod"`.

   ```
   {
       "release": "dev",
       "prod": {
           "hazusInitUrl": "https://raw.githubusercontent.com/nhrap-hazus/hazus/master/hazus/__init__.py",
           "repoZipfileUrl": "https://github.com/nhrap-hazus/export/archive/master.zip",
           "toolInitUrl": "https://raw.githubusercontent.com/nhrap-hazus/export/master/__init__.py"
       },
       "dev": {
           "hazusInitUrl": "https://raw.githubusercontent.com/nhrap-dev/hazus/master/hazus/__init__.py",
           "repoZipfileUrl": "https://github.com/nhrap-dev/export/archive/master.zip",
           "toolInitUrl": "https://raw.githubusercontent.com/nhrap-dev/export/master/__init__.py"
       },
       "proxies": {
           "fema": "http://proxy.apps.dhs.gov:80"
       }
   }

   ```

   Diagram

   ```
   root/
   ├── .gitignore
   ├── LICENSE
   ├── README.md
   └── src/
       └──config.json
   ```

3. Replace the URLs with the URLs for your tool:

   - **release:** _Alternate_ — This specifies which URL links manage.py looks at.
   - **hazusInitUrl:** _Don't change_ — It's the raw URL to the `__init__.py` file in the hazus python package root. It updates the users HazPy installation when the version changes in the `__init__.py`.
   - **repoZipfileUrl:** _Change_ — This is the URL to the zipfile download for your tool. manage.py uses this to auto-download your tool updates. You can access this URL on GitHub by going to your repo, clicking on Clone or Download, and then right clicking on Download Zip and copying the URL.
   - **toolInitUrl:** _Change_ — This is the URL to the `__init__.py` file in the root of your tool on GitHub. When the version is updated in this file, manage.py prompts the user to update the tool. You can access the URL on GitHub by clicking on your `__init__.py` file, then clicking Raw at the top of your code.

4. Create an `__init__.py` file in the src directory with the following code, updating the author. When you update the version here, it will prompt the user to update their tool and download the latest from GitHub:

   ```
    # -*- coding: utf-8 -*-
    """
        Hazus Open-Source Tool
        ~~~~~

        FEMA developed module for analzying risk and loss from natural hazards.

        :copyright: © 2019 by FEMA's Natural Hazards and Risk Assesment Program.
        :license: cc, see LICENSE for more details.
        :author: <firstName lastName>; <first.last@fema.dhs.gov>
    """

    __version__ = '0.0.1'
    __all__ = ['']
   ```

   Diagram

   ```

   root/
   ├── .gitignore
   ├── LICENSE
   ├── README.md
   └── src/
       ├── __init__.py
       └── config.json

   ```

### 2. GitHub Action for manage.py

1. Create a `main.yml` file in this directory structure at the root of your app: `.github/workflows/main.yml`

   Diagram

   ```

   root/
   ├── .github/
   │    └── workflows/
   │        └── main.yml
   ├── .gitignore
   ├── LICENSE
   ├── README.md
   └── src/
       ├── __init__.py
       └── config.json

   ```

2. Enter the following code in the `main.yml` file. You can replace the user email and name if needed. For production, you will change `git clone https://github.com/nhrap-dev/manage.git` to `git clone https://github.com/nhrap-hazus/manage.git`

   ```
   name: CI

   on: [push]

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
       - uses: actions/checkout@v2
       - name: update manage.py
         run: |
           git config --global user.email "jraines521@gmail.com"
           git config --global user.name "lorax521"
           git clone https://github.com/nhrap-dev/manage.git
           cp ./manage/manage.py ./src/manage.py
           rm -rf manage
           git add .
           git commit -m "update manage.py"
           git push
   ```

### 3. Add the manage.py actions to your app

1. Create a run.py file in the same directory as your GUI.

   Diagram

   ```

   root/
   ├── .github/
   │    └── workflows/
   │        └── main.yml
   ├── .gitignore
   ├── LICENSE
   ├── README.md
   └── src/
       ├── __init__.py
       ├── config.json
       ├── GUI.py
       └── run.py

   ```

2. Paste the following code in your run.py

   ```
   try:
       from manage import internetConnected, checkForHazusUpdates, checkForToolUpdates
       if internetConnected():
           checkForHazusUpdates()
           checkForToolUpdates()

       from subprocess import check_call
       check_call('CALL conda.bat activate hazus_env && python .\src\GUI.py', shell=True)

   except:
       import ctypes
       messageBox = ctypes.windll.user32.MessageBoxW
       messageBox(0,"The tool was unable to open. You need internet connection for this tool to update. If this problem persists, contact hazus-support@riskmapcds.com","Hazus", 0x1000)

   ```

3. Create a `.bat` file in your root. Name it your tool name (example: earthquake-tool.bat).

   Diagram

   ```

   root/
   ├── .github/
   │    └── workflows/
   │        └── main.yml
   ├── .gitignore
   ├── earthquake-tool.bat
   ├── LICENSE
   ├── README.md
   └── src/
       ├── __init__.py
       ├── config.json
       ├── GUI.py
       └── run.py

   ```

4. Enter this code in your `.bat` file:

   ```
   CALL conda.bat activate hazus_env & start /min python src\run.py
   ```

Your tool should now open with the `.bat` file and perform checks for tool and HazPy updates on open. Everytime you perform a `git push`, it will update the manage.py file adding it to the directory below. Make sure to perform a `git pull` so it will pull that manage.py file down locally.

Diagram

```

root/
├── .github/
│    └── workflows/
│        └── main.yml
├── .gitignore
├── earthquake-tool.bat
├── LICENSE
├── README.md
└── src/
    ├── __init__.py
    ├── config.json
    ├── GUI.py
    ├── manage.py
    └── run.py

```

Congrats, you just made a HazPy open-source tool!
Happying hacking
