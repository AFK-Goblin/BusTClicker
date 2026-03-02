def init_groups(state):
    """Initialize the groups system within the state dictionary."""
    if "empty_groups" not in state:
        state["empty_groups"] = set()

def get_all_groups(state):
    """Returns a clean, sorted list of all active and empty groups."""
    groups = set()
    for loc in state.get("saved_locations", []):
        if loc.get("group"):
            groups.add(loc["group"])
    
    if "empty_groups" in state:
        groups.update(state["empty_groups"])
        
    return sorted(list(groups))

def create_new_group(state, group_name):
    """Data logic for creating a group. Returns True if successful."""
    if not group_name or group_name.strip() == "":
        return False
        
    current_groups = get_all_groups(state)
    if group_name in current_groups:
        return False # Group already exists
        
    state["empty_groups"].add(group_name)
    return True

def assign_to_group(state, location_names, group_name):
    """Assigns a list of location names to a specific group."""
    count = 0
    for loc in state.get("saved_locations", []):
        if loc["name"] in location_names:
            loc["group"] = group_name
            count += 1
            
    # If the group now has items, it is no longer empty
    if count > 0 and group_name in state.get("empty_groups", set()):
        state["empty_groups"].remove(group_name)
        
    return count

def remove_from_group(state, location_names):
    """Strips the group assignment from the provided locations."""
    groups_to_check = set()
    
    # Remove groups
    for loc in state.get("saved_locations", []):
        if loc["name"] in location_names and loc.get("group"):
            groups_to_check.add(loc["group"])
            loc["group"] = "" # Clear the group
            
    # Check if we accidentally emptied a group, and preserve it
    for group in groups_to_check:
        if not any(loc.get("group") == group for loc in state.get("saved_locations", [])):
            state["empty_groups"].add(group)