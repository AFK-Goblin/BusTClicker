import tkinter as tk
import sys
import os
from tkinter import messagebox, filedialog

# Import the UI
from ui_layout import AutoClickerUI

# Import Core modules
from core.settings import load_locations, save_locations
from core.groups import init_groups, create_new_group, assign_to_group, get_all_groups
from core.recorder import setup_recorder, start_recording
from core.clicker import start_sequence_clicking, start_rapid_clicking, stop_clicking 

if getattr(sys, 'frozen', False):
    # Running as an executable
    _APP_DIR = os.path.dirname(sys.executable)
else:
    # Running as a python script
    _APP_DIR = os.path.dirname(os.path.abspath(__file__))

_DATA_DIR = os.path.join(_APP_DIR, "Data")

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("550x700") 
        self.root.title("Auto Scribe")
        
        # 1. State Management
        self.init_state()
        
        # 2. Build UI via Callback Pattern
        self.ui = AutoClickerUI(self.root, state=self.state, callbacks={
            "save_profile_as": self.save_profile_as,
            "load_profile": self.load_profile,
            "toggle_recording": self.toggle_recording,
            "start_clicking": self.start_clicking,
            "stop_clicking": self.stop_clicking,
            "add_keystroke": self.add_keystroke,
            "edit_location": self.edit_location,
            "delete_location": self.delete_location,
            "clear_all": self.clear_all_locations,
            "trigger_auto_save": self.auto_save,
            "create_group": self.create_group,      # New group wiring
            "assign_to_group": self.assign_to_group # New group wiring
        })
        
        # 3. Init Core features
        self.init_core_features()
        
        # 4. Load Data & Ensure save on exit
        self.load_data()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def init_state(self):
        """Consolidates all app variables into a clean state object."""
        if not os.path.exists(_DATA_DIR):
            os.makedirs(_DATA_DIR)
        
        self.current_profile_path = os.path.join(_DATA_DIR, "click_locations.json")
        
        self.state = {
            "saved_locations": [],
            "location_counter": 1,
            "is_recording": False,
            "is_clicking": False,
            
            # --- Operating Modes ---
            "operating_mode": tk.StringVar(value="sequence"), # "sequence" or "rapid"
            "cps": tk.DoubleVar(value=10.0), # Clicks Per Second for rapid mode
            
            # --- Sequence Settings ---
            "interval": tk.DoubleVar(value=1.0),
            "repetitions": tk.IntVar(value=1),
            "infinite": tk.BooleanVar(value=False),
            "group_filter": tk.StringVar(value="All Groups"),
            
            # --- Stealth & System ---
            "jitter_enabled": tk.BooleanVar(value=False),
            "jitter_range": tk.IntVar(value=3),
            "always_on_top": tk.BooleanVar(value=False),
            "mouse_move_duration": tk.DoubleVar(value=0.5),
            
            "status_msg": tk.StringVar(value="Ready."),
            "hotkeys": {"start": "F7", "stop": "F8", "record": "F6"},
            "is_rebinding": None
        }
        
        # Trace 'always on top' to auto-apply when changed
        self.state["always_on_top"].trace_add("write", self._apply_window_rules)

    def init_core_features(self):
        """Sets up headless core logic."""
        init_groups(self.state)
        setup_recorder(self)
        try:
            from utils.hotkeys import setup_hotkeys
            setup_hotkeys(self)
        except ImportError as e:
            print(f"Hotkey initialization failed: {e}")

    # --- File & Data Management ---

    def load_data(self):
        """Loads data with proper error handling."""
        try:
            self.state["saved_locations"] = load_locations(self.current_profile_path)
            self._update_counter_from_data()
            self.ui.refresh_groups_dropdown()
            self.ui.refresh_location_list()
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to read Grimoire:\n{e}")

    def auto_save(self, *args):
        """Silently saves the current state."""
        try:
            save_locations(self.state["saved_locations"], self.current_profile_path)
        except Exception as e:
            print(f"Auto-save failed: {e}")

    def save_profile_as(self):
        """Explicitly save to a new file."""
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Grimoire Scrolls", "*.json")],
            initialdir=_DATA_DIR,
            title="Scribe New Grimoire"
        )
        if path:
            self.current_profile_path = path
            self.auto_save()
            messagebox.showinfo("Saved", f"Grimoire scribed to:\n{os.path.basename(path)}")
            
    def load_profile(self):
        """Explicitly load a new file."""
        path = filedialog.askopenfilename(
            filetypes=[("Grimoire Scrolls", "*.json")],
            initialdir=_DATA_DIR,
            title="Open Grimoire"
        )
        if path:
            self.current_profile_path = path
            self.load_data()
            messagebox.showinfo("Loaded", f"Opened Grimoire:\n{os.path.basename(path)}")

    def on_closing(self):
        """Ensures final state is saved before exit."""
        self.auto_save()
        self.root.destroy()

    # --- Actions & Logic ---

    def start_clicking(self):
        if self.state["is_clicking"]: return
        
        self.state["is_clicking"] = True
        self.ui.update_playback_buttons(clicking=True)
        
        # Route based on the new mode toggle
        if self.state["operating_mode"].get() == "rapid":
            start_rapid_clicking(self.state["cps"])
            self.state["status_msg"].set(f"Rapid Fire: {self.state['cps'].get()} CPS")
        else:
            start_sequence_clicking(self.state)
            self.state["status_msg"].set("Executing Sequence...")

    def stop_clicking(self):
        if not self.state["is_clicking"]: return
        
        self.state["is_clicking"] = False
        stop_clicking() # Halts whichever core process is running
        self.ui.update_playback_buttons(clicking=False)
        self.state["status_msg"].set("Stopped.")

    def toggle_recording(self):
        if self.state["is_recording"]:
            self.state["is_recording"] = False
            self.ui.update_record_button(recording=False)
            self.state["status_msg"].set("Recording stopped.")
        else:
            self.state["is_recording"] = True
            self.ui.update_record_button(recording=True)
            start_recording(self)

    # --- Location & Group Management ---

    def create_group(self, group_name):
        """Passes group creation to core logic and triggers saves."""
        if create_new_group(self.state, group_name):
            self.auto_save()
            self.ui.refresh_groups_dropdown() 
            return True
        return False

    def assign_to_group(self, location_names, group_name):
        """Assigns selected scrolls to a group."""
        count = assign_to_group(self.state, location_names, group_name)
        if count > 0:
            self.auto_save()
            self.ui.refresh_location_list()
        return count

    def edit_location(self, item_id, location_name):
        """Controller logic for editing. Asks UI to open the window, providing a save callback."""
        target = next((x for x in self.state["saved_locations"] if x["name"] == location_name), None)
        if not target: return

        def on_save_edit(updated_data):
            target.update(updated_data)
            self.auto_save()
            self.ui.refresh_location_list()
            
        self.ui.open_editor_window(target, on_save_edit)

    def delete_location(self, location_names):
        self.state["saved_locations"] = [x for x in self.state["saved_locations"] if x["name"] not in location_names]
        self.auto_save()
        self.ui.refresh_location_list()

    def clear_all_locations(self):
        if messagebox.askyesno("Confirm", "Clear all locations?"):
            self.state["saved_locations"] = []
            self.auto_save()
            self.ui.refresh_location_list()

    def add_keystroke(self, key_string):
        """Called by the UI when a user enters a keystroke."""
        grp = self.state["group_filter"].get()
        self.state["saved_locations"].append({
            "name": f"Keystroke {self.state['location_counter']}",
            "action_type": "keystroke",
            "key": key_string,
            "group": grp if grp != "All Groups" else ""
        })
        self.state["location_counter"] += 1
        self.auto_save()
        self.ui.refresh_location_list()

    # --- Helpers ---

    def _apply_window_rules(self, *args):
        self.root.attributes("-topmost", self.state["always_on_top"].get())
        
    def _update_counter_from_data(self):
        for loc in self.state["saved_locations"]:
            name = loc.get("name", "")
            if name.startswith("Location ") or name.startswith("Keystroke "):
                try:
                    num = int(name.split(" ")[-1])
                    self.state["location_counter"] = max(self.state["location_counter"], num + 1)
                except ValueError: pass