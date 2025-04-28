import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os, threading
from uploader import UploadToDrive
from file_manager import DriveFileManager

class UploadTab(tk.Frame):
    def __init__(self, parent, drive_client):
        super().__init__(parent, bg="#f0f0f0")
        self.drive_client = drive_client
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="📁 Google Drive Uploader", font=("Segoe UI", 16, "bold"), bg="#f7f7f7", fg="#333")
        title.pack(pady=15)

        # File selection
        file_frame = tk.Frame(self, bg="#f7f7f7")
        file_frame.pack(pady=5)

        self.file_label = tk.Label(file_frame, text="No file selected", font=("Segoe UI", 10), bg="#f7f7f7", fg="#777", width=40, anchor="w")
        self.file_label.pack(side="left", padx=(10, 5))

        browse_button = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_button.pack(side="right", padx=10)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        # self.progress_bar.pack(pady=10)

        self.progress_label = ttk.Label(self, text="0%")
        # self.progress_label.pack()

        # Submit button
        submit_btn = ttk.Button(self, text="Upload File", command=self.run_action)
        submit_btn.pack(pady=20, ipadx=10, ipady=4)

        # Result message
        self.result_label = tk.Label(self, text="", font=("Segoe UI", 10), bg="#f7f7f7", fg="#006400")
        self.result_label.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=filename, fg="#333")

    def update_progress(self, progress):
        # print(progress * 100)
        self.progress_label.config(text=f"{progress * 100:.2f}%")
        self.progress_bar["value"] = progress * 100

    def run_action(self):
        # Show the progress bar and label
        self.progress_bar.pack(pady=10)
        self.progress_label.pack()

        uploader = UploadToDrive()  # Create an instance of the Uploader class

        from tkinter import filedialog, messagebox

        # Reset progress bar at the beginning
        self.progress_bar["value"] = 0
        self.progress_label.config(text="0%")

        def run_upload():
            try:
                result = uploader.upload_or_replace_file(
                    self.selected_file,
                    progress_callback=self.update_progress
                )
                self.after(0, lambda: messagebox.showinfo("Success", result))
            except Exception as e:
                err = str(e)
                self.after(0, lambda: messagebox.showerror("Error", err))

        # Run upload in background
        threading.Thread(target=run_upload, daemon=True).start()
        # self.result_label.config(text=result, fg="#006400" if "Uploaded" in result or "Updated" in result else "#b00020")

class DriveUploaderGUI(tk.Tk):
    def __init__(self, drive_client):
        super().__init__()
        self.title("Google Drive Uploader")
        # self.geometry("500x300")
        self.geometry("700x500")
        self.configure(bg="#f7f7f7")
        self.drive_client = drive_client
        self.create_tabs()
        self.resizable(False, False)

        self.selected_file = ""

    def create_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        upload_tab = UploadTab(notebook, self.drive_client)
        manager_tab = DriveFileManager(notebook, self.drive_client)

        notebook.add(upload_tab, text="Upload")
        notebook.add(manager_tab, text="Manage Files")
