from googleapiclient.http import MediaIoBaseUpload
import io, os, sys, requests
from io import BytesIO

class ChunkedFileReader(io.BufferedReader):
    def __init__(self, file_path, chunk_size=1024 * 1024):  # 1MB
        self.file_obj = open(file_path, 'rb')
        super().__init__(self.file_obj)
        self.chunk_size = chunk_size
        self.bytes_read = 0
        self.total_size = os.path.getsize(file_path)
        # while self.progress() <= 1.0:
        #     self.read()
        # self.close()

    def read(self, size=-1):
        chunk = super().read(self.chunk_size if size == -1 else size)
        self.bytes_read += len(chunk)
        return chunk

    def progress(self):
        return self.bytes_read / self.total_size if self.total_size else 0

    def close(self):
        super().close()
        self.file_obj.close()

        return 1.0
