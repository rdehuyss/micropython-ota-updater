# MicroPython OTA Updater

This micropython module allows for automatic updating of your code on Microcontrollers using github releases. It allows you to update devices in the field with ease. 

## History
- 2018/07/19 - First public release
- 2020/12/23 - Major rewrite adding support for M5Stack and low memory devices (I now can upgrade big projects with it on devices like M5Stack Core 1 which are very memory constraint) and it now also supports secrets files (which are kept during upgrades)


## Workflow
The workflow is as follows:
* You have a github repo where you host your micropython project
* In this project, you include all your source code in a certain folder (e.g. `app`)
* You also include the ota_updater.py (https://github.com/rdehuyss/micropython-ota-updater)
* You control your releases with GitHub releases (if you want to deploy a new version, create a new GitHub release)

There are now two different ways to update your code:

### Install new version immediately after boot
You can choose to install a new version yourself. Note that due to memory limitations, this must happen first thing after boot.

To do so, make sure you have an active internet connection and use the following code at startup:
```python
@staticmethod
def _otaUpdate():
    ulogging.info('Checking for Updates...')
    from .ota_updater import OTAUpdater
    otaUpdater = OTAUpdater('https://github.com/rdehuyss/chicken-shed-mgr', github_src_dir='src', main_dir='app', secrets_file="secrets.py")
    otaUpdater.install_update_if_available()
    del(otaUpdater)
```

> Do not forget to do a machine.reset() after the code above.


### Let the OTAUpdater decide when to do the update
* whenever you feel fit, you ask the OTAUpdater (on my project this is after a hardware interrupt which starts up the WLAN) to check for a new version using `ota_updater.check_for_update_to_install_during_next_reboot()`
* if a new version is present, the OTAUpdater generate a `next` folder and within that folder a file called `.version_on_reboot`. After that, you do a `machine.reset()` to kill the WIFI connection.
* You use the following code in your `main.py`:
   ```python
    from ota_update.main.ota_updater import OTAUpdater


    def download_and_install_update_if_available():
        o = OTAUpdater('url-to-your-github-project')
        o.install_update_if_available_after_boot('wifi-ssid', 'wifi-password')


    def start():
        # your custom code goes here. Something like this: ...
        # from main.x import YourProject
        # project = YourProject()
        # ...


    def boot():
        download_and_install_update_if_available()
        start()


    boot()
   ```
* the  OTAUpdater will check if there is a file called `next/.version_on_reboot`.
  * If so, it will initialize the WIFI connection, download the latest code, move it to the `app` folder. You then need to do a `machine.reset()`. On reboot, the latest code will be in the `app` folder and you will be running the latest version.
  * If not, it will NOT initialize the WIFI connection and just start the existing code in the `app` folder

## Extra features
### Support for Private Repositories
This module also adds support for private repositories. To do so, use it as follows:

```python
token='YOUR_GITHUB_TOKEN'
updater = OTAUpdater('https://github.com/sergiuszm/cae_fipy', headers={'Authorization': 'token {}'.format(token)})
```

### Support for secrets file
MicroPython OTA updater now also supports a secret file (which is added to .gitignore). This secrets file must be installed initially (e.g. using USB) and will always be kept when downloading newer versions. In my case, it contains the WIFI credentials and other secret stuff.

## More info?
See the [article on Medium](https://medium.com/@ronald.dehuysser/micropython-ota-updates-and-github-a-match-made-in-heaven-45fde670d4eb).

## Example
- [Showerloop](https://github.com/rdehuyss/showerloop/blob/master/main.py) uses the micropython-ota-updater to get the latest release.
- [Chicken Shed Mgr](https://github.com/rdehuyss/chicken-shed-mgr/blob/main/src/main.py) uses the micropython-ota-updater to get the latest release.
