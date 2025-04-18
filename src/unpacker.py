import os
import struct
import zstandard as zstd
from getpass import getpass

from encryption import hash, derive_key, decrypt_data

def unpack_archive(archive_path, output_path):
    # Zstd decompressor
    decompressor = zstd.ZstdDecompressor()

    # Getting size of archive
    archive_size = os.path.getsize(archive_path)

    with open(archive_path, "rb") as archive:
        # Checking if archive header exists
        archive_header = archive.read(12)
        if (archive_header != b"ARCHIVE_TOOL"):
            print("Can't find the archive header.")
            return

        # Compressed bool
        compressed = struct.unpack("?", archive.read(1))[0]

        # Checking if file is encrypted
        encrypted = struct.unpack("?", archive.read(1))[0]
        if (encrypted == True):
            # Asking for password
            print("This archive needs a password.")
            password = getpass("Enter password: ")

            # Getting hashed password and salt
            hashed_password = archive.read(32)
            salt = archive.read(32)

            # Checking if passwords matches
            if (hashed_password != hash(password, salt)[0]):
                print("\nPasswords do not match.")
                return
            
            # Getting key
            key = derive_key(password, salt)
        
        # Start of progress
        print("")
        print(f"\tUnpacking archive: {os.path.basename(archive_path)} => 0%", end="\r")
        
        # Looping until the stream has reached the end of the file
        while archive.tell() != archive_size:
            # File type
            file_type = struct.unpack("B", archive.read(1))[0]

            # Directories
            if (file_type == 0):
                # Getting directory path
                relative_path_length = struct.unpack("I", archive.read(4))[0]
                relative_path = archive.read(relative_path_length)

                # Decrypting data
                if (encrypted == True):
                    relative_path = decrypt_data(relative_path, key).decode("utf-8")
                else:
                    relative_path = relative_path.decode("utf-8")

                # Putting togheter full directory path
                directory_path = os.path.join(output_path, relative_path)

                # Creating directory if it does not exists
                if (os.path.exists(directory_path) == False):
                    os.makedirs(directory_path)
            
            # Files
            elif (file_type == 1):
                # Getting file path
                relative_path_length = struct.unpack("I", archive.read(4))[0]
                relative_path = archive.read(relative_path_length)
                
                # Getting file data
                file_size = struct.unpack("Q", archive.read(8))[0]
                file_data = archive.read(file_size)

                # Decrypting data
                if (encrypted == True):
                    relative_path = decrypt_data(relative_path, key).decode("utf-8")
                    file_data = decrypt_data(file_data, key)
                else:
                    relative_path = relative_path.decode("utf-8")

                # Decompressing data
                if (compressed == True):
                    file_data = decompressor.decompress(file_data)
                
                # Putting togheter full file path
                file_path = os.path.join(output_path, relative_path)
                
                # Creating directory if it does not exists
                directory = os.path.dirname(file_path)
                if (os.path.exists(directory) == False):
                    os.makedirs(directory)

                # Writing the data to the file
                with open(file_path, "wb") as f:
                    f.write(file_data)
            
            # Updating progress
            print(f"\tUnpacking archive: {os.path.basename(archive_path)} => {round(archive.tell()/archive_size*100)}%", end="\r")

    # End of progress
    print("\n")
    print(f"Archive contents located at: {output_path}")
