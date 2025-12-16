import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

# Set to track empty groups
EMPTY_GROUPS = set()

def init_groups(app):
    """Initialize the groups system for the application"""
    # This is called after UI is created to set up any group-related functionality
    
    # Initialize empty groups set if not already initialized
    if not hasattr(app, 'empty_groups'):
        app.empty_groups = EMPTY_GROUPS
    
    # Update the dropdown with existing groups
    if hasattr(app, 'group_dropdown'):
        update_groups_ui(app)

def update_groups_ui(app):
    """Update the groups UI elements with current group data"""
    if hasattr(app, 'group_dropdown'):
        # Get all current groups and update the dropdown
        groups = ["All Groups"] + get_all_groups(app)
        app.group_dropdown['values'] = groups
        
        # Preserve current selection if possible
        current_group = app.group_var.get()
        if current_group not in groups:
            app.group_var.set("All Groups")

def get_all_groups(app):
    """Get a list of all groups defined in the saved locations and empty groups"""
    # Get groups from saved locations
    groups = set()
    for loc in app.saved_locations:
        if "group" in loc and loc["group"]:
            groups.add(loc["group"])
    
    # Add empty groups
    if hasattr(app, 'empty_groups'):
        groups.update(app.empty_groups)
    
    return list(sorted(groups))

def create_new_group(app, callback=None):
    """Create a new action group with optional callback after creation"""
    group_name = simpledialog.askstring("New Group", "Enter group name:", parent=app.root)
    
    if not group_name or group_name.strip() == "":
        return None
    
    # Check if the group already exists
    current_groups = get_all_groups(app)
    if group_name in current_groups:
        messagebox.showerror("Error", f"Group '{group_name}' already exists")
        return None
    
    # Add to empty groups (it will be empty initially)
    if not hasattr(app, 'empty_groups'):
        app.empty_groups = set()
    app.empty_groups.add(group_name)
    
    # Add to the dropdown
    groups = list(app.group_dropdown['values'])
    if group_name not in groups:
        groups.append(group_name)
        app.group_dropdown['values'] = groups
    
    # Set the current filter to the new group
    app.group_var.set(group_name)
    app.update_location_list()
    
    messagebox.showinfo("Success", f"Group '{group_name}' created")
    
    # If a callback was provided, call it with the new group name
    if callback:
        callback(group_name)
        
    return group_name

def add_to_group(app):
    """Add selected locations to a group"""
    print("Add to group function called")
    
    selected = app.location_tree.selection()
    if not selected:
        messagebox.showinfo("Info", "Please select locations to add to a group")
        return
    
    # Get selected item names now
    selected_names = []
    for item in selected:
        values = app.location_tree.item(item, "values")
        if values:
            selected_names.append(values[0])
    
    print(f"Selected items: {selected_names}")
    
    # Get all available groups
    groups = get_all_groups(app)
    print(f"Available groups: {groups}")
    
    if not groups:
        # Define a callback to handle adding items after group creation
        def add_items_to_new_group(group_name):
            if not group_name:
                return
                
            print(f"Callback - adding items to new group: {group_name}")
            # Add the selected items to the newly created group
            count = 0
            for i in range(len(app.saved_locations)):
                if app.saved_locations[i]["name"] in selected_names:
                    print(f"Adding {app.saved_locations[i]['name']} to group {group_name}")
                    app.saved_locations[i]["group"] = group_name
                    count += 1
            
            print(f"Added {count} items to new group {group_name}")
            
            # Group is no longer empty
            if hasattr(app, 'empty_groups') and group_name in app.empty_groups:
                app.empty_groups.remove(group_name)
            
            # Save and update UI
            from core.settings import save_locations
            save_locations(app.saved_locations, app.config_file)
            app.update_location_list()
            
        # Ask to create a group first and pass the callback
        if messagebox.askyesno("No Groups", "No groups exist. Would you like to create one now?"):
            create_new_group(app, callback=add_items_to_new_group)
        return
    
    # If groups exist, show the dialog to select one
    dialog = tk.Toplevel(app.root)
    dialog.title("Add to Group")
    dialog.geometry("300x200")
    dialog.transient(app.root)
    dialog.grab_set()
    dialog.configure(bg="#1e1e2e")
    
    main_frame = ttk.Frame(dialog, padding=15)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(main_frame, text="Select group:").pack(pady=(0, 10))
    
    group_var = tk.StringVar()
    group_list = ttk.Combobox(main_frame, textvariable=group_var, width=20)
    group_list['values'] = groups
    if groups:
        group_list.current(0)
    group_list.pack(pady=10)
    
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(fill=tk.X, pady=(15, 0))
    
    def save_to_group():
        group_name = group_var.get()
        print(f"Selected group: {group_name}")
        
        if not group_name:
            messagebox.showerror("Error", "Please select a group")
            return
        
        # Update the group for each selected location
        count = 0
        for i in range(len(app.saved_locations)):
            if app.saved_locations[i]["name"] in selected_names:
                print(f"Adding {app.saved_locations[i]['name']} to group {group_name}")
                app.saved_locations[i]["group"] = group_name
                count += 1
        
        print(f"Added {count} items to group {group_name}")
        
        # Group is no longer empty if items were added
        if count > 0 and hasattr(app, 'empty_groups') and group_name in app.empty_groups:
            app.empty_groups.remove(group_name)
        
        # Save and update
        from core.settings import save_locations
        save_locations(app.saved_locations, app.config_file)
        
        # Update the UI
        app.update_location_list()
        
        # Show success message
        dialog.destroy()
        messagebox.showinfo("Success", f"Added {count} item(s) to group '{group_name}'")
    
    ttk.Button(btn_frame, text="Add to Group", command=save_to_group, 
              style="Success.TButton").pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    # Center the dialog
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x_pos = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y_pos = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
    
    # Keep dialog on top
    dialog.attributes("-topmost", True)

def remove_from_group(app):
    """Remove selected locations from their group"""
    selected = app.location_tree.selection()
    if not selected:
        messagebox.showinfo("Info", "Please select locations to remove from group")
        return
    
    # Get the selected items
    selected_names = []
    for item in selected:
        values = app.location_tree.item(item, "values")
        if values:
            selected_names.append(values[0])
    
    # Check if any selected items are in a group
    in_group_items = {}  # Track items by group
    for loc in app.saved_locations:
        if loc["name"] in selected_names and "group" in loc and loc["group"]:
            group = loc["group"]
            if group not in in_group_items:
                in_group_items[group] = []
            in_group_items[group].append(loc["name"])
    
    if not in_group_items:
        messagebox.showinfo("Info", "None of the selected items are in a group")
        return
    
    # Track which groups might become empty
    groups_to_check = set(in_group_items.keys())
    
    # Update to remove group
    count = 0
    for i, loc in enumerate(app.saved_locations):
        if loc["name"] in selected_names and "group" in loc and loc["group"]:
            # Make a copy of the location
            updated_loc = loc.copy()
            # Remove the group key
            del updated_loc["group"]
            # Update the saved location
            app.saved_locations[i] = updated_loc
            count += 1
    
    # Check which groups are now empty
    for group in groups_to_check:
        # See if any locations still use this group
        if not any(loc.get("group") == group for loc in app.saved_locations):
            # This group is now empty, add to empty_groups
            if not hasattr(app, 'empty_groups'):
                app.empty_groups = set()
            app.empty_groups.add(group)
            print(f"Group '{group}' is now empty and will be preserved")
    
    # Save and update
    from core.settings import save_locations
    save_locations(app.saved_locations, app.config_file)
    app.update_location_list()
    
    messagebox.showinfo("Success", f"Removed {count} item(s) from their groups")

def filter_locations_by_group(app, event=None):
    """Filter the locations list by the selected group"""
    app.update_location_list()

def get_filtered_locations(app, locations=None, group_name=None):
    """Get a filtered list of locations based on group name
    
    This is the actual filtering function that returns filtered data.
    """
    # If no locations are provided, use all saved locations
    if locations is None:
        locations = app.saved_locations
    
    # If no group is specified, use the currently selected group
    if group_name is None:
        group_name = app.group_var.get()
    
    if group_name == "All Groups":
        return locations
    else:
        return [loc for loc in locations if loc.get("group", "") == group_name]