import tkinter as tk


class UserInterface:

    def __init__(self):
        self.window = tk.Tk()
        self.create_widgets(self.window)

    def create_widgets(self, window):
        self.greeting = tk.Label(text='Olá mundo!')
        self.greeting.pack()
        window.mainloop()


if __name__ == '__main__':
    test = UserInterface()
