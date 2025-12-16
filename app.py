import tkinter as tk
import sys
from tkinter import messagebox, simpledialog, ttk, filedialog
import os
import threading

# Import the new UI
from ui_layout import AutoClickerUI

# Import Core modules
from core.settings import load_locations, save_locations
from core.groups import init_groups, create_new_group, add_to_group, update_groups_ui
from core.recorder import setup_recorder, start_recording
from core.clicker import start_clicking as core_start_clicking

# Path setup
#_APP_DIR = os.path.dirname(os.path.abspath(__file__))
#_DATA_DIR = os.path.join(_APP_DIR, "Data")

if getattr(sys, 'frozen', False):
    # We are running as an exe
    _APP_DIR = os.path.dirname(sys.executable)
else:
    # We are running as a script
    _APP_DIR = os.path.dirname(os.path.abspath(__file__))

_DATA_DIR = os.path.join(_APP_DIR, "Data")

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("550x700") 
        
        # 1. Init Variables (Create all settings containers)
        self.init_variables()
        
        # 2. Build UI (Now safe to access variables)
        self.ui = AutoClickerUI(self, self.root)
        
        # 3. Init Core features
        self.init_core_features()
        
        # 4. Load Data
        self.load_data()

    def init_variables(self):
        if not os.path.exists(_DATA_DIR):
            os.makedirs(_DATA_DIR)
        
        self.current_profile_path = os.path.join(_DATA_DIR, "click_locations.json")
        self.saved_locations = []
        self.is_recording = False
        self.is_clicking = False
        self.location_counter = 1
        
        # --- Settings Variables ---
        self.interval_var = tk.DoubleVar(value=1.0)
        self.repetitions_var = tk.IntVar(value=1)
        self.infinite_var = tk.BooleanVar(value=False)
        self.random_delay_var = tk.BooleanVar(value=False)
        self.click_order_var = tk.StringVar(value="selection")
        
        self.jitter_enabled = tk.BooleanVar(value=False)
        self.jitter_range = tk.IntVar(value=3)
        
        self.always_on_top = tk.BooleanVar(value=False)
        self.mouse_move_duration = tk.DoubleVar(value=0.5)
        
        self.group_var = tk.StringVar(value="All Groups")
        
        self.hotkeys = {
            "start": "F7",
            "stop": "F8",
            "record": "F6"
        }
        self.is_rebinding = None

    def init_core_features(self):
        init_groups(self)
        setup_recorder(self)
        try:
            from utils.hotkeys import setup_hotkeys
            setup_hotkeys(self)
        except ImportError:
            print("Hotkeys module error.")

    def load_data(self):
        self.saved_locations = load_locations(self.current_profile_path)
        for loc in self.saved_locations:
            name = loc.get("name", "")
            if name.startswith("Location "):
                try:
                    num = int(name.split("Location ")[1])
                    self.location_counter = max(self.location_counter, num + 1)
                except: pass
        self.update_location_list()

    # --- Actions & Logic ---

    def save_profile_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Grimoire Scrolls", "*.json")],
            initialdir=_DATA_DIR,
            title="Scribe New Grimoire"
        )
        if path:
            self.current_profile_path = path
            self.save_and_update()
            messagebox.showinfo("Saved", f"Grimoire scribed to:\n{os.path.basename(path)}")

    def load_profile(self):
        path = filedialog.askopenfilename(
            filetypes=[("Grimoire Scrolls", "*.json")],
            initialdir=_DATA_DIR,
            title="Open Grimoire"
        )
        if path:
            self.current_profile_path = path
            self.load_data()
            messagebox.showinfo("Loaded", f"Opened Grimoire:\n{os.path.basename(path)}")

    def toggle_mini_mode(self):
        if hasattr(self, 'mini_window') and self.mini_window:
            self.mini_window.destroy()
            self.mini_window = None
            self.root.deiconify()
        else:
            self.root.withdraw()
            self.mini_window = tk.Toplevel(self.root)
            self.mini_window.overrideredirect(True)
            self.mini_window.geometry("160x60+100+100")
            self.mini_window.attributes("-topmost", True)
            self.mini_window.attributes("-alpha", 0.9)
            
            # Pass the mini window to UI layout to build it
            drag_bar = self.ui.build_mini_mode(self.mini_window)
            
            def start_move(event):
                self.mini_window.x = event.x
                self.mini_window.y = event.y
            def do_move(event):
                x = self.mini_window.winfo_x() + (event.x - self.mini_window.x)
                y = self.mini_window.winfo_y() + (event.y - self.mini_window.y)
                self.mini_window.geometry(f"+{x}+{y}")
                
            drag_bar.bind("<Button-1>", start_move)
            drag_bar.bind("<B1-Motion>", do_move)

    def rebind_key(self, action):
        self.status_var.set(f"Press ANY key to bind {action.upper()}...")
        self.is_rebinding = action

    def update_location_list(self):
        # FIX: Access location_tree directly on self (attached by UI layout)
        if not hasattr(self, 'location_tree'): return

        for item in self.location_tree.get_children():
            self.location_tree.delete(item)
        
        current_grp = self.group_var.get()
        for loc in self.saved_locations:
            if current_grp != "All Groups" and loc.get("group") != current_grp: continue
            
            name = loc.get("name")
            atype = loc.get("action_type", "click")
            
            if atype == "click":
                x, y = f"{loc.get('x',0)}", f"{loc.get('y',0)}"
                detail = loc.get("click_type", "Left")
                if "Hold" in detail: detail += f" ({loc.get('hold_duration',1)}s)"
            else:
                x, y = "-","-"
                detail = f"Key: {loc.get('key','?')}"
            
            coords = f"{x}, {y}"
            self.location_tree.insert("", tk.END, values=(name, loc.get("group"), coords, detail))
            
        update_groups_ui(self)

    def toggle_recording(self):
        if self.is_recording:
            self.is_recording = False
            # FIX: Access record_button directly on self
            self.record_button.configure(text="● Record") 
            if self.record_listener:
                try: self.record_listener.stop()
                except: pass
            self.status_var.set("Ready")
        else:
            # FIX: Access record_button directly on self
            self.record_button.configure(text="■ Stop Rec")
            start_recording(self)

    def start_clicking(self):
        core_start_clicking(self)

    def stop_clicking(self):
        self.is_clicking = False
        # FIX: Access buttons directly on self
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_var.set("Stopped.")

    def add_keystroke(self):
        key = simpledialog.askstring("Add Key", "Key (e.g. space, enter, a):", parent=self.root)
        if key:
            self.saved_locations.append({
                "name": f"Keystroke {self.location_counter}",
                "action_type": "keystroke",
                "key": key,
                "group": self.group_var.get() if self.group_var.get() != "All Groups" else ""
            })
            self.location_counter += 1
            self.save_and_update()

    def edit_location(self):
        # FIX: Access location_tree directly on self
        sel = self.location_tree.selection()
        if not sel: return
        name = self.location_tree.item(sel[0], "values")[0]
        
        target = next((x for x in self.saved_locations if x["name"] == name), None)
        if not target: return

        # --- Modern Dark Editor ---
        editor = tk.Toplevel(self.root)
        editor.title("Edit Action")
        editor.configure(bg="#18181b")
        editor.geometry("320x420")
        
        pad = tk.Frame(editor, bg="#18181b", padx=20, pady=20)
        pad.pack(fill=tk.BOTH, expand=True)

        def lbl(txt): 
            tk.Label(pad, text=txt, bg="#18181b", fg="#a1a1aa", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 5))
        
        def entry_style(var):
            e = tk.Entry(pad, textvariable=var, bg="#3f3f46", fg="white", insertbackground="white", relief="flat", bd=1)
            e.pack(fill=tk.X, ipady=4)
            return e

        lbl("NAME")
        name_var = tk.StringVar(value=target["name"])
        entry_style(name_var)

        if target.get("action_type", "click") == "click":
            lbl("CLICK TYPE")
            ctype_var = tk.StringVar(value=target.get("click_type", "Left"))
            cb = ttk.Combobox(pad, textvariable=ctype_var, values=["Left", "Right", "Double", "Hold", "Hold Until Stopped"], state="readonly")
            cb.pack(fill=tk.X, ipady=2)
            
            lbl("HOLD DURATION (Seconds)")
            dur_var = tk.DoubleVar(value=target.get("hold_duration", 1.0))
            s = tk.Spinbox(pad, textvariable=dur_var, from_=0.1, to=60.0, increment=0.1, bg="#3f3f46", fg="white", relief="flat", buttonbackground="#27272a")
            s.pack(fill=tk.X, ipady=4)
            
            tk.Label(pad, text="* Only applies if 'Hold' is selected", bg="#18181b", fg="#52525b", font=("Segoe UI", 8)).pack(anchor="w", pady=(2,0))
        else:
            lbl("KEY TO PRESS")
            key_var = tk.StringVar(value=target.get("key", ""))
            entry_style(key_var)

        def save():
            target["name"] = name_var.get()
            if target.get("action_type") == "click":
                target["click_type"] = ctype_var.get()
                target["hold_duration"] = dur_var.get()
            else:
                target["key"] = key_var.get()
            self.save_and_update()
            editor.destroy()
        
        tk.Frame(pad, height=20, bg="#18181b").pack()
        
        btn = tk.Button(pad, text="SAVE CHANGES", command=save, 
                       bg="#15803d", fg="white", 
                       font=("Segoe UI", 9, "bold"), 
                       relief="flat", pady=8, cursor="hand2")
        btn.pack(fill=tk.X)

    def delete_location(self):
        sel = self.location_tree.selection()
        if not sel: return
        names = [self.location_tree.item(i, "values")[0] for i in sel]
        self.saved_locations = [x for x in self.saved_locations if x["name"] not in names]
        self.save_and_update()

    def clear_all_locations(self):
        if messagebox.askyesno("Confirm", "Clear all locations?"):
            self.saved_locations = []
            self.save_and_update()
            
    # Wrappers
    def create_group(self): create_new_group(self)
    def add_selection_to_group(self): add_to_group(self)
    def filter_by_group(self, e): self.update_location_list()
    def save_and_update(self):
        save_locations(self.saved_locations, self.current_profile_path)
        self.update_location_list()
    def update_always_on_top(self): self.root.attributes("-topmost", self.always_on_top.get())