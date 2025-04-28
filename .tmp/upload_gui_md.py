import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Google Drive Uploader")
        self.geometry("1000x600")
        self.minsize(800, 500)

        self.grid_columnconfigure(0, weight=0)  # self.sidebar (fixed)
        self.grid_columnconfigure(1, weight=1)  # Left spacer (10%)
        self.grid_columnconfigure(2, weight=8)  # Main content (80%)
        self.grid_columnconfigure(3, weight=1)  # Right spacer (10%)
        self.grid_rowconfigure(0, weight=1)


        self.create_sidebar()
        self.uploader_frame()

        self.current_frame = None
        
        self.show_frame("Upload")  # default

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self)
        self.sidebar.pack(side="left", fill="y", padx=10)

        title = ctk.CTkLabel(self.sidebar, text="Uploader", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=20, padx=5, fill='x')

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")

        upload_btn = ctk.CTkButton(self.sidebar,
                                   text="Upload",
                                   image=ctk.CTkImage(
                                       light_image=Image.open(os.path.join(image_path, "cloud-arrow-up.png")),
                                       dark_image=Image.open(os.path.join(image_path, "cloud-arrow-up-d.png")),
                                       size=(25, 20)
                                    ),
                                   anchor="w", command=lambda:self.show_frame("Upload"))
        upload_btn.pack(fill="x", pady=5, padx=5)

        settings_btn = ctk.CTkButton(self.sidebar,
                                     text="File Manager",
                                     image=ctk.CTkImage(
                                         light_image=Image.open(os.path.join(image_path, "folder-open.png")),
                                         dark_image=Image.open(os.path.join(image_path, "folder-open-d.png")),
                                         size=(25, 23)
                                     ),
                                     anchor="w", command=lambda:self.show_frame("File Manager"))
        settings_btn.pack(fill="x", pady=5, padx=5)

        # Main content area
        self.main_content = ctk.CTkFrame(self)
        self.main_content.pack(side="right", fill="both", expand=True)

        self.frames = {}

        appearance = ctk.CTkOptionMenu(self.sidebar, values=["System", "Light", "Dark"],
                                       command=ctk.set_appearance_mode)
        appearance.set("System")
        appearance.pack(pady=20, padx=10)

    def uploader_frame(self):
        main_frame = ctk.CTkFrame(self.main_content)

        title = ctk.CTkLabel(main_frame, text="📁 Google Drive Uploader", font=("Segoe UI", 20, "bold"))
        title.pack(pady=40)

        # File selection
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack()

        self.file_label = ctk.CTkLabel(file_frame, text="No file selected", anchor="w")
        self.file_label.pack(side="left", padx=(10, 5), fill="x")

        browse_btn = ctk.CTkButton(file_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side="right", padx=10, fill="x")

        # Progress
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack()

        self.progress_label = ctk.CTkLabel(main_frame, text="0%")
        self.progress_label.pack()

        # Upload Button
        upload_btn = ctk.CTkButton(main_frame, text="Upload File", command=self.upload_file)
        upload_btn.pack()

        # Result
        self.result_label = ctk.CTkLabel(main_frame, text="", font=("Segoe UI", 10))
        self.result_label.pack()

        return main_frame
    
    def file_manager_frame(self):
        frame = ctk.CTkFrame(self.main_content)
        label = ctk.CTkLabel(frame, text="💬 Frame 2", font=("Arial", 24))
        label.pack(pady=20)
        return frame

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_label.configure(text=file_path.split("/")[-1])
            self.result_label.configure(text="")

    def upload_file(self):
        self.progress_bar.set(0.4)  # Simulate progress
        self.progress_label.configure(text="40%")
        self.result_label.configure(text="✅ Upload complete!")

    def show_frame(self, name):
        if self.current_frame:
            self.current_frame.pack_forget()

        if name not in self.frames:
            if name == "Upload":
                self.frames[name] = self.uploader_frame()
            elif name == "File Manager":
                self.frames[name] = self.file_manager_frame()

        self.current_frame = self.frames[name]
        # self.current_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.current_frame.pack(fill="both", pady=40, expand=True, anchor="center")

if __name__ == "__main__":
    app = App()
    app.mainloop()
