# manage.py

`manage.py` handles all the updates for HazPy and the GUI for all the tools! Pretty cool hunh?

## To use

### src directory and config

1. Create a src directory in the root of your app.
2. Create a config.json file in the src directory with the following code:

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

3. Replace the URLs with the URLs for your tool:

   - **release:** This alternates between the URLs for prod and dev. Update to prod for production.
   - **hazusInitUrl:** This can stay the same. It's the raw URL to the `__init__.py` file in the hazus python package root.
   - **repoZipfileUrl:** This is the URL to the zipfile download for your tool. You can access this URL by going to your repo, clicking on Clone or Download, and then right clicking on Download Zip and copying the URL.
   - **toolInitUrl:** This is the URL to the `__init__.py` file in the root of your tool. You can access it by clicking on your `__init__.py` file, then clicking Raw at the top of your code.

### GitHub Action for manage.py

1. Create this file and directory structure in the root of your app: `.github/workflows/main.yml`
2. Enter the following code in the `main.yml` file. You can replace the user email and name if needed. The rest should be the same.

   ```
   name: CI

   on: [push]

   jobs:
   build:
       runs-on: ubuntu-latest

       steps:
       - uses: actions/checkout@v2
       - name: Update manage.py
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

### Add the manage.py actions to your app

1. Create a run.py file in the same directory as your GUI.
2. Paste the following code in your run.py

   ```
    try:
        from manage.manage import internetConnected, checkForHazusUpdates, checkForToolUpdates
        if internetConnected():
            checkForHazusUpdates()
            checkForToolUpdates()

        from subprocess import check_call
        try:
            check_call('conda activate hazus_env && python .\src\__main__.pyw', shell=True)
        except:
            check_call('activate hazus_env && python .\src\__main__.pyw', shell=True)
    except:
        import ctypes
        messageBox = ctypes.windll.user32.MessageBoxW
        messageBox(0,"The tool was unable to open. You need internet connection for this tool to update. If this problem persists, contact hazus-support@riskmapcds.com","Hazus", 0x1000)
   ```

3. In the run.py file, change `.\src\__main__.pyw` to the file that runs your GUI.
4. Create a `.bat` file in your root that calls the run.py file. Enter this code in your `.bat` file:

   ```
   conda activate hazus_env & start /min python src\run.py && exit
   ```

Happying hacking!
