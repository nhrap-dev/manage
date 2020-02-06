from subprocess import check_output, check_call, call
import os
import ctypes
import sys
import requests
import pkg_resources
import json
import socket
try:
    with open('./src/config.json') as configFile:
        config = json.load(configFile)
except:
    with open('./config.json') as configFile:
        config = json.load(configFile)


release = config['release']

def createProxyEnv():
    newEnv = os.environ.copy()
    newEnv["HTTP_PROXY"] = config['proxies']['fema']
    newEnv["HTTPS_PROXY"] = config['proxies']['fema']
    return newEnv

def setProxies():
    call('set HTTP_PROXY=' + config['proxies']['fema'], shell=True)
    call('set HTTPS_PROXY=' + config['proxies']['fema'], shell=True)
    os.environ["HTTP_PROXY"] = config['proxies']['fema']
    os.environ["HTTPS_PROXY"] = config['proxies']['fema']

def activateEnv():
    try:
        try:
            check_call('conda activate hazus_env', shell=True)
        except:
            check_call('activate hazus_env', shell=True)
    except:
        print("Can't activate hazus_env")

def condaInstallHazus():
    messageBox = ctypes.windll.user32.MessageBoxW
    print('Checking for the conda environment hazus_env')
    try:
        try:
            check_call('conda activate hazus_env', shell=True)
        except:
            print('Creating the conda hazus_env')
            try:
                call('echo y | conda create -y -n hazus_env', shell=True)
            except:
                setProxies()
                call('echo y | conda create -y -n hazus_env', shell=True)
        print('Installing the hazus python package')
        try:
            try:
                check_call('conda activate hazus_env && echo y | conda install -c nhrap hazus', shell=True)
            except:
                check_call('activate hazus_env && echo y | conda install -c nhrap hazus', shell=True)
        except:
            setProxies()
            try:
                check_call('conda activate hazus_env && echo y | conda install -c nhrap hazus', shell=True)
            except:
                check_call('activate hazus_env && echo y | conda install -c nhrap hazus', shell=True)
            
        messageBox(0,"The Hazus Python package was successfully installed!","Hazus", 0x1000)
    except:
        messageBox(0, 'Unable to install the hazus python package. If this error persists, contact hazus-support@riskmapcds.com for assistance.',"Hazus", 0x1000)

def installHazus():
    messageBox = ctypes.windll.user32.MessageBoxW
    returnValue = messageBox(None,"The Hazus Python package is required to run this tool. Would you like to install it now?","Hazus",0x1000 | 0x4)
    if returnValue == 6:
        output = check_output('conda config --show channels')
        channels = list(map(lambda x: x.strip(), str(output).replace('\\r\\n', '').split('-')))[1:]
        if not 'anaconda' in channels:
            call('conda config --add channels anaconda')
            print('anaconda channel added')
        if not 'conda' in channels and not 'forge' in channels:
            call('conda config --add channels conda-forge')
            print('conda-forge channel added')
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
        print("Installing the Hazus Python package - hold your horses, this could take a few minutes... but it's totally worth it")
        try:
            print('Conda is installing hazus')
            condaInstallHazus()
        except:
            messageBox(0,"An error occured. The Hazus Python package was not installed. Please check your network settings and try again.","Hazus", 0x1000)

def update():
    messageBox = ctypes.windll.user32.MessageBoxW
    returnValue = messageBox(None,"A newer version of the Hazus Python package was found. Would you like to install it now?","Hazus",0x1000 | 0x4)
    if returnValue == 6:
        print('Conda is installing hazus')
        condaInstallHazus()

def checkForHazusUpdates():
    messageBox = ctypes.windll.user32.MessageBoxW
    try:
        pkg_resources.get_distribution('hazus')
        installedVersion = pkg_resources.get_distribution('hazus').version
        try:
            req = requests.get(config[release]['hazusInitUrl'], timeout=0.5)
        except:
            setProxies()
            req = requests.get(config[release]['hazusInitUrl'], timeout=0.5)
        newestVersion = parseVersionFromInit(req.text)
        if newestVersion != installedVersion:
            returnValue = messageBox(None,"A newer version of the Hazus Python package was found. Would you like to install it now?","Hazus",0x1000 | 0x4)
            if returnValue == 6:
                print('updating hazus')
                update()
        else:
            print('Hazus is up to date')
    except:
        installHazus()

def checkForToolUpdates():
    messageBox = ctypes.windll.user32.MessageBoxW
    try:
        with open('__init__.py') as init:
            text = init.readlines()
            textBlob = ''.join(text)
            installedVersion = parseVersionFromInit(textBlob)
        try:
            req = requests.get(config[release]['toolInitUrl'], timeout=0.5)
        except:
            setProxies()
            req = requests.get(config[release]['toolInitUrl'], timeout=0.5)
        newestVersion = parseVersionFromInit(req.text)
        if newestVersion != installedVersion:
            returnValue = messageBox(None,"A newer version of the tool was found. Would you like to install it now?","Hazus",0x1000 | 0x4)
            if returnValue == 6:
                print('updating tool')
                updateTool()
        else:
            print('Tool is up to date')
    except:
        messageBox(0, 'Unable to check for tool updates. If this error persists, contact hazus-support@riskmapcds.com for assistance.',"Hazus", 0x1000)

def updateTool():
    messageBox = ctypes.windll.user32.MessageBoxW
    try:
        from distutils.dir_util import copy_tree
        from shutil import rmtree
        from io import BytesIO
        from zipfile import ZipFile
        try:
            r = requests.get(config[release]['repoZipfileUrl'])
        except:
            setProxies()
            r = requests.get(config[release]['repoZipfileUrl'])
        z = ZipFile(BytesIO(r.content))
        z.extractall()
        fromDirectory  = z.namelist()[0]
        toDirectory = './'
        copy_tree(fromDirectory, toDirectory)
        rmtree(fromDirectory)
        messageBox(0, 'Tools was successfully updated! I hope that was quick enough for you.',"Hazus", 0x1000)
    except:
        messageBox(0, 'The tool update failed. If this error persists, contact hazus-support@riskmapcds.com for assistance.',"Hazus", 0x1000)


def parseVersionFromInit(textBlob):
    reqList = textBlob.split('\n')
    version = list(filter(lambda x: '__version__' in x, reqList))[0]
    replaceList = ['__version__', '=', "'", '"']
    for i in replaceList:
        version = version.replace(i, '')
    version = version.strip()
    return version

def internetConnected():
    # http://zetcode.com/python/socket/
    print('Checking for internet connection')
    socket.setdefaulttimeout(0.5)
    try: 
        try:
            # try with normal connections
            hostname = 'google.com'
            host = socket.gethostbyname(hostname)
        except:
            # adds DHS proxies and retries
            print('retrying with proxies')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                host = "proxy.apps.dhs.gov" #proxy server IP
                port = 80            #proxy server port
                s.connect((host , port))
                s.sendall(b"GET / HTTP/1.1\r\nHost: www.google.com\r\nAccept: text/html\r\nConnection: close\r\n\r\n")
        print('Found connection')
        return True
    except:
        print('Unable to find connection')
        return False
