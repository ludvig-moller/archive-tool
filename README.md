# Archive Tool

This is an archive tool made in Python with zstandard for compression and cryptography for encryption.

## Features

- Compression
- Encryption
- Listing archive content

## Installation

First navigate to the project folder in your terminal:

```
cd path/to/project-folder
```

Then run the following command:

```
pip install .
```

## Usage

Packing a folder into a archive

```
archive-tool pack "source" "output" "name" "--encrypt" "--no-compress"

Example:
archive-tool pack "C:\Desktop\my_folder" "C:\Desktop" "my_archive" --encrypt
```

Unpacking an archive

```
archive-tool unpack "archive" "output"

Example:
archive-tool unpack "C:\Desktop\my_archive.arct" "C:\Desktop\my_folder"
```

Listing contents of an archive

```
archive-tool pack "archive"

Example:
archive-tool unpack "C:\Desktop\my_archive.arct"
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
