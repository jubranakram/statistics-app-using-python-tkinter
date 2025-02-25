from tkinter import *
from tkinter import ttk
from pathlib import Path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import pandas as pd
import numpy as np

from app.utils.helpers import get_statistics_with_line_formatting, STAT_LABELS
from app.gui.widgets import BaseFrame, ListFrame, TextFrame, get_filename, save_figure

# Specify parameters
MAIN_PADDING = (3, 3, 3, 3)
PLOT_PADDING = (3, 3, 3, 3)
PARAM_PADDING = (3, 3, 3, 3)
VIS_PARAM_PADDING = (3, 3, 3, 3)

MAIN_FPARAMS = {
    'padding': MAIN_PADDING
}

PLOT_FPARAMS = {
    'padding': PLOT_PADDING,
    'borderwidth': 5,
    'relief': 'sunken',
    'width': 100, 
    'height': 100    
}

PARAM_FPARAMS = {
    'padding': PARAM_PADDING
}

VPARAM_FPARAMS = {
    'padding': VIS_PARAM_PADDING
}


BASE_ASSETS_PATH = Path('./assets')
ICONS_PATH = BASE_ASSETS_PATH / 'icons'
IMGS_PATH = BASE_ASSETS_PATH / 'images'
class MainWindow(Tk):
    def __init__(self, title, size, resizable, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(resizable[0], resizable[1])
        self.iconbitmap(ICONS_PATH / 'histogram.ico')      
        

    def menu(self):
        '''Creates file menu'''
        menu = Menu(self)
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="Quit", command=self.destroy) # Add Quit item to FileMenu
        menu.add_cascade(label="File", menu=file_menu)
        self.config(menu=menu) 
        
    def create_frame_structure(self):
        # main container
        self._main_frame = BaseFrame(self, **MAIN_FPARAMS)
        # other child containers
        self._plot_frame = self._main_frame.create_child_frame(**PLOT_FPARAMS)
        self._param_frame = self._main_frame.create_child_frame(**PARAM_FPARAMS)
        self._vis_param_frame = self._main_frame.create_child_frame(**VPARAM_FPARAMS)
        # other grandchild containers
        self._load_frame = self._main_frame.get_frame(self._param_frame)
        self._list_frame = self._main_frame.get_frame(self._param_frame)
        self._list_button_frame = self._main_frame.get_frame(self._param_frame)
        self._text_frame = self._main_frame.get_frame(self._param_frame)
        self._text_frame_ch = TextFrame(self._text_frame)
        self._frame_left = ListFrame(self._list_frame, STAT_LABELS.copy())
        self._frame_right = ListFrame(self._list_frame)
        
        # set grid structure
        self._main_frame.grid(column=0, row=0, sticky=(N, S, E, W))
        self._plot_frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        self._param_frame.grid(column=3, row=0, columnspan=2, rowspan=2, sticky=(N, S, E, W))
        self._vis_param_frame.grid(column=0, row=2, columnspan=3, rowspan=2, sticky=(N,S,E,W))
        self._load_frame.pack(side=TOP, fill=BOTH, expand=True)      
        self._list_frame.pack(side=TOP, fill=BOTH, anchor='n') 
        self._list_button_frame.pack(side=TOP, fill=BOTH, expand=True, anchor='n') 
        self._text_frame.pack(side=TOP, fill=BOTH, expand=True)
        self._text_frame_ch.pack(side=TOP, fill=BOTH, expand=True)
        
    def create_load_file_widget(self):
        namelbl = ttk.Label(self._load_frame, text="* Select an input data file in csv format only.")
        self._entry_var = StringVar()
        name = ttk.Entry(self._load_frame, state='disabled', textvariable=self._entry_var)
        load_button = ttk.Button(self._load_frame, text="Load", command=self.load_csv)
        
        # placement
        namelbl.pack(side=TOP, anchor='nw', padx=10)
        name.pack(side=TOP, fill=X, pady=5, padx=10)
        load_button.pack(side=TOP, anchor='e', padx=10)
        
    def load_csv(self):        
        filename = get_filename()
        if filename:
            self._entry_var.set(filename) 
            self._data = pd.read_csv(filename)
            self.cb_1['values'] = list(self._data.columns)
            self.cb_2['values'] = list(self._data.columns)
            # columns with numbers only - discarding categorical and boolean columns
            self._data_numbers = self._data.select_dtypes(include=['number'])
            
    def create_list_box_widget(self):
        # buttons to select and unselect statistics
        self._btn_to_right = ttk.Button(self._list_frame, text=">", command=self.move_to_right)
        self._btn_to_left = ttk.Button(self._list_frame, text="<", command=self.move_to_left)
        # placement
        self._frame_left.pack(side=LEFT, padx=10)
        self._frame_right.pack(side=RIGHT, padx=10)
        self._btn_to_right.pack(expand=True, ipadx=5)
        self._btn_to_left.pack(expand=True, ipadx=5)  
        
    def move_to_right(self):
        # select statistics
        self.move(self._frame_left, self._frame_right)

    def move_to_left(self):
        # unselect statistics
        self.move(self._frame_right, self._frame_left)

    def move(self, from_frame, to_frame):
        # select -> unselect -> select
        value = from_frame.pop_selection()
        if value:
            for val in value:
                to_frame.insert_item(val)
                
    def create_compute_button_widget(self):
        compute_button = ttk.Button(self._list_button_frame, text="Compute", command=self.compute_statistics)
        # placement
        compute_button.pack(side=RIGHT, padx=10, anchor='e', pady=5)
        
    def compute_statistics(self):
        # compute statistics and prepare formatted text for display as a table
        self._text_frame_ch._text.configure(state='normal')
        self._text_frame_ch._text.delete('1.0', END)
        # create header line
        columns = list(self._data_numbers.columns)
        header_line = f"{'':<20}"
        for col in columns:
            header_line += f"{col:<20}"
        
        self._text_frame_ch.insert_text('1.0', header_line+'\n')
        self._text_frame_ch.insert_text('2.0', '-'*len(header_line)+'\n')
        
        n = 3
        for val in self._frame_right.get_items():
            self._text_frame_ch.insert_text(f"{n}.0", get_statistics_with_line_formatting(self._data_numbers, val)+'\n')
            n += 1
        self._text_frame_ch._text.configure(state='disabled')
            
    def create_column_selectors(self):
        label_col1 = ttk.Label(self._vis_param_frame, text="Col-1:")
        label_col1.pack(side=LEFT, padx=5, anchor='w')

        self.col_1_selection = StringVar()
        self.cb_1 = ttk.Combobox(self._vis_param_frame, textvariable=self.col_1_selection, 
           values=())
        self.cb_1.pack(side=LEFT, padx=5, anchor='w')

        label_col2 = ttk.Label(self._vis_param_frame, text="Col-2:")
        label_col2.pack(side=LEFT, padx=5, anchor='w')

        self.col_2_selection = StringVar()
        self.cb_2 = ttk.Combobox(self._vis_param_frame, textvariable=self.col_2_selection, 
           values=())
        self.cb_2.pack(side=LEFT, padx=5, anchor='w')
        
    def create_plot_buttons(self):
        bx, b_y = 20, 20
        
        self.himg = PhotoImage(file=IMGS_PATH / 'histogram.png', width=bx, height=b_y)
        self.bimg = PhotoImage(file=IMGS_PATH / 'box_whisker.png', width=bx, height=b_y)
        self.scimg = PhotoImage(file=IMGS_PATH / 'scatter.png', width=bx, height=b_y)
        self.simg = PhotoImage(file=IMGS_PATH / 'save.png', width=bx, height=b_y)

        btn_hist = ttk.Button(self._vis_param_frame, image=self.himg, width=bx, command=self.plot_histogram)
        btn_boxw = ttk.Button(self._vis_param_frame, image=self.bimg, width=bx, command=self.plot_boxw)
        btn_scatt = ttk.Button(self._vis_param_frame, image=self.scimg, width=bx, command=self.plot_scatter)
        btn_save = ttk.Button(self._vis_param_frame, image=self.simg, width=bx, command=self.save_fig)
        # placement
        btn_hist.pack(side=LEFT, padx=2, anchor='center')
        btn_boxw.pack(side=LEFT, anchor='center')
        btn_scatt.pack(side=LEFT, padx=2, anchor='w')
        btn_save.pack(side=LEFT, anchor='w')
        
    def base_plot(self):
        if self.canvas == None:
            self.canvas = FigureCanvasTkAgg(self.fig, self._plot_frame)
            self.canvas.get_tk_widget().pack(fill=BOTH, side=TOP, expand=True)    
            self.axs = self.fig.add_subplot(111)
        self.axs.clear()
        self._column_name = self.col_1_selection.get()        
        self.axs.set_xlabel(self._column_name.title())
        self.axs.set_ylabel("Frequency")        
        
        
    def plot_histogram(self):
        self.base_plot()
        self.axs.hist(self._data[self._column_name], bins='auto', color='blue', edgecolor='k', alpha=0.5)
        self.canvas.draw_idle()
    
    def plot_boxw(self):
        self.base_plot()
        self.axs.boxplot(self._data[self._column_name], patch_artist=True, boxprops=dict(facecolor='blue', color='k',alpha=0.5))
        self.canvas.draw_idle()
    
    def plot_scatter(self):
        self.base_plot()
        column_name_2 = self.col_2_selection.get()        
        if len(self._column_name) and len(column_name_2):
            self.axs.scatter(self._data[self._column_name], self._data[column_name_2], s=12, c='blue', marker='o', edgecolors='k', alpha=0.5)
            x_label = self._column_name
            y_label = column_name_2
        elif len(self._column_name):           
            self.axs.scatter(self._data[self._column_name], self._data[self._column_name], s=12, c='blue', marker='o', edgecolors='k', alpha=0.5)
            x_label = self._column_name
            y_label = self._column_name
        
        self.axs.set_xlabel(x_label) 
        self.axs.set_ylabel(y_label)
        self.axs.grid()
        self.canvas.draw_idle()
    
    def save_fig(self):
        save_figure(self.fig)
        
            
           
    def setup(self):
        # add menu
        self.menu()
        # create app structure
        self.create_frame_structure()
        # add load file widget
        self.create_load_file_widget()
        # add listboxes
        self.create_list_box_widget()
        # add compute statistics widget
        self.create_compute_button_widget()
        # add column selectors
        self.create_column_selectors()
        # add plot buttons
        self.create_plot_buttons()
        
        # final formatting to layout
        self.canvas = None

        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self._main_frame.columnconfigure(0, weight=3)
        self._main_frame.columnconfigure(1, weight=3)
        self._main_frame.columnconfigure(2, weight=3)
        self._main_frame.columnconfigure(3, weight=1)        
        self._main_frame.rowconfigure(1, weight=1)   

        self.fig = Figure()
        
        
        

    
        
        
        