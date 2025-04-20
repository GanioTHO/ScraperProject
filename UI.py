import tkinter as tk
from tkinter import *
BG_COLOR = "#EDCB96"


class UI():

    def __init__(self):
        self.window = Tk()
        self.window.title("Scraper")
        self.window.config(bg=BG_COLOR)
        self.window.geometry("300x300")

        for i, weight in [(0, 1), (1, 1)]:
            self.window.columnconfigure(i, weight=weight)

        for i, weight in [(0, 1), (1, 6)]:
            self.window.rowconfigure(i, weight=weight)

        self.scrap = Button(text="Scrap", highlightthickness=0)
        self.scrap.grid(row=0, column=0, pady=(150, 0), padx=(100, 0))

        self.save = Button(text="Save", highlightthickness=0)
        self.save.grid(row=0, column=2, pady=(150, 0), padx=(0, 100))

        self.label_scraping = Label(text="Scraping...", bg=BG_COLOR)
        self.label_scraping.grid(row=1, column=0, columnspan=3, pady=(0, 30))


        self.label_url = Label(text="Enter URL:", bg=BG_COLOR)
        self.label_url.grid(row=0, column=0, columnspan=3, pady=(0, 0))
        self.url_box = Entry(width=30)
        self.url_box.grid(row=0, column=0, columnspan=3, pady=(40, 0))




        self.window.mainloop()

UI()