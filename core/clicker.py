import threading
import time
import random
from tkinter import messagebox

try:
    import pyautogui
    import pydirectinput
except ImportError:
    print("Mouse modules missing. Please run: pip install pyautogui pydirectinput")

# Use a global Event to safely and instantly stop background threads
_stop_event = threading.Event()

def start_sequence_clicking(state):
    """Executes the planned out Grimoire Scrolls."""
    if not state.get("saved_locations"):
        messagebox.showinfo("Empty Scroll", "Your Grimoire is empty! Record or add locations first.")
        # We assume app.py handles resetting the UI buttons if this fails
        return
        
    _stop_event.clear()
    thread = threading.Thread(target=_perform_sequence, args=(state,))
    thread.daemon = True
    thread.start()

def start_rapid_clicking(cps_var):
    """Executes extremely fast, on-the-spot clicking based on CPS."""
    _stop_event.clear()
    
    # Extract the raw float value from the Tkinter DoubleVar
    try:
        cps = float(cps_var.get())
    except:
        cps = 10.0

    thread = threading.Thread(target=_perform_rapid, args=(cps,))
    thread.daemon = True
    thread.start()

def stop_clicking():
    """Instantly flags all clicking threads to halt."""
    _stop_event.set()

# --- Internal Thread Logic ---

def _perform_rapid(cps):
    try:
        # Prevent division by zero
        target_delay = 1.0 / max(0.1, cps) 
        
        while not _stop_event.is_set():
            pydirectinput.click()
            
            # Anti-Ban Micro-Jitter: Fluctuates the delay by ±10% 
            # so it isn't flagged as perfect robotic input
            humanized_delay = target_delay + random.uniform(-target_delay * 0.1, target_delay * 0.1)
            
            # Sleep in tiny chunks so we can interrupt it instantly if stop is pressed
            _interruptible_sleep(humanized_delay)
            
    except Exception as e:
        print(f"Rapid fire interrupted: {e}")

def _perform_sequence(state):
    try:
        interval = state.get("interval").get()
        is_infinite = state.get("infinite").get()
        reps = state.get("repetitions").get() if not is_infinite else float('inf')
        
        # Safely fetch optional state variables
        random_delay_var = state.get("random_delay_var")
        has_random_delay = random_delay_var.get() if random_delay_var else False
        
        grp = state.get("group_filter").get()
        actions = state.get("saved_locations", [])
        
        if grp != "All Groups":
            actions = [x for x in actions if x.get("group") == grp]
            
        count = 0
        while not _stop_event.is_set() and count < reps:
            for loc in actions:
                if _stop_event.is_set(): break
                
                atype = loc.get("action_type", "click")
                if atype == "click":
                    hold = loc.get("hold_duration", 1.0) if "Hold" in loc.get("click_type") else None
                    _do_click(state, loc.get("x", 0), loc.get("y", 0), loc.get("click_type", "Left"), hold)
                elif atype == "keystroke":
                    _do_keystroke(loc.get("key"))
                
                # Sequence Delays
                wait = interval
                if has_random_delay: 
                    wait += random.uniform(-0.5, 0.5)
                _interruptible_sleep(max(0.01, wait))
                
            count += 1
            
    except Exception as e:
        print(f"Sequence error: {e}")

def _do_click(state, x, y, click_type, hold_duration=None):
    try:
        final_x, final_y = int(x), int(y)
        
        # --- SPIRIT JITTER LOGIC ---
        jitter_var = state.get("jitter_enabled")
        if jitter_var and jitter_var.get():
            r_var = state.get("jitter_range")
            r = r_var.get() if r_var else 3
            final_x += random.randint(-r, r)
            final_y += random.randint(-r, r)
            
        # Move Sequence
        move_var = state.get("mouse_move_duration")
        duration = move_var.get() if move_var else 0.5
        
        if duration > 0:
            cur_x, cur_y = pyautogui.position()
            steps = int(max(5, duration * 20))
            
            for i in range(steps):
                if _stop_event.is_set(): return # Break out immediately
                nx = int(cur_x + (final_x - cur_x) * ((i+1)/steps))
                ny = int(cur_y + (final_y - cur_y) * ((i+1)/steps))
                pydirectinput.moveTo(nx, ny)
                time.sleep(duration/steps)
                
        pydirectinput.moveTo(final_x, final_y)
        if _stop_event.is_set(): return
        
        # Click Execution
        if click_type == "Left": pydirectinput.click()
        elif click_type == "Right": pydirectinput.rightClick()
        elif click_type == "Double": pydirectinput.doubleClick()
        elif click_type == "Hold":
            pydirectinput.mouseDown()
            _interruptible_sleep(hold_duration or 1.0)
            pydirectinput.mouseUp()
            
    except Exception as e:
        print(f"Click execution failed: {e}")

def _do_keystroke(key):
    if _stop_event.is_set(): return
    try:
        pyautogui.press(key)
    except:
        pass

def _interruptible_sleep(duration):
    """Sleeps in 0.05s chunks so the thread can exit instantly if Stop is pressed."""
    elapsed = 0
    while elapsed < duration:
        if _stop_event.is_set(): break
        sleep_chunk = min(0.05, duration - elapsed)
        time.sleep(sleep_chunk)
        elapsed += sleep_chunk