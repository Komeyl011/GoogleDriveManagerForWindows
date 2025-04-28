import os, uploader, threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from uploader import UploadToDrive

class DriveFileManager(ttk.Frame):
    MB = 1048576
    
    def __init__(self, parent):
        super().__init__(parent)
        self.drive_client = uploader.ManageFiles()
        self.pack(fill=BOTH, expand=True)
        self.style = ttk.Style()

        self.create_widgets()
        self.refresh_file_list()

    def create_widgets(self):
        # Title
        title = ttk.Label(self, text="📂 Drive File Manager", font=("Segoe UI", 14, "bold"), foreground="#333")
        title.pack(pady=10)

        # Treeview
        self.style.configure("Custom.Treeview",
            borderwidth=0,
            ipadx=10
        )

        columns = ("name", "id", "size")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        self.tree.config(style="Custom.Treeview")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.heading("name", text="File Name")
        self.tree.heading("id", text="File ID")
        self.tree.heading("size", text="Size (MB)")
        self.tree.column("name", width=200)
        self.tree.column("id", width=200)
        self.tree.column("size", width=80, anchor="center")

        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        self.tree.pack(padx=15, pady=10, fill="both", expand=True)

        # Action buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        self.refresh_btn = ttk.Button(btn_frame, text="🔄 Refresh", command=self.refresh_file_list)
        self.refresh_btn.pack(side="left", padx=5)
        
        self.dl_btn = ttk.Button(btn_frame, text="⬇️ Download", command=self.download_selected)
        self.dl_btn.pack(side="left", padx=5)
        self.del_btn = ttk.Button(btn_frame, text="🗑️ Delete", command=self.delete_selected)
        self.del_btn.pack(side="left", padx=5)

    def refresh_file_list(self):
        self.after(0, lambda: self.config(cursor="wait"))
        self.refresh_btn.config(bootstyle=OUTLINE, state="disabled")
        self.dl_btn.config(state="disabled")
        self.del_btn.config(state="disabled")

        def refresh():
            files = self.drive_client.list_files()

            def update_ui():
                for item in self.tree.get_children():
                    self.tree.delete(item)

                for f in files:
                    if not f['trashed']:
                        size_in_bytes = int(f.get("size", 0))
                        size_mb = f"{size_in_bytes / self.MB:.2f}"
                        self.tree.insert("", "end", values=(f["name"], f["id"], size_mb))

                self.config(cursor="")
                self.refresh_btn.config(bootstyle=PRIMARY, state="normal")
                self.dl_btn.config(state="normal")
                self.del_btn.config(state="normal")

            self.after(0, update_ui)

        threading.Thread(target=refresh, daemon=True).start()

    def get_selected_file(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a file.")
            return None
        return self.tree.item(selected)["values"]

    def download_selected(self):
        file = self.get_selected_file()
        if file:
            save_path = os.path.join(os.path.expanduser("~"), "Downloads", file[0])
            success, path = self.drive_client.download_file(file[1], save_path)
            if success:
                messagebox.showinfo("Downloaded", f"File saved to: {path}")
            else:
                messagebox.showerror("Error", "Failed to download file.")

    def delete_selected(self):
        file = self.get_selected_file()
        if file:
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{file[0]}'?")
            if confirm:
                success = self.drive_client.delete_file(file[1])
                if success:
                    messagebox.showinfo("Deleted", f"File '{file[0]}' was deleted.")
                    self.refresh_file_list()
                else:
                    messagebox.showerror("Error", "Failed to delete file.")