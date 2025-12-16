import threading
import time
import random
from tkinter import messagebox
import tkinter as tk

try:
    import pyautogui
    import pydirectinput
except ImportError:
    print("Mouse modules missing.")

def start_clicking(app):
    if not app.saved_locations:
        messagebox.showinfo("Empty", "Grimoire is empty!")
        return
        
    app.is_clicking = True
    app.start_button.configure(state="disabled")
    app.stop_button.configure(state="normal")
    app.status_var.set("Casting spells...")
    
    app.click_thread = threading.Thread(target=perform_clicking, args=(app,))
    app.click_thread.daemon = True
    app.click_thread.start()

def perform_clicking(app):
    try:
        interval = app.interval_var.get()
        reps = app.repetitions_var.get() if not app.infinite_var.get() else float('inf')
        random_delay = app.random_delay_var.get()
        
        # Get actions based on filter/selection
        actions = app.saved_locations
        if app.group_var.get() != "All Groups":
            actions = [x for x in actions if x.get("group") == app.group_var.get()]
            
        count = 0
        while app.is_clicking and count < reps:
            app.root.after(0, lambda c=count: app.status_var.set(f"Casting Ritual {c+1}..."))
            
            for loc in actions:
                if not app.is_clicking: break
                
                atype = loc.get("action_type", "click")
                if atype == "click":
                    hold = loc.get("hold_duration", 1.0) if "Hold" in loc.get("click_type") else None
                    do_click(app, loc["x"], loc["y"], loc["click_type"], hold)
                elif atype == "keystroke":
                    do_keystroke(app, loc["key"])
                
                # Delays
                wait = interval
                if random_delay: wait += random.uniform(-0.5, 0.5)
                time.sleep(max(0.1, wait))
                
            count += 1
            
        if app.is_clicking:
            app.root.after(0, app.stop_clicking)
            
    except Exception as e:
        print(f"Error: {e}")
        app.root.after(0, app.stop_clicking)

def do_click(app, x, y, click_type, hold_duration=None):
    try:
        # --- SPIRIT JITTER LOGIC ---
        final_x, final_y = x, y
        if app.jitter_enabled.get():
            r = app.jitter_range.get()
            final_x += random.randint(-r, r)
            final_y += random.randint(-r, r)
            
        # Move
        duration = app.mouse_move_duration.get()
        cur_x, cur_y = pyautogui.position()
        steps = int(max(5, duration * 20))
        
        for i in range(steps):
            nx = int(cur_x + (final_x - cur_x) * ((i+1)/steps))
            ny = int(cur_y + (final_y - cur_y) * ((i+1)/steps))
            pydirectinput.moveTo(nx, ny)
            time.sleep(duration/steps)
            
        pydirectinput.moveTo(final_x, final_y)
        
        # Click
        if click_type == "Left": pydirectinput.click()
        elif click_type == "Right": pydirectinput.rightClick()
        elif click_type == "Double": pydirectinput.doubleClick()
        elif click_type == "Hold":
            pydirectinput.mouseDown()
            time.sleep(hold_duration or 1.0)
            pydirectinput.mouseUp()
            
    except Exception as e:
        print(f"Click failed: {e}")

def do_keystroke(app, key):
    try:
        pyautogui.press(key)
    except:
        pass