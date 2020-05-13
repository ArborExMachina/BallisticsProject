import os
import glob
import tkinter as tk

import GUI
import GUI.Profiles

class ImportFrame:
    def __init__(self, root):
        frame = tk.Frame(root)
        self.frame = frame
        self.root = root

        config_dir = os.path.realpath(GUI._root_dir + "/Configs")
        options = [x.split('/')[-1].split('.')[0] for x in glob.glob(config_dir+"/*.ini")]
        options.append("New:")
        self.selected = tk.StringVar(frame)
        self.selected.set(options[0])

        profile_label = tk.Label(frame, text="Profile")
        self.profiler_drop = tk.OptionMenu(frame, self.selected, *options, command=self.drop_changed)
        
        profile_label.grid(row=1,column=1)
        self.profiler_drop.grid(row=2,column=1)
        tk.Button(frame, text="Edit Selected", command=self.edit).grid()
        frame.pack()
    
    def update_list(self, new_option):
        menu = self.profiler_drop['menu']
        menu.delete("New:")
        menu.add_command(label=new_option, command=tk._setit(self.selected, new_option, self.drop_changed))
        menu.add_command(label="New:", command=tk._setit(self.selected, "New:", self.drop_changed))
    
    def drop_changed(self, val):
        if val == "New:":
            GUI.Profiles.Editor(self.root, val, self.profile_editor_closed)
    
    def edit(self):
        GUI.Profiles.Editor(self.root, self.selected.get(), self.profile_editor_closed)
    
    def profile_editor_closed(self, selected_profile):
        self.update_list(selected_profile)
        self.selected.set(selected_profile)
        self.drop_changed(selected_profile)
    
        