import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageTk
from io import BytesIO
import datetime
import time
import tkinter as tk
from tkinter.font import Font
import sqlite3
from pathlib import Path

def save_devices(devices):
    # Open a connection to the database file
    conn = sqlite3.connect('files/devices.db')

    # Iterate over the devices and update them in the database
    for name, (width, height) in devices.items():
        conn.execute("INSERT OR REPLACE INTO devices (name, width, height) VALUES (?, ?, ?)",
                     (name, width, height))

    # Commit the changes to the database and close the connection
    conn.commit()
    conn.close()


def load_devices():
    # Open a connection to the database file
    conn = sqlite3.connect('files/devices.db')

    # Check if the devices table exists in the database and create it if it doesn't
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='devices'")
    result = cursor.fetchone()
    if result is None:
        conn.execute('''CREATE TABLE devices
                         (name TEXT PRIMARY KEY,
                          width INTEGER,
                          height INTEGER);''')
        # Insert the default devices into the database
        for name, (width, height) in default_devices.items():
            conn.execute("INSERT INTO devices (name, width, height) VALUES (?, ?, ?)",
                         (name, width, height))
        conn.commit()

    # Load the devices from the database into a dictionary
    devices = {}
    cursor = conn.execute("SELECT name, width, height FROM devices")
    for row in cursor:
        name, width, height = row
        devices[name] = (width, height)

    # Close the connection to the database file
    conn.close()

    return devices


# Define the default device sizes
default_devices = {
    "Mobile": (375, 812),
    "Tablet": (1024, 1366),
    "Desktop": (1920, 1080)
}

# Load the devices from the database or use the default devices if the database is empty
devices = load_devices()
if not devices:
    devices = default_devices
    save_devices(devices)

# Define a function to take a screenshot after refreshing the page
def take_screenshot(url, size, selector=None):
    # Open the web page in Selenium
    driver = webdriver.Chrome()
    driver.get(url)

    # Set the window size
    driver.set_window_size(*size)

    # Wait for the element to be present
    time.sleep(2)
    if selector:
        wait = WebDriverWait(driver, timeout=10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        # Center the element using the provided selector class
        element = driver.find_element(By.CSS_SELECTOR, selector)
        driver.execute_script("return arguments[0].scrollIntoView({block: 'center'});", element)
    else:
        wait = WebDriverWait(driver, timeout=10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Wait for the page to fully load
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(2)

    # Take a screenshot
    screenshot = driver.get_screenshot_as_png()

    # Save the screenshot with a timestamp under the 'screenshots' folder
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    dir_path = os.path.join(os.getcwd(), 'screenshots')
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    filename = f"screenshot_{size[0]}x{size[1]}_{timestamp}.png"
    filepath = os.path.join(dir_path, filename)
    Image.open(BytesIO(screenshot)).save(filepath)
    
    # Close the web page
    driver.quit()

# Define a function to take screenshots for all device sizes
def take_all_screenshots(url, selector):
    # Take a screenshot for each device size
    for device_name, device_size in devices.items():
        size = device_size
        if selector:
            take_screenshot(url, size, selector)
        else:
            take_screenshot(url, size)

# Define a function to handle the button click event
def on_click():
    url = url_entry.get()
    selector = selector_entry.get()

    # Take screenshots for all device sizes
    take_all_screenshots(url, selector)

    # Show a message box to indicate the screenshots have been saved
    tk.messagebox.showinfo("Screenshot saved", "Screenshots saved successfully!")

# Define a function to add a new device
def add_device():
    device_name = device_name_entry.get()
    width = int(width_entry.get())
    height = int(height_entry.get())
    devices[device_name] = (width, height)
    device_listbox.insert(tk.END, f"{device_name} ({width}x{height})")

# Define a function to remove a device
def remove_device():
    device_name_with_resolution = device_listbox.get(device_listbox.curselection())
    device_name = device_name_with_resolution.split()[0]
    devices.pop(device_name)
    device_listbox.delete(device_listbox.curselection())

# Create the main window
root = tk.Tk()
root.title("Screen Grabber")

# Create an Image widget
# Load the image and resize it to 50% of its original width
image = Image.open("files/sg-logo.png")
width = int(image.width / 2)
height = int(image.height / 2)
image = image.resize((width, height), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(image)

# Create a label to display the logo
logo_label = tk.Label(root, image=logo)
logo_label.pack(pady=10)

# Create a label and entry for the URL
url_label = tk.Label(root, text="URL:")
url_label.pack()
url_entry = tk.Entry(root)
url_entry.pack()

# Create a label and entry for the CSS selector
selector_label = tk.Label(root, text="CSS Selector (optional):")
selector_label.pack()
selector_entry = tk.Entry(root)
selector_entry.pack()

# Create a font object for the button text
special_button_font = Font(size=12, weight="bold")

# Create a button to take screenshots
button = tk.Button(root, text="Take Screenshots", font=special_button_font, command=on_click)
button.pack(pady=10)

# Create a label and listbox for the devices
device_label = tk.Label(root, text="Devices:")
device_label.pack()
device_listbox = tk.Listbox(root)
for device_name, device_size in devices.items():
    size_text = f"{device_size[0]}x{device_size[1]}"
    device_listbox.insert(tk.END, f"{device_name} ({size_text})")
device_listbox.pack()

# Create a frame to hold the device form
device_frame = tk.Frame(root)

# Create labels and entries for the device form
device_name_label = tk.Label(device_frame, text="Device Name:")
device_name_label.pack()
device_name_entry = tk.Entry(device_frame)
device_name_entry.pack()

width_label = tk.Label(device_frame, text="Width:")
width_label.pack()
width_entry = tk.Entry(device_frame)
width_entry.pack()

height_label = tk.Label(device_frame, text="Height:")
height_label.pack()
height_entry = tk.Entry(device_frame)
height_entry.pack()

# Create buttons to add and remove devices
add_button = tk.Button(device_frame, text="Add Device", command=add_device)
add_button.pack(side=tk.LEFT, padx=5)
remove_button = tk.Button(device_frame, text="Remove Device", command=remove_device)
remove_button.pack(side=tk.LEFT, padx=5)

# Add the device form to the main window
device_frame.pack(pady=10)

def save_devices_to_database():
    save_devices(devices)
    print("Saved devices to database")

# Create a button to save the devices to the database
save_button = tk.Button(root, text="Save settings", command=save_devices_to_database)
save_button.pack(side=tk.TOP, padx=5)

def restore_default_settings():
    # Check if the file exists
    if os.path.exists("files/devices.db"):
        # If it exists, remove it
        os.remove("files/devices.db")
        print("Restored default settings, by removing database file")
        # Reload the script
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        print("Cannot restore default settings, database file does not exist")
    
# Create a button to restore default settings
restore_button = tk.Button(root, text="Restore default settings", command=restore_default_settings)
restore_button.pack(side=tk.TOP, padx=5)

# Set the padding and margin
root.configure(pady=15)

# Start the main loop
root.mainloop()
