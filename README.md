# Set up
1. [Create "Personal access token" on GitHub](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token):
Settings -> Developer settings -> Personal access tokens.
2. Create .env file in the same folder as main.py
3. Write to .env: [GH_TOKEN](https://github.com/SergeyPirogov/webdriver_manager#configuration)=your token
4. Provide Firefox profile folder name in settings at [FIREFOX_PROFILE_FOLDER](settings.py) variable.
Profile folder location: Help -> Troubleshooting Information -> Profile folder
5. Depending on library you use:
    1. [**rarfile**](https://pypi.org/project/rarfile/).\
    On Linux install unrar: `sudo apt install unrar`.\
    On Windows download ["UnRAR for Windows"](https://www.rarlab.com/rar_add.htm) (Command line freeware Windows UnRAR). Then extract file to current working directory.
    2. [**subprocess**](https://docs.python.org/3/library/subprocess.html). Download and install [7-zip](https://www.7-zip.org/).

# Useful links
1. [Firefox driver](https://github.com/mozilla/geckodriver/releases)
2. [Firefox configs](http://kb.mozillazine.org/About:config_entries)
3. [Firefox config editor](https://support.mozilla.org/en-US/kb/about-config-editor-firefox)
4. [Webdriver manager](https://github.com/SergeyPirogov/webdriver_manager)
