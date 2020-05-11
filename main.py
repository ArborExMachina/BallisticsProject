from tkinter import *

def main():
    window = Tk()
    window.title('Ballistics Project')
    window.geometry("300x200+10+10")


    btn=Button(window, text="Parse")
    btn.place(x=80, y=100)
    
    window.mainloop()

if __name__ == '__main__':
    main()