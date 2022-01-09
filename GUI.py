import json
import webbrowser
import news_search as ns
from tkinter import *

class newsfeed:
    def __init__(self,gui):
        # set a title
        self.gui = gui
        self.gui.title("Newsfeed")
        self.gui.geometry("800x500")
        self.gui.configure(bg="grey20")
        
        # make window sticky for NS(North and South)
        self.gui.grid_columnconfigure(0, weight=1)
        self.gui.rowconfigure(2, weight=2)
        
        #--------Search Frame section----------------------------------------------------------------------
        # create frame, search frame
        self.searchFrame = LabelFrame(gui,bg="grey20")
        self.sf = self.searchFrame
        self.sf.grid(row=0, sticky="ew")
        
        # make search frame sticky for every case
        self.sf.grid_rowconfigure(0, weight=1)
        self.sf.grid_columnconfigure(0, weight=1)
    
        # create search bar entry
        self.entry = Entry(self.sf,bg="gray20", fg="grey", borderwidth=0)
        self.entry.bind("<Return>", self.search)
        self.entry.grid(row=0,sticky="ew")
        
        # create search button
        search_button = Button(self.sf, text="Search", 
                               command=self.search, 
                               bg="grey20", 
                               fg="white", 
                               cursor="hand2",
                               relief="flat")
        search_button.grid(row=0,column=1)
        
        #---------News Frame section-----------------------------------------------------------------------
        # create frame, news frame
        self.newsFrame = LabelFrame(gui,bg="grey")
        self.nf = self.newsFrame
        self.nf.grid(row=1,column=0,sticky="nsew")
        
        self.nf.grid_rowconfigure(0, weight=1)
        self.nf.grid_columnconfigure(0, weight=1)
        
        # create news label
        Label(self.nf, text="News", 
              bg="grey", 
              fg="white", 
              relief="raised",
              borderwidth=0).grid(row=0,sticky="ew")
        self.s_label = Label(self.nf, text="Symbol",bg="grey", fg="white")
        self.s_label.grid(row=0,column=1,sticky="ew")
        
    # stores stock ticker searched, calls update
    def search(self, event=None):
        ticker = self.entry.get()
        print("searching...",)
        ns.search(ticker)
        print("search complete...")
        self.s_label.config(text=ticker.upper())
        self.update()
    
    # update the new search
    def update(self):
        # opens json file
        with open('newsfeedData.json') as json_data:
            jsonData = json.load(json_data)
        
        # create news frame 2
        self.main_nframe = LabelFrame(self.gui, bg="grey20")
        self.mnf = self.main_nframe
        self.mnf.grid(row=2, column=0, sticky="nsew")
        
        self.mnf.grid_rowconfigure(0, weight=1)
        self.mnf.grid_columnconfigure(0, weight=1)
    
        # Create canvas
        self.my_canvas = Canvas(self.mnf, bg="grey")
        self.my_canvas.grid(row=0,column=0,sticky="nsew")  
        
        # Add a scrollbar to canvas
        my_scrollbar = Scrollbar(self.mnf, orient=VERTICAL, command=self.my_canvas.yview)
        my_scrollbar.grid(row=0,column=1,sticky="ns")
        
        # Config the canvas
        self.my_canvas.configure(yscrollcommand=my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))
        
        # create another frame inside the canvas
        self.second_frame = LabelFrame(self.my_canvas)
        self.frame = self.my_canvas.create_window((0,0), window=self.second_frame, anchor="nw")
        self.my_canvas.bind('<Configure>', self.resize_frame, add="+")
        
        self.second_frame.grid_rowconfigure(0, weight=1)
        self.second_frame.grid_columnconfigure(0, weight=1)
        
        # clears frame upon each search
        self.clear_frame()
        
        # creates news labels
        link = lambda x: (lambda u: self.openlink(x))
        cursor_e = lambda x: (lambda e: self.cursor_enter(x))
        cursor_l = lambda x: (lambda l: self.cursor_leave(x))
        
        for i in range(0,len(jsonData)):
            index = jsonData[i]
            title = index["title"]
            url = index["link"]
            title_label = Label(self.second_frame, text=title, 
                                fg="white", 
                                bg="grey20", 
                                cursor="hand2", 
                                relief="ridge",
                                borderwidth=1)
            title_label.grid(row=2+i, sticky="ew")
            
            title_label.bind("<Button-1>", link(url))
            title_label.bind("<Enter>", cursor_e(title_label))
            title_label.bind("<Leave>", cursor_l(title_label))
        
        
    # clears old search data/labels   
    def clear_frame(self):
        for label in self.second_frame.winfo_children():
            label.grid_forget()
            
    def openlink(self,url):
        webbrowser.open_new(url)
    
    def cursor_enter(self, label):
        label.config(bg="grey30")
        
    def cursor_leave(self, label):
        label.config(bg="grey20")
    
    def resize_frame(self, e):
        self.my_canvas.itemconfig(self.frame, width=e.width)

# driver
if __name__ == "__main__":
         
    # create a GUI window
    gui = Tk()
    obj = newsfeed(gui)    
    gui.mainloop()
