import os
import struct
import zstandard as zstd

def unpack_archive(archive_path, folder_path):
    decompressor = zstd.ZstdDecompressor()

    # Getting size of archive
    archive_size = os.path.getsize(archive_path)

    with open(archive_path, "rb") as archive:
        # Checking if archive header exists
        archive_header = archive.read(16)
        if (archive_header != b"SQUISHED_ARCHIVE"):
            return
        
        # Looping until the stream has reached the end of the file
        while archive.tell() != archive_size:
            # Getting file path
            relative_path_length = struct.unpack("I", archive.read(4))[0]
            relative_path = archive.read(relative_path_length).decode("utf-8")
            file_path = os.path.join(folder_path, relative_path)

            # Checking if path exists. If not creating directories
            directory_path = os.path.dirname(file_path)
            if (not os.path.exists(directory_path)):
                os.makedirs(directory_path)

            # Compressed bool
            compressed = struct.unpack("?", archive.read(1))[0]
            
            # Getting file data
            file_size = struct.unpack("Q", archive.read(8))[0]
            file_data = archive.read(file_size)

            if (compressed == True):
                file_data = decompressor.decompress(file_data)

            # Writing the data to the file
            with open(file_path, "wb") as f:
                f.write(file_data)
