from PIL import Image
from PIL import ImageTk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from ttkbootstrap.constants import *
from tkinter import filedialog
import ttkbootstrap as tb
import json
import pathlib
import subprocess
import os


# Environment temporary storage
env_selected = ""
data_bank = []  
temp_data_bank = {}

# Function to save data to a JSON file
def save_data_to_file(data_dict, filename='data.json'):
    """Function to save data to a JSON file"""
    filepath = os.path.join(os.path.dirname(__file__), 'assets', filename)
    with open(filepath, 'w') as file:
        json.dump(data_dict, file)

# Function to load data from a JSON file
def load_data_from_file(filename='data.json'):
    """Function to load data from a JSON file"""
    filepath = os.path.join(os.path.dirname(__file__), 'assets', filename)
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Function to import new environments
def open_file_dialog():
    """Opens a window to select and import python environments to data base"""
    folder = filedialog.askdirectory()
    if folder:
        path_display_text.config(text="Target Acquired")
        env_path = folder
        env_name = os.path.basename(folder)


        depack = [f'{folder}/bin/python', '-m', 'pip', 'freeze']
        try:
            env_packages_process = subprocess.run(depack, capture_output=True, text=True)
            env_packages = env_packages_process.stdout.strip().split('\n')
            
            # Append a new dictionary to data_bank
            data_bank.append({'name': env_name, 'path': env_path, 'packages': env_packages})

            # Update the display using the updated data_bank
            update_display_frame(data_bank)

            # Save the updated data to the file
            save_data_to_file(data_bank)
        except:
            path_display_text.config(text="Invalid Location")

# Function to update packages in data base
def refresh_data_bank():
    """Runs data base info to update changes made to environment packages"""
    global data_bank
    temp_data_bank = []

    for key in data_bank:
        folder = key['path']
        if os.path.exists(folder):
            env_name = key['name']
            depack = [f'{folder}/bin/python', '-m', 'pip', 'freeze']
            env_packages_process = subprocess.run(depack, capture_output=True, text=True)
            env_packages = env_packages_process.stdout.strip().split('\n')
            temp_data_bank.append({'name': env_name, 'path': folder, 'packages': env_packages})

    data_bank = temp_data_bank
    update_display_frame(data_bank)

    # Save the updated data to the file
    save_data_to_file(data_bank)

    package_data_label.delete(0, END)

    path_display_text.config(text="Arsenals Reloaded")


# updates display frame with database info
def update_display_frame(data_list=data_bank):
    """updates display frame with database info"""
    env_data_label.delete(0, END)
    for item in data_list:
        env_data_label.insert(END, item['name'])

selected_env = ""

# Selection tool
def env_selected(event):
    selected_indices = env_data_label.curselection()

    # Ensure that something is selected before processing
    if not selected_indices:
        return

    # Use the first selected index (assuming single selection)
    selected_index = selected_indices[0]
    env_selected = data_bank[selected_index]['name']

    package_data_label.delete(0, END)

    for package in data_bank[selected_index]['packages']:
        package_data_label.insert(END, package)

    path_display_text.config(text=data_bank[selected_index]['path'])

for key in data_bank:
    env_data_label.insert(END, '{}'.format(key['name'], key))

# Function to delete environment from data base
def delete_environment():
    """Function to delete environment from data base"""
    selected_indices = env_data_label.curselection()

    # Ensure that something is selected before attempting to delete
    if not selected_indices:
        showinfo("No Selection", "Please select an environment to delete.")
        return

    # Loop through selected indices and delete corresponding environment keys
    for i in selected_indices:
        path_display_text.config(text=f"{data_bank[i]['name']} Has been Burned")
        del data_bank[i]

    update_display_frame(data_bank)
    package_data_label.delete(0, END)

    # Save the updated data to the file
    save_data_to_file(data_bank)

# Load data from the file when the script starts
json_path = os.path.join(os.path.dirname(__file__), 'assets', 'data.json')
data_bank = load_data_from_file(json_path)

if not isinstance(data_bank, list):
    data_bank = []  # If data is not loaded successfully or is not in the expected format, initialize as an empty list

root = tb.Window(themename="cyborg")
root.title("PYro-Maniac")

frame = tb.Frame(root)
frame.pack()

# Logo widget
logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'pyro_logo.png')
logo_img = PhotoImage(file=logo_path)

logo_widget = tb.Label(frame, image=logo_img)
logo_widget.image = logo_img
logo_widget.grid(row=0, column=0)

title_frame = tb.Frame(frame, bootstyle="default")
title_frame.grid(row=0, column=1)

app_title = tb.Label(title_frame, bootstyle="warning", text="PYRO-MANIAC ENVIRONMENT MANAGER", font="Helvetica, 20")
app_title.grid(row=0, column=0)

path_bar = tb.LabelFrame(title_frame, text="Path / Status", bootstyle="default")
path_bar.grid(row=1, column=0, sticky="nesw")

path_display_text = tb.Label(path_bar, bootstyle="warning", text="")
path_display_text.pack(fill=BOTH)

for widget in title_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)

button_frame = tb.Frame(frame)
button_frame.grid(row=1, column=0)

file_button = tb.Button(button_frame, text="Select", bootstyle="danger outline", width=10, command=open_file_dialog)
file_button.grid(row=0, column=0)

refresh_button = tb.Button(button_frame, text="Refresh", bootstyle="danger outline", width=10, command=refresh_data_bank)
refresh_button.grid(row=1, column=0)

delete_button = tb.Button(button_frame, text="Delete", bootstyle="danger outline", width=10, command=delete_environment)
delete_button.grid(row=2, column=0)

for widget in button_frame.winfo_children():
    widget.grid_configure(padx=10, pady=10)

data_display_frame = tb.Frame(frame, bootstyle="default")
data_display_frame.grid(row=1, column=1, sticky="news")

env_view_frame = tb.LabelFrame(data_display_frame, bootstyle="default", text="Python Environments")
env_view_frame.pack(side=LEFT, expand=True, fill=BOTH, padx=10, pady=5)

env_data_label = Listbox(env_view_frame)
env_data_label.pack(expand=True, fill=BOTH)

# Ensure the correct dictionary key is used when inserting items
for key in data_bank:
    env_data_label.insert(END, '{}'.format(key['name'], key))

env_data_label.bind('<<ListboxSelect>>', env_selected)

scrollbar = ttk.Scrollbar(env_data_label, orient=VERTICAL, command=env_data_label.yview)
env_data_label['yscrollcommand'] = scrollbar.set

scrollbar.pack(anchor="e", expand=True, fill=Y)

package_view_frame = tb.LabelFrame(data_display_frame, bootstyle="default", text="Environment Packages")
package_view_frame.pack(side=RIGHT, expand=True, fill=BOTH, padx=10, pady=5)

package_data_label = Listbox(package_view_frame, selectmode=SINGLE)
package_data_label.pack(expand=True, fill=BOTH)

scrollbar = ttk.Scrollbar(package_data_label, orient=VERTICAL, command=package_data_label.yview)
package_data_label['yscrollcommand'] = scrollbar.set

scrollbar.pack(anchor="e", expand=True, fill=Y)

update_display_frame(data_bank)

root.mainloop()