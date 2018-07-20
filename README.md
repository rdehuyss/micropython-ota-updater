# MicroPython OTA Updater

This micropython module allows for automatic updating of your code on Microcontrollers using github releases.

The workflow is as follows:
* You have a github repo where you host your micropython project
* In this project, you include all your source code in a folder called 'main'
* You also include the ota_updater.py (https://github.com/rdehuyss/micropython-ota-updater)
* whenever you feel fit, you ask the OTAUpdater (on my project this is after a hardware interrupt which starts up the WLAN) to check for a new version using `ota_updater.check_for_update_to_install_during_next_reboot()`
* if a new version is present, the OTAUpdater generate a `next` folder and within that folder a file called `.version_on_reboot`. After that, you do a `machine.reset()`
* You use the following code in your `main.py`:
   ```python
    from ota_update.main.ota_updater import OTAUpdater


    def download_and_install_update_if_available():
        o = OTAUpdater('url-to-your-github-project')
        o.download_and_install_update_if_available('wifi-ssid', 'wifi-password')


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
  * If so, it will download the latest code, move it to the `main` folder and do a `machine.reset()`. On reboot, the OTAUpdater will see that you are running on the latest version and just start your code in the `main` folder
  * If not, it will just start your code in the `main` folder

This workflow allows you to update devices in the field with ease. 