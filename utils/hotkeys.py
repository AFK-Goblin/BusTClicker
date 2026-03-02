try:
    from pynput import keyboard
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False
    print("Mouse/Keyboard modules missing. Run: pip install pynput")

def setup_hotkeys(app):
    if not HAS_PYNPUT: 
        return
        
    # 1. Initialize hotkey state if it doesn't exist yet
    if "hotkeys" not in app.state:
        app.state["hotkeys"] = {"start": "F7", "stop": "F8", "record": "F6"}
    if "is_rebinding" not in app.state:
        app.state["is_rebinding"] = None

    def on_press(key):
        try:
            # 2. Securely convert key to string format
            if hasattr(key, 'char') and key.char is not None:
                k_str = key.char.upper()
            elif hasattr(key, 'name') and key.name is not None:
                k_str = key.name.upper()
            else:
                k_str = str(key).replace("Key.", "").upper()

            # --- REBINDING MODE ---
            current_rebind = app.state.get("is_rebinding")
            if current_rebind:
                # Update the state dictionary
                app.state["hotkeys"][current_rebind] = k_str
                app.state["is_rebinding"] = None
                
                # Safely update the status bar from the main thread
                app.root.after(0, lambda: app.state["status_msg"].set(f"Bound {current_rebind.upper()} to {k_str}"))
                
                # Tell the UI to refresh the button labels (we'll add this method to UI next)
                if hasattr(app.ui, 'refresh_hotkey_buttons'):
                    app.root.after(0, app.ui.refresh_hotkey_buttons)
                return

            # --- NORMAL MODE ---
            # Check against saved hotkeys in state
            hotkeys = app.state["hotkeys"]
            if k_str == hotkeys.get('record'):
                app.root.after(0, app.toggle_recording)
            elif k_str == hotkeys.get('start'):
                app.root.after(0, app.start_clicking)
            elif k_str == hotkeys.get('stop'):
                app.root.after(0, app.stop_clicking)
                
        except Exception as e:
            print(f"Key listener error: {e}")
            
    # 3. Start the background listener
    app.listener = keyboard.Listener(on_press=on_press)
    app.listener.daemon = True
    app.listener.start()