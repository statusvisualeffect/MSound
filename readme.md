# MSound
MSound is a simple yet powerful application that plays custom sounds for mouse clicks and keyboard presses. It allows users to configure different sounds for left, right, and middle mouse clicks, as well as for keyboard key presses. Users can also set a custom key combination to toggle the visibility of the application window and adjust the volume of the sounds.

# Features
Customizable Sounds: Set custom sound files for left, right, and middle mouse clicks, as well as keyboard key presses.
Volume Control: Adjust the sound volume from 1% to 100%.
Configurable Key Combination: Set a key combination to toggle the application window's visibility.
Theme Selection: Choose between light and dark themes.
Support for All Keys: Includes support for all keyboard keys, including special keys like function keys (F1, F2, ..., F12), space, enter, tab, escape, etc.
Installation
Prerequisites
Python 3.6 or later
pip package manager

#Install the required Python packages using the following command:

pip install PyQt5 pynput pygame
Running the Application
Run the application by executing the start.bat file:
start.bat

# Usage
Launching the Application
Upon launching, the application window is hidden by default. Use the configured key combination to toggle the visibility of the application window.

# Configuring Settings
Open Settings: Click the Settings button to open the settings dialog.
Enable/Disable Sounds: Check or uncheck the boxes to enable or disable specific sounds for left, right, and middle mouse clicks, as well as keyboard presses.
Set Custom Sounds: Use the Browse buttons to set custom sound files or click the Reset buttons to revert to default sounds.
Adjust Volume: Use the volume slider to set the sound volume from 1% to 100%.
Set Key Combination: Select keys from the dropdowns to set the key combination for toggling the application window.
Save Settings: Click the Save button to save your settings.
Playing Sounds
The application will play the configured sounds for mouse clicks and keyboard presses based on your settings.

# Closing the Application
To close the application, use the configured key combination to toggle the window visibility and then close the application window.

# Configuration File
The application settings are saved in a config.json file located in the same directory as the script. The configuration includes settings for enabled sounds, sound file paths, theme, key combination, and volume.

