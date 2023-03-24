# ScreenGrabber
Simple Python application with Selenium to grab screenshots with specified viewports.<br>
Add your URL, optional CSS selector <i>(like this - ".random-class")</i> and devices with specified viewport.<br>

Then click on "Take Screenshots" button to capture a browser display for each device and store them locally in "screenshots" folder.

# Prerequisites:
 [Python 3](https://www.python.org/downloads/)

# Libraries:
    selenium: to automate web browser actions and take screenshots.
    It can be installed by running !pip install selenium in the terminal or command prompt.

    Pillow: to handle image files and display the screenshots.
    It can be installed by running !pip install Pillow in the terminal or command prompt.

    tkinter: to create the graphical user interface.
    It is usually included in standard Python installations, but it might need to be installed separately for some platforms.

    sqlite3: to store and load the devices information from a local database file.
    It is a built-in module, so it does not need to be installed separately.

    pathlib: to handle file paths in a platform-independent manner.
    It is also a built-in module, so it does not need to be installed separately.

    A web driver for Selenium, such as chromedriver (default in code), geckodriver, or edgedriver, depending on the web browser and operating system being used.
    The user will need to download the appropriate web driver and add it to the system PATH environment variable or provide its path in the code.

![2023-03-24_11h41_29](https://user-images.githubusercontent.com/77245159/227631019-9217dcf8-4e4e-45c9-b7db-00d23074a0d0.png)<br>
<i>That's my cat, Lucek <3</i>
