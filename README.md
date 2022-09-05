# Set up
1. [Create "Personal access token" on GitHub](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token):
Settings -> Developer settings -> Personal access tokens.
2. Create .env file in the same folder as main.py
3. Write to .env: [GH_TOKEN](https://github.com/SergeyPirogov/webdriver_manager#configuration)=your token
4. Provide Firefox profile folder name in settings at [FIREFOX_PROFILE_FOLDER](settings.py) variable.
Profile folder location: Help -> Troubleshooting Information -> Profile folder

Install unrar. On Linux:
```
sudo apt install unrar
```
On Windows download "UnRAR for Windows" - "Command line freeware Windows UnRAR" from https://www.rarlab.com/rar_add.htm.
Exctract file to current working directory.

There are plans to make it work with 7zip.

# Useful links
1. [Firefox driver](https://github.com/mozilla/geckodriver/releases)
2. [Firefox configs](http://kb.mozillazine.org/About:config_entries)
3. [Firefox config editor](https://support.mozilla.org/en-US/kb/about-config-editor-firefox)
4. [Webdriver manager](https://github.com/SergeyPirogov/webdriver_manager)
