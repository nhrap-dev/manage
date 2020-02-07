# manage.py

## This is a submodule for Hazus Open-Source Tools

`manage.py` handles all the updates for HazPy and the GUI for all the tools! Pretty cool hunh?

## To use

1.  Open the root of your tool and run `git submodule add -b master https://github.com/nhrap-dev/manage.git src\manage`
2.  In the tool root run `git config --global submodule.recurse true`
3.  Create a config.json file in the src directory with the following code:

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

4.  Replace the URLs with the URLs for your tool:

    - **release:** This alternates between the URLs for prod and dev. Update to prod for production.
    - **hazusInitUrl:** This can stay the same. It's the raw URL to the `__init__.py` file in the hazus python package root.
    - **repoZipfileUrl:** This is the URL to the zipfile download for your tool. You can access this URL by going to your repo, clicking on Clone or Download, and then right clicking on Download Zip and copying the URL.
    - **toolInitUrl:** This is the URL to the `__init__.py` file in the root of your tool. You can access it by clicking on your `__init__.py` file, then clicking Raw at the top of your code.

5.  Create an `__init__.py` file in the src folder, so that the manage submodule can be seen by your app. Put this code inside of it:

    ```
    __version__ = '0.0.1'
    __all__ = ['manage']

    from .manage import manage
    ```

6.  Update your run.py file that is called by the .bat entry point:

    If your GUI is in the src folder, you can call

    ```
    from manage.manage import internetConnected, checkForHazusUpdates, checkForToolUpdates
    if internetConnected():
        checkForHazusUpdates()
        checkForToolUpdates()
    ```

    If your GUI is in "Example_Folder", you can call

    ```
    from Example_Folder.manage.manage import internetConnected, checkForHazusUpdates, checkForToolUpdates
    if internetConnected():
        checkForHazusUpdates()
        checkForToolUpdates()
    ```

Happying hacking!
