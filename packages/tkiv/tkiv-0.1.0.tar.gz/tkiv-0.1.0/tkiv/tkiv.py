import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PIL import Image, ImageTk


INITIAL_DIRECTORY = Path.home()
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.ico', '.bmp', '.tiff']

class MainWindow(ttk.Frame):
    def __init__(self, root, title, *args, **kwargs):
        ttk.Frame.__init__(self, root, *args, **kwargs)

        self.root = root
        root.minsize(width=600, height=350)
        root.title(title)
        self.pack(fill=tk.BOTH, expand=tk.YES, padx=10, pady=10)

        self.style = ttk.Style()

        pw= ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        pw.pack(expand=tk.YES, fill=tk.BOTH)

        #DRAWING PANES
        self.left_pane = LeftPane(pw, self)
        self.right_pane = RightPane(pw, self)

        pw.add(self.left_pane)
        pw.add(self.right_pane)

        self.right_pane.bind('<Configure>', lambda event: self.load_image())

    def load_image(self, path=None):
        self.right_pane.load_image(path)


class LeftPane(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        self.controller = controller

        self.path_var = tk.StringVar()
        self.path_var.set(INITIAL_DIRECTORY)

        self.label_path = self.draw_label_path()
        self.label_path.grid(row=0, column=0, sticky='news')
        self.grid_columnconfigure(0, weight=1)

        self.browse_button = self.draw_browse_button()
        self.browse_button.grid(row=0, column=1)

        self.images_treeview_frame = self.draw_images_treeview()
        self.images_treeview_frame.grid(columnspan=2, row=1, column=0, sticky='news')
        self.grid_rowconfigure(1, weight=1)

        self.images_treeview = self.images_treeview_frame.children['files']
        self.populate_images_treeview()

    def draw_label_path(self):
        label = ttk.Label(self, textvar=self.path_var, padding=(3, 0, 0, 0), relief=tk.GROOVE, anchor=tk.W)
        label.bind('<Button-1>', self.select_directory)
        return label

    def draw_browse_button(self):
        button = ttk.Button(self, text='...', width=5, command=self.select_directory)
        return button

    def draw_images_treeview(self):
        #Adding a parent frame to help placing the scrollbar
        treeview_frame = tk.Frame(self)

        treeview = ttk.Treeview(treeview_frame, name='files')
        treeview.pack(fill=tk.BOTH, expand=tk.Y, side=tk.LEFT)
        treeview.heading('#0', text='File Name')
        treeview.column('#0', stretch=tk.YES)
        treeview.bind('<<TreeviewSelect>>', self.on_image_selected)

        scroll = ttk.Scrollbar(treeview_frame, orient=tk.VERTICAL, command=treeview.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        treeview['yscrollcommand'] = scroll.set

        return treeview_frame

    def on_image_selected(self, event):
        currentItem = self.images_treeview.focus()
        fullpath = os.path.join(self.path_var.get(), self.images_treeview.item(currentItem)['text'])
        self.controller.load_image(fullpath)

    def populate_images_treeview(self):
        files = self.get_images_list(self.path_var.get())
        self.images_treeview.delete(*self.images_treeview.get_children())
        for file in files:
            self.images_treeview.insert('', 0, text=file)

    def get_images_list(self, path):
        images = []
        for file in os.listdir(path):
            ext = os.path.splitext(file)[1]
            if ext.lower() in SUPPORTED_FORMATS:
                images.append(file)
        return images

    def select_directory(self, event=None):
        path = filedialog.askdirectory(parent=self.controller.root, initialdir=r'C:\Users\danilo', title='Please select a directory')
        if path:
            self.path_var.set(path)
            self.populate_images_treeview()

class RightPane(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)

        self.controller = controller
        #prevent big images from resizing right pane
        self.grid_propagate(False)

        ttk.Style().configure('RightPane.TFrame', background='black')
        self.configure(style='RightPane.TFrame')

        self.original_image = None #image opened from disk
        self.previous_image = None #resized image on frame

        self.image_label = ttk.Label(self, text="No image selected...")
        self.image_label.grid(row=0, column=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def clamp_dimensions(self, original_dimensions, clamp_dimensions):
        image_width, image_height = original_dimensions
        width, height = clamp_dimensions

        #if image is smaller than frame, don't resize
        if image_width <= width and image_height <= height:
            return original_dimensions

        #round to get a few pixels of slack when resizing
        image_ratio = round(image_width / image_height, 2)
        frame_ratio = round(width / height, 2)

        #if image width is proportionally larger than frame width, set image width to frame width and scale height
        if image_ratio > frame_ratio:
            new_width = width
            new_height = int((width / image_width) * image_height)
        #if image height is proportionally larger than frame height, set image height to frame height and scale width
        elif image_ratio < frame_ratio:
            new_width = int((height / image_height) * image_width)
            new_height = height
        #image size is a multiple of frame saze (rounded to 2 decimal places), so just stick it to the frame sides
        else:
            new_width = width
            new_height = height

        return new_width, new_height



    def load_image(self, path=None):

        if path == None and self.original_image == None:
            return
        elif path != None:
            self.original_image = Image.open(path)

        new_width, new_height = self.clamp_dimensions(original_dimensions=self.original_image.size,
                                                      clamp_dimensions=(self.winfo_width(), self.winfo_height()))

        previous_width, previous_height = self.previous_image.size if self.previous_image else (0, 0)
        # path is != None when treeview selection change, otherwise, we know it's still the same image therefore
        # if dimensions are different, resize the image, otherwise, use the previous one
        if path != None or new_width != previous_width or new_height != previous_height:
            self.previous_image = self.original_image.resize((new_width, new_height), Image.ANTIALIAS)

        self.photoimage = ImageTk.PhotoImage(self.previous_image)
        self.image_label.configure(image=self.photoimage)

def main(args=None):
    root = tk.Tk()
    MainWindow(root, "Tkiv")
    root.mainloop()

if __name__ == '__main__':
    main()