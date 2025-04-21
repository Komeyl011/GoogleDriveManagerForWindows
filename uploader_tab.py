import os, threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
from uploader import UploadToDrive

class UploaderTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.style = ttk.Style()
        self.style.configure("FileUploaderFrame.TFrame", background="#F5F5F5")
        self.style.configure("DrivePrimary.TButton", background="#4285F4", foreground="white")

        parent.configure(style="FileUploaderFrame.TFrame")

        self.selected_file = None
        self.create_widgets(parent)
    
    def create_widgets(self, parent):
        frame_bg = self.style.lookup("FileUploaderFrame.TFrame", "background")
        title = ttk.Label(parent, text="📁 Google Drive Uploader", font=("Segoe UI", 16, "bold"), background=frame_bg, foreground="#202124")
        title.pack(pady=(90, 25))

        # File selection
        file_frame = ttk.Frame(parent)
        file_frame.config(style="FileUploaderFrame.TFrame")
        file_frame.pack(pady=5)

        self.file_label = ttk.Label(file_frame, text="No file selected", font=("Segoe UI", 10), background=frame_bg, width=40, anchor="w")
        self.file_label.pack(side="left", padx=(10, 5))

        self.browse_button = ttk.Button(file_frame, text="Browse", command=self.browse_file, bootstyle=(PRIMARY))
        self.browse_button.pack(side="right", padx=10)
        
        # Progress bar
        self.style.configure("Custom.Horizontal.TProgressbar",
                            troughcolor="#e0e0e0",
                            background="#4285F4",  # progress color
                            bordercolor="#808080",
                            thickness=20)
        self.progress_bar = ttk.Progressbar(parent, orient="horizontal", length=300, mode="determinate", style="Custom.Horizontal.TProgressbar")
        # self.progress_bar.pack(pady=10)

        self.progress_label = ttk.Label(parent, text="0%", background=frame_bg)
        # self.progress_label.pack()

        # Submit button
        self.submit_btn = ttk.Button(parent, text="Upload File", command=self.run_action, bootstyle=(PRIMARY))
        self.submit_btn.pack(pady=(60, 20), ipadx=10, ipady=4)

        # Result message
        self.result_label = ttk.Label(parent, text="", font=("Segoe UI", 10))
        self.result_label.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=filename, foreground="#333")
    
    def update_progress(self, progress):
        # print(progress * 100)
        self.progress_label.config(text=f"{progress * 100:.2f}%")
        self.progress_bar["value"] = progress * 100

    def run_action(self):
        if self.selected_file is None:
            return 0
        
        # Show the progress bar and label
        self.progress_bar.pack(pady=10)
        self.progress_label.pack()

        uploader = UploadToDrive()  # Create an instance of the Uploader class

        from tkinter import messagebox

        # Reset progress bar at the beginning
        self.progress_bar["value"] = 0
        self.progress_label.config(text="0%")

        def run_upload():
            try:
                self.submit_btn.config(state="disabled")
                self.browse_button.config(state="disabled")

                result = uploader.upload_or_replace_file(
                    self.selected_file,
                    progress_callback=self.update_progress
                )
                self.submit_btn.config(state="normal")

                self.browse_button.config(state="normal")
                self.after(0, lambda: messagebox.showinfo("Success", result))
            except Exception as e:
                err = str(e)
                self.after(0, lambda: messagebox.showerror("Error", err))

        # Run upload in background
        threading.Thread(target=run_upload, daemon=True).start()
        # self.result_label.config(text=result, fg="#006400" if "Uploaded" in result or "Updated" in result else "#b00020")