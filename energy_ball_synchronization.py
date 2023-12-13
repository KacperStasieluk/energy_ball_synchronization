import tkinter as tk
from tkinter import messagebox
import random
from random import randint
import math


class EnergyBallWindow:
    def __init__(self, root, windows, id):
        self.root = root
        self.id = id
        self.windows = windows
        self.ball_size = 50
        self.window_size = 200
        self.create_window(self.window_size)
        self.draw_energy_ball()

    def create_window(self, size):
        self.window = tk.Toplevel(self.root)
        self.window.geometry('200x200+{}+{}'.format(randint(100, 500), randint(100, 500)))
        self.window.overrideredirect(True)
        self.canvas = tk.Canvas(self.window, bg='black', width=size, height=size)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Button-1>', self.start_move)
        self.canvas.bind('<ButtonRelease-1>', self.stop_move)
        self.canvas.bind('<B1-Motion>', self.on_move)

    def start_move(self, event):
        self.window._drag_start_x = event.x
        self.window._drag_start_y = event.y

    def stop_move(self, event):
        self.window._drag_start_x = None
        self.window._drag_start_y = None

    def on_move(self, event):
        dx = event.x - self.window._drag_start_x
        dy = event.y - self.window._drag_start_y
        x = self.window.winfo_x() + dx
        y = self.window.winfo_y() + dy
        self.window.geometry(f'+{x}+{y}')

    def get_window_center(self):
        return self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2

    def draw_energy_ball(self):
        self.colors = ['red', 'green', 'blue', 'pink', 'purple']
        color = self.colors[self.id % len(self.colors)]
        x, y = self.window_size // 2, self.window_size // 2
        self.ball = self.canvas.create_oval(x - self.ball_size, y - self.ball_size, x + self.ball_size, y + self.ball_size, fill=color)

    def update_connection(self):
        self.canvas.delete('connection')
        self.canvas.delete('another_ball')
        center_x1, center_y1 = self.get_window_center()
        wx, wy = self.window.winfo_x(), self.window.winfo_y()

        for id, window in enumerate(self.windows):
            if window != self:
                obx, oby = window.get_window_center()
                ox, oy = window.window.winfo_x(), window.window.winfo_y()
                center_x2, center_y2 = obx + ox - wx, oby + oy - wy

                self.canvas.create_oval(center_x2 - self.ball_size, center_y2 - self.ball_size, center_x2 + self.ball_size, center_y2 + self.ball_size, fill=self.colors[id], tags="another_ball")
                self.canvas.create_line(center_x1, center_y1, center_x2, center_y2, fill='yellow', tags="connection", width=3)

class ControlPanel:
    def __init__(self, root, windows):
        self.root = root
        self.windows = windows
        self.panel = tk.Toplevel(root)
        self.panel.title('Energy Ball Synchronization')
        self.panel.geometry('300x100')
        self.create_widgets()

    def create_widgets(self):
        button_frame = tk.Frame(self.panel)
        button_frame.pack(expand=True)
        create_button = tk.Button(button_frame, text='Create new ball', command=self.create_new_window)
        delete_button = tk.Button(button_frame, text='Delete last ball', command=self.delete_last_window)
        create_button.grid(row=0, column=0, padx=10, pady=10)
        delete_button.grid(row=0, column=1, padx=10, pady=10)
        self.panel.protocol('WM_DELETE_WINDOW', self.close_all_windows)
        self.panel.geometry('350x50')
        self.panel.resizable(False, False)

    def create_new_window(self):
        if(len(self.windows) < 5):
            new_id = len(self.windows)
            new_window = EnergyBallWindow(self.root, self.windows, new_id)
            self.windows.append(new_window)
        else:
            messagebox.showinfo('Info', f'You cannot create more than {len(self.windows)} energy balls.')

    def delete_last_window(self):
        if self.windows:
            last_window = self.windows.pop()
            last_window.window.destroy()
        else:
            messagebox.showinfo('Info', 'Nothing to delete.\nTry to create some energy balls first. :)')

    def close_all_windows(self):
        for window in self.windows:
            window.window.destroy()
        self.root.quit()


def main():
    root = tk.Tk()
    root.withdraw()

    windows = []
    control_panel = ControlPanel(root, windows)
    for i in range(2):
        window = EnergyBallWindow(root, windows, i)
        windows.append(window)

    def update_connections():
        for window in windows:
            window.update_connection()
        root.after(100, update_connections)

    update_connections()
    root.mainloop()

main()
