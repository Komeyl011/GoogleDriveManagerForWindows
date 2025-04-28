@echo off
set /p target=Enter the version: 
echo Building "GoogleDriveUploader.final.v%target%"...
pyinstaller --onefile --clean --windowed --disable-windowed-traceback^
    --name="GoogleDriveUploader.final.v%target%" --add-data="./credentials.json;." --add-data="./drive_uploader.png;." ^
    --add-data="C:\Users\Komeil\AppData\Roaming\Python\Python312\site-packages\certifi\cacert.pem;certifi" ^
    --icon="./drive_uploader.ico" main.py
pause