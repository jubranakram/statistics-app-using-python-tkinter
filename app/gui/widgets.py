from tkinter import *
from tkinter import ttk, filedialog

class BaseFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(BaseFrame, self).__init__(parent, *args, **kwargs)
        
    def create_child_frame(self, *args, **kwargs):
        return ttk.Frame(self, *args, **kwargs)
    
    def get_frame(self, container, *args, **kwargs):
        return ttk.Frame(container, *args, **kwargs)
    
    
def save_figure(figure):
    # Open a file dialog to specify the save location and filename
    file_path = filedialog.asksaveasfilename(defaultextension=".png", 
                                             filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                             title="Save the plot as...")
    if file_path:
        # Save the figure to the specified file
        figure.savefig(file_path)
        
    
def get_filename():
    file_types = (("csv files (*.csv)", "*.csv"), ("All files", "*"))
    filename = filedialog.askopenfilename(title="Open file", initialdir="/", filetypes=file_types)
    return filename
            
        


class ListFrame(ttk.Frame):
    def __init__(self, parent, items=[]):
        super(ListFrame, self).__init__(parent)
        self._items = items
        self.listvar = Variable(value=())
        self._listbox = Listbox(self, selectmode = "multiple", listvariable=self.listvar)
        self._scroll = Scrollbar(self, orient=VERTICAL, command=self._listbox.yview)
        self._listbox.config(yscrollcommand=self._scroll.set)
        self._listbox.insert(0, *self._items)
        self._listbox.pack(side=LEFT)
        self._scroll.pack(side=LEFT, fill=Y)

    def pop_selection(self):
        index = self._listbox.curselection()
        
        values = []
        if index:
            for idx in index:
                value = self._listbox.get(idx)
                values.append(value)
            for idx in sorted(index, reverse=True):
                self._listbox.delete(idx)
                
        return values
        
    def insert_item(self, item):
        self._listbox.insert(END, item)

    def get_items(self):
        return self.listvar.get()

class TextFrame(ttk.Frame):
    def __init__(self, parent):
        super(TextFrame, self).__init__(parent)
        
        self._text = Text(self, width=40, state='disabled', wrap="none")
        
        self._tscroll = Scrollbar(parent, orient=VERTICAL, command=self._text.yview)
        self._txscroll = Scrollbar(parent, orient=HORIZONTAL, command=self._text.xview)
        self._text.config(yscrollcommand=self._tscroll.set, xscrollcommand=self._txscroll.set)
        
        self._text.pack(side=TOP, fill=BOTH, expand=True)
        self._tscroll.pack(side=RIGHT, fill=Y)
        self._txscroll.pack(side=BOTTOM, fill=X)

    def insert_text(self, line, text):        
        self._text.insert(line, text)
        

    