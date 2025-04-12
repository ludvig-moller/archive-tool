import os
import struct
import zstandard as zstd

from encryption import hash, derive_key, encrypt_data

def pack_folder(folder_path, archive_directory, archive_name, password, compress=True):
    # Zstd compressor
    compressor = zstd.ZstdCompressor(level=10)

    # Archive path
    archive_name += ".arct"
    archive_path = os.path.join(archive_directory, archive_name)

    with open(archive_path, "wb") as archive:

        # Archive header
        archive.write(b"SQUISHED_ARCHIVE")

        # Adding password
        if (password):
            archive.write(struct.pack("?", True))

            # Hashing password
            hashed_password, salt = hash(password)
            archive.write(hashed_password) # Hashed password
            archive.write(salt) # Salt

            # Getting encryption key
            key = derive_key(password, salt)
        else:
            archive.write(struct.pack("?", False))

        # Loop through directories and files in folder
        for root, dirs, files in os.walk(folder_path):
            # Adding directories
            for dir in dirs:
                # Getting archive relative path
                directory_path = os.path.join(root, dir)
                relative_path = os.path.relpath(directory_path, folder_path).encode("utf-8")

                # Writing directory data to archive
                archive.write(struct.pack("B", 0)) # File type. Directory = 0
                archive.write(struct.pack("I", len(relative_path))) # Relative path length
                archive.write(relative_path) # Relative path

            # Adding files
            for file in files:
                # Getting the all file data
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    file_data = f.read()
                
                # Compression
                if (compress == True):
                    file_data = compressor.compress(file_data)

                # Encryption
                if (password):
                    file_data = encrypt_data(file_data, key)

                # Getting relative path
                relative_path = os.path.relpath(file_path, folder_path).encode("utf-8")

                # Writing file data to the archive
                archive.write(struct.pack("B", 1)) # File type. File = 1
                archive.write(struct.pack("I", len(relative_path))) # Relative path length
                archive.write(relative_path) # Relative path
                archive.write(struct.pack("?", compress)) # Compressed bool
                archive.write(struct.pack("Q", len(file_data))) # File size
                archive.write(file_data) # File data
