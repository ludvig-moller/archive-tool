import os
import struct
from functools import reduce
import operator

def list_archive(archive_path):
    # Getting size of archive
    archive_size = os.path.getsize(archive_path)

    with open(archive_path, "rb") as archive:
        # Checking if archive header exists
        archive_header = archive.read(16)
        if (archive_header != b"SQUISHED_ARCHIVE"):
            return
        
        # If encrypted move forward 64 bytes
        encrypted = struct.unpack("?", archive.read(1))[0]
        if (encrypted == True):
            archive.seek(64, 1)

        # Dictonairy for list all files
        archive_data = {}
        
        # Looping until the stream has reached the end of the file
        while archive.tell() != archive_size:
            # File type
            file_type = struct.unpack("B", archive.read(1))[0]

            # Directories
            if (file_type == 0):
                # Getting directory path
                relative_path_length = struct.unpack("I", archive.read(4))[0]
                relative_path = archive.read(relative_path_length).decode("utf-8")
                path_list = relative_path.split("\\")

                # Create the new directory
                reduce(operator.getitem, path_list[:-1], archive_data)[path_list[-1]] = {}

            # Files
            elif (file_type == 1):
                # Getting file path
                relative_path_length = struct.unpack("I", archive.read(4))[0]
                relative_path = archive.read(relative_path_length).decode("utf-8")
                path_list = relative_path.split("\\")

                # Skipping compressed bool
                archive.seek(1, 1)

                # Getting file size
                file_size = struct.unpack("Q", archive.read(8))[0]

                # Skipping file data
                archive.seek(file_size, 1)

                # Making file size readable
                if (file_size < 1000):
                    file_size = str(file_size) + "B"
                elif (file_size < 1000000):
                    file_size = str(round(file_size/1000, 2)) + "kB"
                elif (file_size < 1000000000):
                    file_size = str(round(file_size/1000000, 2)) + "MB"
                else:
                    file_size = str(round(file_size/1000000000, 2)) + "GB"

                # Adding file
                reduce(operator.getitem, path_list[:-1], archive_data)[path_list[-1]] = file_size
    
    # Creating string and printing results
    print(f"List of {os.path.basename(archive_path)}\n")
    for line in create_archive_string(archive_data):
        print(line)
    print("\nEnd of archive.")

def create_archive_string(dictionary, level=0):
    # Adding \t to every nested dictionary
    base_string = "\t"*level
    
    # Going through dictionary items
    # If the value is a dictionary it will call this function with a deeper level
    for key, value, in dictionary.items():
        yield f"{base_string}{key} {'- ' + str(value) if not isinstance(value, dict) else ''}"
        if (isinstance(value, dict)):
            yield from create_archive_string(value, level+1)
