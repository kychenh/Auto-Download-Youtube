from youtubedownloader import YouTubeDownloader
import tkinter as tk
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # self.grid()
        # self.create_widgets()
        self.downloader = YouTubeDownloader(master)

  
root = tk.Tk()
app = Application(master=root)
app.mainloop()
