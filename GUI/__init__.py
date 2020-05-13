_root_dir = None

def start():
    import os

    import tkinter as tk
    import tkinter.filedialog as fd

    from GUI.Importer import ImportFrame

    global _root_dir
    _root_dir = os.getcwd()

    window = tk.Tk()
    window.title('Ballistics Project')
    window.geometry("300x200+10+10")

    x = ImportFrame(window)

    window.mainloop()
