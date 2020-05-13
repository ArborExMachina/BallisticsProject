import os
import glob
import tkinter as tk
import configparser

import GUI

params = {
    'sh' : 'sight height',
    'sa' : 'shooting angle',
    'ws' : 'wind speed',
    'wa' : 'wind angle'
}
range_words = ['start', 'end', 'step']

class Editor:
    def __init__(self, root, profile_name, close_handler):
        self.config = configparser.ConfigParser()
        self.close_handler = close_handler

        if profile_name != "New:":
            self.config.read(f"Configs/{profile_name}.ini")

        popup = tk.Toplevel(root)
        frame = tk.Frame(popup)
        self.popup = popup
        self.input_fields = {}

        tk.Label(frame, text="Profile Name").grid(row=1,column=1)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=1,column=2)
        self.name_entry.insert(0, profile_name)

        # flat params
        for row,param in enumerate(params, start=3):
            e_var = tk.StringVar()
            e_var.set(self.config.get('params', param, fallback="New Value"))
            self.input_fields[param] = e_var
            
            tk.Label(frame, text=params[param]).grid(row=row, column=1)
            tk.Entry(frame, textvariable=e_var).grid(row=row, column=2)
            
        
        # zero test range
        # tk.Label(frame, text="Zero params").grid(row=8, column=2)
        # tk.Label(frame, text="Zero").grid(row=8, column=1)
        zero_params = {}
        for col,word in enumerate(range_words, start=1):
            e_var = tk.StringVar()
            e_var.set(self.config.get('zero',word,fallback="New Value"))
            zero_params[word] = e_var
            
            tk.Label(frame, text="zero " + word).grid(row=8, column=col)
            tk.Entry(frame, textvariable=e_var).grid(row=9, column=col)
            
        self.input_fields['zero'] = zero_params

        # range cutoff (ie, bullet travel distance we care about)
        range_params = {}
        for col,word in enumerate(range_words, start=1):
            e_var = tk.StringVar()
            e_var.set(self.config.get('range',word,fallback="New Value"))
            range_params[word] = e_var
            
            tk.Label(frame, text="range " + word).grid(row=10, column=col)
            tk.Entry(frame, textvariable=e_var).grid(row=11, column=col)

        self.input_fields['range'] = range_params
        
        frame.pack()

        tk.Button(popup, text="Save", command=self.shutdown).pack()
        
        # popup.protocol("WM_DELETE_WINDOW", lambda: self.shutdown(close_handler))
        popup.mainloop()
    
    def shutdown(self):
        profile_name = self.name_entry.get()
        self.write(profile_name)
        self.close_handler(profile_name)
        self.popup.destroy()

    def write(self, profile_name):     
        self.config['params'] = {param:self.input_fields[param].get() for param in params}
        self.config['zero'] = {word:self.input_fields['zero'][word].get() for word in range_words}
        self.config['range'] = {word:self.input_fields['range'][word].get() for word in range_words}

        with open(f"Configs/{profile_name}.ini",'w') as ofile:
            self.config.write(ofile)
