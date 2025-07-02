import pyeapi                    # 👉 Imports the pyeapi library to connect to Arista switches
import os                        # 👉 Imports the os module to handle directories
import yaml                      # 👉 Imports yaml to read switch names from devices.yml

pyeapi.load_config('eapi.conf') # 👉 Loads connection details from eapi.conf

# Load switch list from YAML file
with open('optional_backup_yaml.yml', 'r') as file:
    device_dict = yaml.safe_load(file)  # 👉 Converts the YAML file to a Python dictionary

# Set backup folder
directory = "config1"
if not os.path.exists(directory):       # 👉 Checks if the folder 'config1' exists
    os.makedirs(directory)              # 👉 Creates the folder if it doesn't

# Extract switch list
switches = device_dict['switches']      # 👉 Gets the list of switch names

# Loop through each switch and save config
for switch in switches:
    connect = pyeapi.connect_to(switch)                 # 👉 Connects to the switch using profile from eapi.conf
    running_config = connect.get_config(as_string=True) # 👉 Retrieves running config in plain text
    path = f"{directory}/{switch}.cfg"                  # 👉 Sets file path as config1/switchname.cfg
    with open(path, 'w') as file:                       # 👉 Opens the file for writing
        file.write(running_config)                      # 👉 Writes the config to the file
    print(f"Backing up {switch}")                       # 👉 Shows progress in the terminal