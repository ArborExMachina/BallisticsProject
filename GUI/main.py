import tkinter as tk
import tkinter.filedialog as fd

from Dialog import Dialog

path = {
    'ini':"",
    'input':""
}

def set_path(thing):
    path[thing] = fd.askopenfile('r').name

def main():
    window = tk.Tk()
    window.title('Ballistics Project')
    window.geometry("300x200+10+10")


    config_btn=tk.Button(window, text="Config", command=lambda: set_path('ini'))
    config_btn.grid(row=1,column=1)
    input_btn=tk.Button(window, text="Input", command=lambda: set_path('input'))
    input_btn.grid(row=1,column=2)
    run=tk.Button(window, text="Run", command=lambda: )
    window.mainloop()

if __name__ == '__main__':
    main()