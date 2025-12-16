try:
    from pynput import keyboard
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False

def setup_hotkeys(app):
    if not HAS_PYNPUT: return
        
    def on_press(key):
        try:
            # Convert key to string format
            try: k_str = key.char # 'a', 'b'
            except: k_str = key.name.upper() # 'F6', 'ENTER'
            
            if k_str is None: k_str = str(key).replace("Key.", "").upper()

            # --- REBINDING MODE ---
            if app.is_rebinding:
                action = app.is_rebinding
                app.hotkeys[action] = k_str
                
                # Update Button Text
                btn = getattr(app, f"btn_bind_{action}")
                app.root.after(0, lambda: btn.configure(text=f"{action.title()}: {k_str}"))
                app.root.after(0, lambda: app.status_var.set(f"Bound {action} to {k_str}"))
                
                app.is_rebinding = None
                return

            # --- NORMAL MODE ---
            # Check against saved hotkeys
            if str(k_str).upper() == str(app.hotkeys['record']).upper():
                app.root.after(0, app.toggle_recording)
            elif str(k_str).upper() == str(app.hotkeys['start']).upper():
                app.root.after(0, app.start_clicking)
            elif str(k_str).upper() == str(app.hotkeys['stop']).upper():
                app.root.after(0, app.stop_clicking)
                
        except Exception as e:
            print(f"Key error: {e}")
            
    app.listener = keyboard.Listener(on_press=on_press)
    app.listener.daemon = True
    app.listener.start()