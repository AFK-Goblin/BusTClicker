from tkinter import messagebox

try:
    from pynput import mouse
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False
    print("pynput module not found. Recording will be disabled.")

def setup_recorder(app):
    """Set up the recorder functionality"""
    if not HAS_PYNPUT:
        return False
    return True

def start_recording(app):
    """Start recording mode to capture mouse clicks"""
    if not HAS_PYNPUT:
        messagebox.showinfo("Info", "Recording requires pynput. Run: pip install pynput")
        return
        
    app.state["status_msg"].set("Recording mode active. Click on screen to capture location.")
    
    def on_click(x, y, button, pressed):
        # We only care when the mouse is pressed down
        if not pressed or not app.state.get("is_recording"):
            return True  # Continue listening
        
        # Route the data back to the main thread securely
        app.root.after(0, lambda: _save_recorded_location(app, x, y))
        return False  # Stop the listener thread entirely
        
    # Start the background listener
    app.record_listener = mouse.Listener(on_click=on_click)
    app.record_listener.daemon = True
    app.record_listener.start()

def _save_recorded_location(app, x, y):
    """Handles data formatting and UI updates strictly on the main thread."""
    state = app.state
    
    # Grab the active group if one is selected
    grp = state.get("group_filter").get()
    
    new_location = {
        "name": f"Location {state['location_counter']}",
        "x": int(x),  # Ensure x/y are clean integers
        "y": int(y),
        "click_type": "Left",
        "action_type": "click",
        "hold_duration": 1.0,
        "group": grp if grp != "All Groups" else ""
    }
    
    # Update State
    state["saved_locations"].append(new_location)
    state["location_counter"] += 1
    state["is_recording"] = False
    
    # Trigger App-level callbacks to handle the UI and Saving
    app.ui.update_record_button(recording=False)
    app.ui.refresh_location_list()
    app.auto_save()
    
    # Update the status bar
    state["status_msg"].set(f"Scribed Location at X: {int(x)}, Y: {int(y)}")