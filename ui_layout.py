import tkinter as tk
from tkinter import ttk, simpledialog
import tkinter.font as tkfont

class AutoClickerUI:
    def __init__(self, root, state, callbacks):
        self.root = root
        self.state = state
        self.callbacks = callbacks
        
        self.root.title("✨ BusTClicker ✨")
        
        # --- The Grimoire Menu ---
        self.build_menu()
        
        # --- Theme: "Eldritch Slate" ---
        self.setup_eldritch_theme()
        self.build_layout()

    def build_menu(self):
        menubar = tk.Menu(self.root, bg="#1c1614", fg="#c0a080", activebackground="#3e2e28", activeforeground="#ffffff", relief="flat")
        file_menu = tk.Menu(menubar, tearoff=0, bg="#1c1614", fg="#c0a080")
        
        file_menu.add_command(label="📜 Open Grimoire...", command=self.callbacks.get("load_profile"))
        file_menu.add_command(label="✒️ Scribe Grimoire As...", command=self.callbacks.get("save_profile_as"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        menubar.add_cascade(label="Grimoire", menu=file_menu)
        self.root.config(menu=menubar)

    def setup_eldritch_theme(self):
        style = ttk.Style()
        style.theme_use('clam')

        # --- Palette: "Ancient Temple" ---
        BG_VOID = "#0f0c0b"
        self.BG_SLATE = "#1c1614"
        BG_INPUT = "#2a221e"
        TEXT_GOLD = "#d4b483"
        TEXT_BRONZE = "#8c7050"
        TEXT_EMBER = "#ff7b00"
        BORDER_GOLD = "#594836"
        BTN_BG = "#2a221e"
        BTN_ACTIVE = "#3e2e28"
        SUCCESS_BG = "#1e3a29"
        DANGER_BG = "#4a1e1e"

        # Fonts
        available_fonts = set(tkfont.families())
        rpg_font = "Palatino Linotype" if "Palatino Linotype" in available_fonts else "Georgia"
        base_font = (rpg_font, 10)
        header_font = (rpg_font, 11, "bold") 

        self.root.configure(bg=BG_VOID)
        
        # Widget Styling
        style.configure(".", background=BG_VOID, foreground=TEXT_GOLD, font=base_font)
        style.configure("TFrame", background=BG_VOID)
        style.configure("TLabelframe", background=self.BG_SLATE, bordercolor=BORDER_GOLD, borderwidth=1, relief="solid")
        style.configure("TLabelframe.Label", background=self.BG_SLATE, foreground=TEXT_BRONZE, font=header_font, padding=(10, 5))
        style.configure("TEntry", fieldbackground=BG_INPUT, foreground=TEXT_GOLD, bordercolor=BORDER_GOLD, padding=5)
        style.configure("TSpinbox", fieldbackground=BG_INPUT, foreground=TEXT_GOLD, arrowcolor=TEXT_GOLD, bordercolor=BORDER_GOLD)
        style.configure("TCombobox", fieldbackground=BG_INPUT, foreground=TEXT_GOLD, arrowcolor=TEXT_GOLD, bordercolor=BORDER_GOLD, padding=5)
        
        style.configure("TButton", background=BTN_BG, foreground=TEXT_GOLD, font=(rpg_font, 10, "bold"), borderwidth=1, bordercolor=BORDER_GOLD, padding=(15, 6))
        style.map("TButton", background=[('active', BTN_ACTIVE), ('pressed', BG_INPUT)], bordercolor=[('active', TEXT_BRONZE)], foreground=[('active', TEXT_EMBER)])

        style.configure("Success.TButton", background=SUCCESS_BG, bordercolor="#2e5c40", foreground="#90ff90")
        style.map("Success.TButton", background=[('active', "#2e5c40")], foreground=[('active', "white")])
        style.configure("Danger.TButton", background=DANGER_BG, bordercolor="#7a2e2e", foreground="#ff9090")
        style.map("Danger.TButton", background=[('active', "#7a2e2e")], foreground=[('active', "white")])

        style.configure("Treeview", background=self.BG_SLATE, fieldbackground=self.BG_SLATE, foreground=TEXT_GOLD, rowheight=28, borderwidth=1, bordercolor=BORDER_GOLD, font=base_font)
        style.configure("Treeview.Heading", background="#0f0c0b", foreground=TEXT_BRONZE, relief="flat", font=header_font, padding=(10, 8))
        style.map("Treeview", background=[('selected', "#3e2e28")], foreground=[('selected', TEXT_EMBER)])
        style.configure("Vertical.TScrollbar", troughcolor=BG_VOID, background=BTN_BG, borderwidth=0, arrowcolor=TEXT_GOLD)

        style.configure("TNotebook", background=BG_VOID, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_VOID, foreground=TEXT_BRONZE, padding=(20, 8), font=header_font, borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", self.BG_SLATE)], foreground=[("selected", TEXT_EMBER)])

    def build_layout(self):
        # Header
        header = tk.Frame(self.root, bg="#0f0c0b", padx=10, pady=15)
        header.pack(fill=tk.X)
        title = tk.Label(header, text="❖ BusTClicker", font=("Georgia", 16, "bold"), bg="#0f0c0b", fg="#d4b483")
        title.pack(side=tk.LEFT, padx=10)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        self.loc_tab = ttk.Frame(self.notebook)
        self.set_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.loc_tab, text="SCROLLS (Sequence)")
        self.notebook.add(self.set_tab, text="RITUALS (Settings)")

        self.build_locations_tab()
        self.build_settings_tab()
        self.build_bottom_controls()

        # Footer Status
        status_frame = tk.Frame(self.root, bg="#1c1614", height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(status_frame, text="✦", bg="#1c1614", fg="#ff7b00", font=("Arial", 10)).pack(side=tk.LEFT, padx=(15, 5))
        tk.Label(status_frame, textvariable=self.state.get("status_msg"), bg="#1c1614", fg="#8c7050", font=("Georgia", 9, "italic")).pack(side=tk.LEFT)

    def build_locations_tab(self):
        container = ttk.Frame(self.loc_tab, padding=15)
        container.pack(fill=tk.BOTH, expand=True)

        actions = ttk.Frame(container)
        actions.pack(fill=tk.X, pady=(0, 15))
        
        self.record_button = ttk.Button(actions, text="◎ Record", command=self.callbacks.get("toggle_recording"))
        self.record_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(actions, text="+ Key", width=8, command=self._prompt_add_key).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(actions, text="Guild:").pack(side=tk.LEFT, padx=(20, 5))
        self.group_dropdown = ttk.Combobox(actions, textvariable=self.state.get("group_filter"), state="readonly", width=15)
        # (Inside build_locations_tab)
        self.group_dropdown.pack(side=tk.LEFT)
        self.group_dropdown.bind("<<ComboboxSelected>>", lambda e: self.refresh_location_list())
        ttk.Button(actions, text="+", width=3, command=self._prompt_create_group).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(actions, text="↓", width=3, command=self._prompt_assign_group).pack(side=tk.LEFT, padx=(5, 0))

        # Treeview Scroll
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        border = tk.Frame(tree_frame, bg="#594836", bd=1)
        border.pack(fill=tk.BOTH, expand=True)
        
        cols = ("Name", "Group", "Coords", "Action")
        self.location_tree = ttk.Treeview(border, columns=cols, show="headings", selectmode="extended")
        
        for col in cols:
            self.location_tree.heading(col, text=col.upper())
        self.location_tree.column("Name", width=140)
        self.location_tree.column("Group", width=80)
        self.location_tree.column("Coords", width=80, anchor="center")
        self.location_tree.column("Action", width=120)
        
        sb = ttk.Scrollbar(border, orient="vertical", command=self.location_tree.yview)
        self.location_tree.configure(yscrollcommand=sb.set)
        self.location_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        tools = ttk.Frame(container)
        tools.pack(fill=tk.X, pady=(15, 0))
        ttk.Button(tools, text="Modify", command=self._trigger_edit).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(tools, text="Banish", command=self._trigger_delete).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(tools, text="Purge All", command=self.callbacks.get("clear_all")).pack(side=tk.RIGHT)

    def build_settings_tab(self):
        container = ttk.Frame(self.set_tab, padding=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        left_col = ttk.Frame(container)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        right_col = ttk.Frame(container)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # --- Left Col: Modes & Sequence ---
        mode_frame = ttk.LabelFrame(left_col, text="OPERATING MODE", padding=15)
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Radiobutton(mode_frame, text="Grimoire Sequence (Scrolls Tab)", variable=self.state.get("operating_mode"), value="sequence").pack(anchor="w", pady=2)
        ttk.Radiobutton(mode_frame, text="Rapid Fire (On-the-spot)", variable=self.state.get("operating_mode"), value="rapid").pack(anchor="w", pady=2)
        cps_frame = ttk.Frame(mode_frame)
        cps_frame.pack(fill=tk.X, pady=(5,0), padx=(20, 0))
        ttk.Label(cps_frame, text="Clicks/Second:").pack(side=tk.LEFT)
        ttk.Spinbox(cps_frame, from_=0.1, to=100.0, increment=1.0, textvariable=self.state.get("cps"), width=8).pack(side=tk.LEFT, padx=5)

        beh_frame = ttk.LabelFrame(left_col, text="SEQUENCE RULES", padding=15)
        beh_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(beh_frame, text="Cooldown (s)").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Spinbox(beh_frame, from_=0.0, to=3600.0, increment=0.1, textvariable=self.state.get("interval"), width=8).grid(row=0, column=1, sticky="e")
        ttk.Label(beh_frame, text="Repetitions").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Spinbox(beh_frame, from_=1, to=9999, textvariable=self.state.get("repetitions"), width=8).grid(row=1, column=1, sticky="e")
        ttk.Checkbutton(beh_frame, text="Eternal Chant (Infinite)", variable=self.state.get("infinite")).grid(row=2, column=0, columnspan=2, sticky="w", pady=5)

        # --- Right Col: Hotkeys & Anti-Cheat ---
        key_frame = ttk.LabelFrame(right_col, text="RUNIC BINDINGS", padding=15)
        key_frame.pack(fill=tk.X, pady=(0, 15))
        
        hotkeys = self.state.get("hotkeys", {"start": "F7", "stop": "F8", "record": "F6"})
        self.btn_bind_start = ttk.Button(key_frame, text=f"Start: {hotkeys.get('start')}", command=lambda: self._trigger_rebind('start'))
        self.btn_bind_start.pack(fill=tk.X, pady=2)
        self.btn_bind_stop = ttk.Button(key_frame, text=f"Stop: {hotkeys.get('stop')}", command=lambda: self._trigger_rebind('stop'))
        self.btn_bind_stop.pack(fill=tk.X, pady=2)
        self.btn_bind_rec = ttk.Button(key_frame, text=f"Record: {hotkeys.get('record')}", command=lambda: self._trigger_rebind('record'))
        self.btn_bind_rec.pack(fill=tk.X, pady=2)

        sys_frame = ttk.LabelFrame(right_col, text="WINDOW AURA", padding=15)
        sys_frame.pack(fill=tk.X)
        ttk.Checkbutton(sys_frame, text="Float Above All", variable=self.state.get("always_on_top")).pack(anchor="w", pady=5)

    def build_bottom_controls(self):
        footer = tk.Frame(self.root, bg="#0f0c0b", padx=20, pady=20)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.start_button = ttk.Button(footer, text="⚔ BEGIN RITUAL", style="Success.TButton", command=self.callbacks.get("start_clicking"))
        self.start_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15), ipady=5)
        
        self.stop_button = ttk.Button(footer, text="✖ CEASE", style="Danger.TButton", command=self.callbacks.get("stop_clicking"), state="disabled")
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 0), ipady=5)

    # --- UI Update Methods (Called by App) ---
    
    def update_playback_buttons(self, clicking: bool):
        if clicking:
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
        else:
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

    def update_record_button(self, recording: bool):
        if recording:
            self.record_button.configure(text="■ Stop Rec")
        else:
            self.record_button.configure(text="◎ Record")

    def refresh_location_list(self):
        for item in self.location_tree.get_children():
            self.location_tree.delete(item)
            
        current_grp = self.state.get("group_filter").get()
        for loc in self.state.get("saved_locations", []):
            if current_grp != "All Groups" and loc.get("group") != current_grp: continue
            
            name = loc.get("name")
            atype = loc.get("action_type", "click")
            
            if atype == "click":
                coords = f"{loc.get('x',0)}, {loc.get('y',0)}"
                detail = loc.get("click_type", "Left")
            else:
                coords = "-, -"
                detail = f"Key: {loc.get('key','?')}"
            
            self.location_tree.insert("", tk.END, values=(name, loc.get("group"), coords, detail))

    def refresh_hotkey_buttons(self):
        """Called by the background listener when a new key is successfully bound."""
        hotkeys = self.state.get("hotkeys", {})
        self.btn_bind_start.configure(text=f"Start: {hotkeys.get('start', 'F7')}")
        self.btn_bind_stop.configure(text=f"Stop: {hotkeys.get('stop', 'F8')}")
        self.btn_bind_rec.configure(text=f"Record: {hotkeys.get('record', 'F6')}")

    # --- Internal UI Events (Passing Data Back to App) ---

    def _trigger_rebind(self, action):
        """Tells the state that we are waiting for a keystroke."""
        self.state["is_rebinding"] = action
        self.state.get("status_msg").set(f"Press ANY key to bind {action.upper()}...")
        
        if action == 'start': self.btn_bind_start.configure(text="Start: [Press Key...]")
        elif action == 'stop': self.btn_bind_stop.configure(text="Stop: [Press Key...]")
        elif action == 'record': self.btn_bind_rec.configure(text="Record: [Press Key...]")

    def _prompt_add_key(self):
        key = simpledialog.askstring("Add Key", "Key (e.g. space, enter, a):", parent=self.root)
        if key and self.callbacks.get("add_keystroke"):
            self.callbacks["add_keystroke"](key)

    def _trigger_delete(self):
        sel = self.location_tree.selection()
        if not sel: return
        names = [self.location_tree.item(i, "values")[0] for i in sel]
        if self.callbacks.get("delete_location"):
            self.callbacks["delete_location"](names)

    def _trigger_edit(self):
        sel = self.location_tree.selection()
        if not sel: return
        item_id = sel[0]
        name = self.location_tree.item(item_id, "values")[0]
        if self.callbacks.get("edit_location"):
            self.callbacks["edit_location"](item_id, name)

    # --- Popups ---

    def open_editor_window(self, target_data, on_save_callback):
        editor = tk.Toplevel(self.root)
        editor.title("Scribe Action")
        editor.configure(bg=self.BG_SLATE)
        editor.geometry("320x420")
        
        pad = tk.Frame(editor, bg=self.BG_SLATE, padx=20, pady=20)
        pad.pack(fill=tk.BOTH, expand=True)

        def lbl(txt): 
            tk.Label(pad, text=txt, bg=self.BG_SLATE, fg="#8c7050", font=("Georgia", 9, "bold")).pack(anchor="w", pady=(10, 5))

        lbl("NAME")
        name_var = tk.StringVar(value=target_data.get("name", ""))
        ttk.Entry(pad, textvariable=name_var).pack(fill=tk.X)

        ctype_var = tk.StringVar()
        key_var = tk.StringVar()
        
        if target_data.get("action_type", "click") == "click":
            lbl("CLICK TYPE")
            ctype_var.set(target_data.get("click_type", "Left"))
            ttk.Combobox(pad, textvariable=ctype_var, values=["Left", "Right", "Double", "Hold"], state="readonly").pack(fill=tk.X)
        else:
            lbl("KEY TO PRESS")
            key_var.set(target_data.get("key", ""))
            ttk.Entry(pad, textvariable=key_var).pack(fill=tk.X)

        def save():
            updated = {"name": name_var.get()}
            if target_data.get("action_type") == "click":
                updated["click_type"] = ctype_var.get()
            else:
                updated["key"] = key_var.get()
                
            on_save_callback(updated)
            editor.destroy()
        
        tk.Frame(pad, height=20, bg=self.BG_SLATE).pack()
        ttk.Button(pad, text="Scribe Changes", command=save).pack(fill=tk.X)
    
    def refresh_groups_dropdown(self):
        """Reads the state and updates the dropdown choices."""
        from core.groups import get_all_groups
        groups = ["All Groups"] + get_all_groups(self.state)
        self.group_dropdown['values'] = groups

    def _prompt_create_group(self):
        """Pops a Tkinter dialog to ask for the group name."""
        group_name = simpledialog.askstring("New Guild", "Enter guild name:", parent=self.root)
        if group_name and self.callbacks.get("create_group"):
            if self.callbacks["create_group"](group_name):
                self.state.get("group_filter").set(group_name)
                self.refresh_location_list()

    def _prompt_assign_group(self):
        """Pops a clean dialog to ask which group to assign the highlighted items to."""
        sel = self.location_tree.selection()
        if not sel: 
            tk.messagebox.showinfo("Guild Assignment", "Please select at least one scroll from the list first.")
            return
            
        names = [self.location_tree.item(i, "values")[0] for i in sel]

        # Grab groups from the dropdown, excluding the default "All Groups"
        available_groups = [g for g in self.group_dropdown['values'] if g != "All Groups"]
        
        if not available_groups:
            tk.messagebox.showinfo("No Guilds", "You don't have any Guilds yet! Create one using the '+' button.")
            return

        # Build a tiny, themed dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Assign Guild")
        dialog.configure(bg=self.BG_SLATE)
        dialog.geometry("250x150")
        dialog.transient(self.root)
        dialog.grab_set() # Forces the user to deal with this popup before clicking away
        
        pad = tk.Frame(dialog, bg=self.BG_SLATE, padx=20, pady=20)
        pad.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(pad, text="Select Guild:", bg=self.BG_SLATE, fg="#8c7050", font=("Georgia", 9, "bold")).pack(anchor="w", pady=(0, 5))
        
        group_var = tk.StringVar(value=available_groups[0])
        cb = ttk.Combobox(pad, textvariable=group_var, values=available_groups, state="readonly")
        cb.pack(fill=tk.X, pady=(0, 15))
        
        def on_confirm():
            target_group = group_var.get()
            if target_group and self.callbacks.get("assign_to_group"):
                self.callbacks["assign_to_group"](names, target_group)
                self.state.get("status_msg").set(f"Assigned {len(names)} scrolls to {target_group}")
            dialog.destroy()
            
        ttk.Button(pad, text="Scribe to Guild", command=on_confirm).pack(fill=tk.X)