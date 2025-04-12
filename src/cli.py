import argparse
from getpass import getpass

from packer import pack_folder
from unpacker import unpack_archive

def cli():
    parser = argparse.ArgumentParser(description="Pack folder into archives with optional compression and encryption")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Pack command
    pack_parser = subparsers.add_parser("pack", help="Pack a folder in to an archive.")
    pack_parser.add_argument("source", help="The path to the folder you want to pack.")
    pack_parser.add_argument("output", help="The path to the position you want to save your archive.")
    pack_parser.add_argument("name", help="The name of the archive.")
    pack_parser.add_argument("-e", "--encrypt", action="store_true", help="Letting you encrypt the archive with a password.")
    pack_parser.add_argument("-nc", "--no-compress", action="store_true", help="Disables the compression for this archive.")

    # Unpack command
    unpack_parser = subparsers.add_parser("unpack", help="Unpack an archive in to a folder.")
    unpack_parser.add_argument("archive", help="The path to the archive you want to unpack.")
    unpack_parser.add_argument("output", help="The path to the folder you want to unpack the contents of the archive.")

    # Parse args
    args = parser.parse_args()

    # Handle commands
    if (args.command == "pack"):
        # Get encryption password
        if (args.encrypt == True):
            print("You need to choose a password to encrypt.")
            password = getpass("Enter password: ")
        else:
            password = None

        # Get compression flag
        compress = not args.no_compress

        # Pack folder
        pack_folder(args.source, args.output, args.name, password=password, compress=compress)

    elif (args.command == "unpack"):
        # Unpack archive
        unpack_archive(args.archive, args.output)
