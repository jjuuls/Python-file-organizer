"""Python File Organizer Script
Organizes files in the user's Downloads folder
into categorized subfolders by file types.
"""

from pathlib import Path as pt
from datetime import datetime

# Target folder to organize
downloads_path = pt.home() / "Downloads"

# File categories mapped to supported extensions
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Spreadsheets": [".xlsx", ".csv"],
    "Videos": [".mp4", ".mov"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"]
}

# Log all actions with timestamps to a log file for troubleshooting and record-keeping
def log_message(message):
    with open("organizer.log", "a") as log_file:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_file.write(f"{timestamp}: {message}\n")

# Main organizer function
def organize_downloads():

    moved_files = 0

    # Iterate through all items in the Downloads folder
    for file in downloads_path.iterdir():

        # Track whether file matched a supported category
        matched = False

        # Only process files, skip directories/folders
        if file.is_file():

            # Check file extension against defined categories
            for folder_name, extensions in file_types.items():
                
                # Compare file extension to supported extensions for the category
                if file.suffix.lower() in extensions:

                    # Move file and track successful move 
                    if move_file(file, folder_name):

                        moved_files += 1

                        matched = True

                        # Once a match is found and file is moved, no need to check other categories
                        break

            # Log unsupported file types
            if not matched:

                message = f"Skipped unsupported file type: {file.name}"           

                log_message(message)
                
                print(message)
    
    print(f"Finished organizing: {moved_files} files.")

# Function to move a file and handle errors
def move_file(file, folder_name):

    folder_path = downloads_path / folder_name

    # Create folder if it doesn't already exist
    folder_path.mkdir(exist_ok=True)

    new_location = folder_path / file.name
    
    try:
        
        file.rename(new_location)
        
        message = f"Moved {file.name} to {folder_name}"
        
        log_message(message)
        
        print(message)
        
        return True

    # Handle duplicate file names
    except FileExistsError:
        
        message = f"{file.name} already exists in {folder_name}. Skipping."
        
        log_message(message)
        
        print(message)
        
        return False

    # Handle restricted or locked files    
    except PermissionError:
        
        message = f"Permission denied for {file.name}. Skipping."
        
        log_message(message)
        
        print(message)
        
        return False

    # Handle any other unexpected errors 
    except Exception as e:
       
        message = f"Error moving {file.name}: {e}"
        
        log_message(message)
        
        print(message)

        return False

# Run script directly 
if __name__ == "__main__":
    organize_downloads()        

