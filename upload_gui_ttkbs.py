import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from uploader_tab import UploaderTab
from file_manager_tab import DriveFileManager
from uploader import Authentication

class DriveUploaderGUI(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")

        self.configure(background="#F5F5F5")

        auth = Authentication()
        file = auth.get_resource_path(relative_path="drive_uploader.png")
        icon = ttk.PhotoImage(file=file)
        self.iconphoto(False, icon)

        self.title("Google Drive Manager")
        self.geometry("800x500")

        self.create_tabs()

    def create_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.uploader_tab = ttk.Frame(notebook)
        notebook.add(self.uploader_tab, text="Uploader")

        UploaderTab(self.uploader_tab)

        self.file_manager_tab = ttk.Frame(notebook)
        notebook.add(self.file_manager_tab, text="File Manager")

        DriveFileManager(self.file_manager_tab)
