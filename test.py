from the_directory_scanner import scan_directory

scan_result = scan_directory(directory=".", output_file_name="directory_structure.txt",
                             ignored_items=('.git', '.idea', 'venv', '__pycache__',))