import os #
import json #
from tkinter import messagebox #

# --- Path setup for Data folder relative to project root ---
# Path to the directory containing settings.py (i.e., the 'core' directory)
_CORE_DIR = os.path.dirname(os.path.abspath(__file__))
# Path to the project root directory (one level up from 'core')
_PROJECT_ROOT_DIR = os.path.dirname(_CORE_DIR)
# Path to the Data directory within the project root
_PROJECT_DATA_DIR = os.path.join(_PROJECT_ROOT_DIR, "Data")

# Default settings file path, now relative to project root
_DEFAULT_APP_SETTINGS_PATH = os.path.join(_PROJECT_DATA_DIR, "app_settings.json")
# --- End of Path setup ---

def load_locations(config_file): 
    """Load saved locations from file. config_file is expected to be an absolute path."""
    saved_locations = [] #
    try:
        if os.path.exists(config_file): #
            with open(config_file, 'r') as f: #
                saved_locations = json.load(f) #
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load saved locations: {e}") #
    return saved_locations #
            
def save_locations(locations, config_file): 
    """Save locations to file. config_file is expected to be an absolute path."""
    try:
        # Ensure the Data directory exists (using the directory from the absolute path)
        data_dir_for_locations = os.path.dirname(config_file) 
        if data_dir_for_locations and not os.path.exists(data_dir_for_locations):
            os.makedirs(data_dir_for_locations)
            
        with open(config_file, 'w') as f: #
            json.dump(locations, f, indent=2) #
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save locations: {e}") #
        
def load_settings(settings_file=None): 
    """Load application settings. Uses default absolute path if None."""
    if settings_file is None:
        settings_file = _DEFAULT_APP_SETTINGS_PATH
        
    settings = {
        "always_on_top": False, #
        "transparency": 0.9, #
        "mouse_move_duration": 1.0, #
        "default_interval": 1.0, #
        "default_repetitions": 1 #
    } 
    
    try:
        if os.path.exists(settings_file): #
            with open(settings_file, 'r') as f: #
                loaded = json.load(f) #
                settings.update(loaded) #
    except Exception as e:
        print(f"Failed to load settings: {e}") #
    return settings #
    
def save_settings(settings, settings_file=None): 
    """Save application settings. Uses default absolute path if None."""
    if settings_file is None:
        settings_file = _DEFAULT_APP_SETTINGS_PATH
        
    try:
        # Ensure the Data directory exists (using the directory from the absolute path)
        data_dir_for_settings = os.path.dirname(settings_file) 
        if data_dir_for_settings and not os.path.exists(data_dir_for_settings):
            os.makedirs(data_dir_for_settings)
            
        with open(settings_file, 'w') as f: #
            json.dump(settings, f, indent=2) #
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save settings: {e}") #