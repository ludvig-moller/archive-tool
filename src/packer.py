import os
import struct

def pack_folder(folder_path, archive_path):
    with open(archive_path, "wb") as archive:

        # Archive header
        archive.write(b"SQUISHED_ARCHIVE")

        # Loop through directories and files in folder
        for root, dirs, files in os.walk(folder_path):

            # Adding files
            for file in files:
                # Getting the all file data
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    file_data = f.read()

                # Getting relative path
                relative_path = os.path.relpath(file_path, folder_path).encode("utf-8")

                # Writing file data to the archive
                archive.write(struct.pack("I", len(relative_path))) # Relative path length
                archive.write(relative_path) # Relative path
                archive.write(struct.pack("Q", len(file_data))) # File size
                archive.write(file_data) # File data
