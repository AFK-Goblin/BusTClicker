import os
import json

# --- Path setup ---
_CORE_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT_DIR = os.path.dirname(_CORE_DIR)
_PROJECT_DATA_DIR = os.path.join(_PROJECT_ROOT_DIR, "Data")
_DEFAULT_APP_SETTINGS_PATH = os.path.join(_PROJECT_DATA_DIR, "app_settings.json")

def load_locations(config_file): 
    """Load saved locations from file safely without UI blockers."""
    if not os.path.exists(config_file):
        return []
        
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load saved locations: {e}")
        return []
            
def save_locations(locations, config_file): 
    """Save locations to file, creating directories if needed."""
    try:
        data_dir = os.path.dirname(config_file) 
        if data_dir:
            os.makedirs(data_dir, exist_ok=True)
            
        with open(config_file, 'w') as f:
            json.dump(locations, f, indent=2)
    except Exception as e:
        print(f"Failed to save locations: {e}")
        # We raise here so app.py's auto_save can catch it if it wants to
        raise 
        
def load_settings(settings_file=None): 
    """Load core application settings."""
    if settings_file is None:
        settings_file = _DEFAULT_APP_SETTINGS_PATH
        
    settings = {
        "always_on_top": False,
        "transparency": 0.9,
        "mouse_move_duration": 1.0,
        "default_interval": 1.0,
        "default_repetitions": 1
    } 
    
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r') as f:
                settings.update(json.load(f))
        except Exception as e:
            print(f"Failed to load settings: {e}")
            
    return settings
    
def save_settings(settings, settings_file=None): 
    """Save core application settings."""
    if settings_file is None:
        settings_file = _DEFAULT_APP_SETTINGS_PATH
        
    try:
        data_dir = os.path.dirname(settings_file) 
        if data_dir:
            os.makedirs(data_dir, exist_ok=True)
            
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        print(f"Failed to save settings: {e}")