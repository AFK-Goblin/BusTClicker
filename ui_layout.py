import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

class AutoClickerUI:
    def __init__(self, app, root):
        self.app = app
        self.root = root
        self.root.title("✨ BusTClicker ✨")
        
        # --- The Grimoire Menu ---
        self.build_menu()
        
        # --- Theme: "Eldritch Slate" ---
        self.setup_eldritch_theme()
        self.build_layout()

    def build_menu(self):
        # Menu colors to match the dark theme
        menubar = tk.Menu(self.root, bg="#1c1614", fg="#c0a080", activebackground="#3e2e28", activeforeground="#ffffff", relief="flat")
        
        file_menu = tk.Menu(menubar, tearoff=0, bg="#1c1614", fg="#c0a080")
        file_menu.add_command(label="📜 Open Grimoire...", command=self.app.load_profile)
        file_menu.add_command(label="✒️ Scribe Grimoire As...", command=self.app.save_profile_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        menubar.add_cascade(label="Grimoire", menu=file_menu)
        self.root.config(menu=menubar)

    def setup_eldritch_theme(self):
        style = ttk.Style()
        style.theme_use('clam')

        # --- Palette: "Ancient Temple" ---
        BG_VOID = "#0f0c0b"       # Deepest Black (Window BG)
        BG_SLATE = "#1c1614"      # Dark Stone (Panels)
        BG_INPUT = "#2a221e"      # Lighter Stone (Inputs)
        
        TEXT_GOLD = "#d4b483"     # Faded Gold (Primary Text)
        TEXT_BRONZE = "#8c7050"   # Dark Bronze (Secondary)
        TEXT_EMBER = "#ff7b00"    # Glowing Orange (Active/Focus)
        
        BORDER_GOLD = "#594836"   # Subtle Gold Border
        BORDER_ACTIVE = "#8c7050" # Brighter Border
        
        # Button Gradients (Simulated via colors)
        BTN_BG = "#2a221e"
        BTN_ACTIVE = "#3e2e28"
        
        SUCCESS_BG = "#1e3a29"    # Forest Magic
        DANGER_BG = "#4a1e1e"     # Blood Magic

        # --- Fonts ---
        # Palatino/Georgia for that "RPG" feel, Segoe for readability
        available_fonts = set(tkfont.families())
        rpg_font = "Palatino Linotype" if "Palatino Linotype" in available_fonts else "Georgia"
        
        base_font = (rpg_font, 10)
        header_font = (rpg_font, 11, "bold") 
        title_font = (rpg_font, 14, "bold")

        self.root.configure(bg=BG_VOID)
        
        # --- Widget Styling ---
        
        # 1. Backgrounds
        style.configure(".", background=BG_VOID, foreground=TEXT_GOLD, font=base_font)
        style.configure("TFrame", background=BG_VOID)
        
        # 2. Panels (Stone Slabs)
        style.configure("TLabelframe", background=BG_SLATE, bordercolor=BORDER_GOLD, borderwidth=1, relief="solid")
        style.configure("TLabelframe.Label", background=BG_SLATE, foreground=TEXT_BRONZE, font=header_font, padding=(10, 5))
        
        # 3. Inputs (Inlaid Stone)
        style.configure("TEntry", fieldbackground=BG_INPUT, foreground=TEXT_GOLD, bordercolor=BORDER_GOLD, padding=5)
        style.configure("TSpinbox", fieldbackground=BG_INPUT, foreground=TEXT_GOLD, arrowcolor=TEXT_GOLD, bordercolor=BORDER_GOLD)
        style.configure("TCombobox", fieldbackground=BG_INPUT, foreground=TEXT_GOLD, arrowcolor=TEXT_GOLD, bordercolor=BORDER_GOLD, padding=5)
        
        # 4. Buttons (Runestones)
        style.configure("TButton", 
                        background=BTN_BG, 
                        foreground=TEXT_GOLD, 
                        font=(rpg_font, 10, "bold"), 
                        borderwidth=1, 
                        bordercolor=BORDER_GOLD,
                        padding=(15, 6))
        
        style.map("TButton", 
                  background=[('active', BTN_ACTIVE), ('pressed', BG_INPUT)],
                  bordercolor=[('active', TEXT_BRONZE)],
                  foreground=[('active', TEXT_EMBER)])

        # Special Buttons (Glowing Runes)
        style.configure("Success.TButton", background=SUCCESS_BG, bordercolor="#2e5c40", foreground="#90ff90")
        style.map("Success.TButton", background=[('active', "#2e5c40")], foreground=[('active', "white")])
        
        style.configure("Danger.TButton", background=DANGER_BG, bordercolor="#7a2e2e", foreground="#ff9090")
        style.map("Danger.TButton", background=[('active', "#7a2e2e")], foreground=[('active', "white")])

        # 5. The Scroll (List)
        style.configure("Treeview", 
                        background=BG_SLATE, 
                        fieldbackground=BG_SLATE, 
                        foreground=TEXT_GOLD, 
                        rowheight=28, 
                        borderwidth=1,
                        bordercolor=BORDER_GOLD,
                        font=base_font)
                        
        style.configure("Treeview.Heading", 
                        background="#0f0c0b", 
                        foreground=TEXT_BRONZE, 
                        relief="flat", 
                        font=header_font,
                        padding=(10, 8))
                        
        style.map("Treeview", background=[('selected', "#3e2e28")], foreground=[('selected', TEXT_EMBER)])
        
        # Scrollbar (Bronze)
        style.configure("Vertical.TScrollbar", troughcolor=BG_VOID, background=BTN_BG, borderwidth=0, arrowcolor=TEXT_GOLD)

        # 6. Notebook (Tabs)
        style.configure("TNotebook", background=BG_VOID, borderwidth=0)
        style.configure("TNotebook.Tab", 
                        background=BG_VOID, 
                        foreground=TEXT_BRONZE, 
                        padding=(20, 8), 
                        font=header_font,
                        borderwidth=0)
                        
        style.map("TNotebook.Tab", 
                  background=[("selected", BG_SLATE)], 
                  foreground=[("selected", TEXT_EMBER)])

    def build_layout(self):
        # Header
        header = tk.Frame(self.root, bg="#0f0c0b", padx=10, pady=15)
        header.pack(fill=tk.X)
        
        # Title with Gold text
        title = tk.Label(header, text="❖ BusTClicker", font=("Georgia", 16, "bold"), bg="#0f0c0b", fg="#d4b483")
        title.pack(side=tk.LEFT, padx=10)
        
        # Mini Mode Button
        ttk.Button(header, text="🔮 Mini Sphere", width=12, command=self.app.toggle_mini_mode).pack(side=tk.RIGHT, padx=10)

        # Main Layout
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        self.loc_tab = ttk.Frame(self.notebook)
        self.set_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.loc_tab, text="SCROLLS")
        self.notebook.add(self.set_tab, text="RITUALS")

        self.build_locations_tab()
        self.build_settings_tab()
        self.build_bottom_controls()

        # Footer Status
        self.app.status_var = tk.StringVar(value="Magic flows...")
        status_frame = tk.Frame(self.root, bg="#1c1614", height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Glowing Dot
        tk.Label(status_frame, text="✦", bg="#1c1614", fg="#ff7b00", font=("Arial", 10)).pack(side=tk.LEFT, padx=(15, 5))
        tk.Label(status_frame, textvariable=self.app.status_var, bg="#1c1614", fg="#8c7050", font=("Georgia", 9, "italic")).pack(side=tk.LEFT)

    def build_locations_tab(self):
        container = ttk.Frame(self.loc_tab, padding=15)
        container.pack(fill=tk.BOTH, expand=True)

        # 1. Action Bar (Top)
        actions = ttk.Frame(container)
        actions.pack(fill=tk.X, pady=(0, 15))
        
        # Use symbols for buttons
        self.app.record_button = ttk.Button(actions, text="◎ Record", command=self.app.toggle_recording)
        self.app.record_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(actions, text="+ Key", width=8, command=self.app.add_keystroke).pack(side=tk.LEFT, padx=(0, 10))
        
        # Group Filter
        ttk.Label(actions, text="Guild:").pack(side=tk.LEFT, padx=(20, 5))
        self.app.group_var = tk.StringVar(value="All Groups")
        self.app.group_dropdown = ttk.Combobox(actions, textvariable=self.app.group_var, state="readonly", width=15)
        self.app.group_dropdown.pack(side=tk.LEFT)
        self.app.group_dropdown.bind("<<ComboboxSelected>>", self.app.filter_by_group)

        # Tiny Group Buttons
        ttk.Button(actions, text="+", width=3, command=lambda: self.app.create_group()).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(actions, text="↓", width=3, command=lambda: self.app.add_selection_to_group()).pack(side=tk.LEFT, padx=(5, 0))

        # 2. Main Scroll (List)
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Gold border wrapper
        border = tk.Frame(tree_frame, bg="#594836", bd=1)
        border.pack(fill=tk.BOTH, expand=True)
        
        cols = ("Name", "Group", "Coords", "Action")
        self.app.location_tree = ttk.Treeview(border, columns=cols, show="headings", selectmode="extended")
        
        self.app.location_tree.heading("Name", text="NAME")
        self.app.location_tree.heading("Group", text="GUILD")
        self.app.location_tree.heading("Coords", text="LOC")
        self.app.location_tree.heading("Action", text="SPELL")
        
        self.app.location_tree.column("Name", width=140)
        self.app.location_tree.column("Group", width=80)
        self.app.location_tree.column("Coords", width=80, anchor="center")
        self.app.location_tree.column("Action", width=120)
        
        sb = ttk.Scrollbar(border, orient="vertical", command=self.app.location_tree.yview)
        self.app.location_tree.configure(yscrollcommand=sb.set)
        
        self.app.location_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        # 3. Bottom Tools
        tools = ttk.Frame(container)
        tools.pack(fill=tk.X, pady=(15, 0))
        
        ttk.Button(tools, text="Modify", command=self.app.edit_location).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(tools, text="Banish", command=self.app.delete_location).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(tools, text="Purge All", command=self.app.clear_all_locations).pack(side=tk.RIGHT)

    def build_settings_tab(self):
        container = ttk.Frame(self.set_tab, padding=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        left_col = ttk.Frame(container)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_col = ttk.Frame(container)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # --- Left: Magic Logic ---
        beh_frame = ttk.LabelFrame(left_col, text="CASTING RULES", padding=15)
        beh_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(beh_frame, text="Cooldown (s)").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Spinbox(beh_frame, from_=0.0, to=3600.0, increment=0.1, textvariable=self.app.interval_var, width=8).grid(row=0, column=1, sticky="e")
        
        ttk.Label(beh_frame, text="Repetitions").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Spinbox(beh_frame, from_=1, to=9999, textvariable=self.app.repetitions_var, width=8).grid(row=1, column=1, sticky="e")
        
        # Separation Line
        tk.Frame(beh_frame, height=1, bg="#594836").grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        
        ttk.Checkbutton(beh_frame, text="Eternal Chant (Infinite)", variable=self.app.infinite_var).grid(row=3, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(beh_frame, text="Chaos Delay (±0.5s)", variable=self.app.random_delay_var).grid(row=4, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(beh_frame, text="Ordered Casting", variable=self.app.click_order_var, onvalue="selection", offvalue="all").grid(row=5, column=0, columnspan=2, sticky="w", pady=2)

        # --- Anti-Cheat ---
        jit_frame = ttk.LabelFrame(left_col, text="STEALTH MAGIC", padding=15)
        jit_frame.pack(fill=tk.X)
        
        ttk.Checkbutton(jit_frame, text="Spirit Jitter (Anti-Ban)", variable=self.app.jitter_enabled).pack(anchor="w", pady=(0, 10))
        
        f = ttk.Frame(jit_frame)
        f.pack(fill=tk.X)
        ttk.Label(f, text="Wander Radius:").pack(side=tk.LEFT)
        ttk.Spinbox(f, from_=1, to=50, textvariable=self.app.jitter_range, width=5).pack(side=tk.RIGHT)

        # --- Right: Bindings ---
        key_frame = ttk.LabelFrame(right_col, text="RUNIC BINDINGS", padding=15)
        key_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.app.btn_bind_start = ttk.Button(key_frame, text=f"Start: {self.app.hotkeys['start']}", command=lambda: self.app.rebind_key('start'))
        self.app.btn_bind_start.pack(fill=tk.X, pady=2)
        
        self.app.btn_bind_stop = ttk.Button(key_frame, text=f"Stop: {self.app.hotkeys['stop']}", command=lambda: self.app.rebind_key('stop'))
        self.app.btn_bind_stop.pack(fill=tk.X, pady=2)
        
        self.app.btn_bind_rec = ttk.Button(key_frame, text=f"Record: {self.app.hotkeys['record']}", command=lambda: self.app.rebind_key('record'))
        self.app.btn_bind_rec.pack(fill=tk.X, pady=2)

        # System
        sys_frame = ttk.LabelFrame(right_col, text="WINDOW AURA", padding=15)
        sys_frame.pack(fill=tk.X)
        ttk.Checkbutton(sys_frame, text="Float Above All", variable=self.app.always_on_top, command=self.app.update_always_on_top).pack(anchor="w", pady=5)
        ttk.Label(sys_frame, text="Travel Speed:").pack(anchor="w", pady=(5,0))
        ttk.Spinbox(sys_frame, from_=0.0, to=5.0, increment=0.1, textvariable=self.app.mouse_move_duration).pack(fill=tk.X)

    def build_bottom_controls(self):
        footer = tk.Frame(self.root, bg="#0f0c0b", padx=20, pady=20)
        footer.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.app.start_button = ttk.Button(footer, text="⚔ BEGIN RITUAL", style="Success.TButton", command=self.app.start_clicking)
        self.app.start_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15), ipady=5)
        
        self.app.stop_button = ttk.Button(footer, text="✖ CEASE", style="Danger.TButton", command=self.app.stop_clicking, state="disabled")
        self.app.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(15, 0), ipady=5)

    def build_mini_mode(self, mini_window):
        # Mini Sphere Layout
        mini_window.configure(bg="#0f0c0b")
        
        # Bronze Drag Bar
        drag_bar = tk.Frame(mini_window, bg="#594836", height=18)
        drag_bar.pack(fill=tk.X)
        tk.Label(drag_bar, text="✦", bg="#594836", fg="#d4b483", font=("Arial", 8)).pack()
        
        content = tk.Frame(mini_window, bg="#0f0c0b", padx=5, pady=5)
        content.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(content, text="⚔", width=4, style="Success.TButton", command=self.app.start_clicking).pack(side=tk.LEFT, padx=3)
        ttk.Button(content, text="✖", width=4, style="Danger.TButton", command=self.app.stop_clicking).pack(side=tk.LEFT, padx=3)
        ttk.Button(content, text="⤢", width=4, command=self.app.toggle_mini_mode).pack(side=tk.LEFT, padx=3)
        
        return drag_bar