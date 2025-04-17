import tkinter as tk
from tkinter import ttk, messagebox
import os

class DriveFileManager(tk.Frame):
    MB = 1048576
    
    def __init__(self, parent, drive_client):
        super().__init__(parent, bg="#f7f7f7")
        self.drive_client = drive_client
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.refresh_file_list()

    def create_widgets(self):
        # Title
        title = tk.Label(self, text="📂 Drive File Manager", font=("Segoe UI", 14, "bold"), bg="#f7f7f7", fg="#333")
        title.pack(pady=10)

        # Treeview
        columns = ("name", "id", "size")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
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
        btn_frame = tk.Frame(self, bg="#f7f7f7")
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="🔄 Refresh", command=self.refresh_file_list).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="⬇️ Download", command=self.download_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ Delete", command=self.delete_selected).pack(side="left", padx=5)

    def refresh_file_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        files = self.drive_client.list_files()
        for f in files:
            # size_kb = int(f.get("size", 0)) // self.MB if "size" in f else "-"
            size_in_bytes = int(f.get("size", 0))
            size_mb = f"{size_in_bytes / self.MB:.2f}"
            self.tree.insert("", "end", values=(f["name"], f["id"], size_mb))

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
