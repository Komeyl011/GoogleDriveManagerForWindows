import os
import sys
import uploader
import upload_gui_ttkbs
from tkinter import messagebox

if __name__ == "__main__":
    driveUploader = uploader.UploadToDrive()
    os.environ['SSL_CERT_FILE'] = driveUploader.get_resource_path("certifi/cacert.pem")

    check = driveUploader.check_authentication()
    if not check:
        success = driveUploader.authenticate()
        if not success:
            messagebox.showerror("Authentication Failed", "Login was cancelled or failed.")
            sys.exit(1)

    app = upload_gui_ttkbs.DriveUploaderGUI()
    app.mainloop()
