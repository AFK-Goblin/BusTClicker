from tkinter import messagebox
import tkinter as tk

# Try to import needed modules
try:
    from pynput import mouse
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False
    print("pynput module not found. Recording will be disabled.")

def setup_recorder(app):
    """Set up the recorder functionality"""
    # Nothing to set up if pynput is not available
    if not HAS_PYNPUT:
        return False
    return True

def start_recording(app):
    """Start recording mode to capture mouse clicks"""
    if not HAS_PYNPUT:
        messagebox.showinfo("Info", "Recording requires pynput module. Please install it with: pip install pynput")
        return
        
    app.is_recording = True
    app.record_button.configure(text="Stop Recording", style="Warning.TButton")
    app.status_var.set("Recording mode active. Click on screen to capture location.")
    
    def on_click(x, y, button, pressed):
        if not pressed or not app.is_recording:
            return True  # Continue listening
        
        # Get the location when mouse clicked
        app.root.after(0, lambda: add_new_location_instant(app, x, y))
        return False  # Stop listener
        
    # Start the mouse listener in a separate thread
    app.record_listener = mouse.Listener(on_click=on_click)
    app.record_listener.daemon = True
    app.record_listener.start()

def add_new_location_instant(app, x, y):
    """Add a new click location from the recorder"""
    # Create a new location with default values
    new_location = {
        "name": f"Location {app.location_counter}",
        "x": x,
        "y": y,
        "click_type": "Left",  # Default to left click
        "action_type": "click"  # Explicitly mark as click action
    }
    
    # Add default hold duration for future use (won't affect normal clicks)
    new_location["hold_duration"] = 1.0
    
    # Increment the counter for next time
    app.location_counter += 1
    
    # Add to saved locations and update UI
    app.saved_locations.append(new_location)
    app.update_location_list()
    
    # Import here to avoid circular imports
    from core.settings import save_locations
    save_locations(app.saved_locations, app.config_file)
    
    # Select the newly added location
    for item in app.location_tree.get_children():
        values = app.location_tree.item(item, "values")
        if values and values[0] == new_location["name"]:
            app.location_tree.selection_set(item)
            app.location_tree.see(item)
            break
    
    # Show a brief notification in the status bar
    app.status_var.set(f"Location added at X: {x}, Y: {y} - Use 'Edit Selected' to customize")
    
    # Reset the recording state
    app.is_recording = False
    app.record_button.configure(text="Record New Location")
    
    # After a delay, return to Ready status
    app.root.after(3000, lambda: app.status_var.set("Ready"))