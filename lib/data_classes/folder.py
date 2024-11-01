import os  # Import the os module for operating system functions
import datetime  # Import the datetime module for handling dates and times
import fnmatch  # Import fnmatch module for filename matching
import glob  # Import glob module for pathname matching
from pathlib import Path  # Import Path class from pathlib module
import os
import shutil

from lib.general_functions.general_functions import delete_files_with_extensions

class Folder:
    """
    Base class for managing folders.

    This class provides methods to interact with and manage files within a specified folder directory.

    Attributes
    ----------

    folder_dir : str
        The directory path of the folder.

    Methods
    -------

    __init__(folder_dir)
        Initialize the Folder object with the specified folder directory.
    __str__()
        Return a string representation of the Folder object.
    get_num_files(file_extension, recursive)
        Get the number of files in the folder with a specific file extension.
    get_directories_by_extension(file_extension, recursive, subfolder="")
        Get a list of file directories with a specific file extension in the folder.
    """

    def __init__(self, folder_dir):
        """
        Initialize the Folder object with the specified folder directory.

        Parameters
        ----------

        folder_dir : str
            The directory path of the folder.
        """
        self.folder_dir = folder_dir  # Store the folder directory

    def __str__(self):
        """
        Return a string representation of the Folder object.

        Returns
        -------

        str
            A string representing the folder directory.
        """
        return f"Folder dir: {self.folder_dir}"

    def get_num_files(self, file_extension, recursive):
        """
        Get the number of files in the folder with a specific file extension.

        Parameters
        ----------

        file_extension : str
            The file extension (e.g., '.txt', '.csv').
        recursive : bool
            Boolean flag to indicate whether to search subdirectories recursively.

        Returns
        -------

        int
            The number of files with the specified extension.
        """
        # Count files matching the file extension in the folder
        count = len(glob.glob(self.folder_dir + "/*" + file_extension, recursive=recursive))
        return count

    def get_directories_by_extension(self, file_extension, recursive, subfolder=""):
        """
        Get a list of file directories with a specific file extension in the folder.

        Parameters
        ----------

        file_extension : str
            The file extension (e.g., '.txt', '.csv').
        recursive : bool
            Boolean flag to indicate whether to search subdirectories recursively.
        subfolder : str, optional
            Optional subfolder name to search within.

        Returns
        -------
        
        list of str
            List of file directories matching the criteria.
        """
        file_dirs = []

        # Handle subfolder path construction
        if subfolder != "":
            subfolder = "/" + subfolder

        # Handle recursive search based on the flag
        if recursive:
            # Search recursively for files matching the extension
            for file in glob.glob(self.folder_dir + subfolder + "/**/*." + file_extension, recursive=True):
                file_path = os.path.join(self.folder_dir, file)
                file_dirs.append(file_path)
        else:
            # Search in the specified subfolder for files matching the extension
            for file in glob.glob(self.folder_dir + subfolder + "/*." + file_extension):
                file_path = os.path.join(self.folder_dir, file)
                file_dirs.append(file_path)

        return file_dirs
    
    def delete_folder_files(self, keep_extensions = ['.CPS_001', '.GOM', '.dll', '.out', '.exe', '.bat']):
        # Purpose: Delete all files in a folder except those with a certain extentension
        #TODO: Make this overwritable in the future
        delete_files_with_extensions(self.folder_dir, keep_extensions)

    def copy_files_2_folder(self, new_folder_dir):
        """
        Copy all files from the current folder to a new folder.
        
        Parameters:
        - new_folder_dir (str): Path to the new folder where files will be copied.
        """
        # Create the new folder if it doesn't exist
        os.makedirs(new_folder_dir, exist_ok=True)

        # Loop through all files in the current folder
        for filename in os.listdir(self.folder_dir):
            file_path = os.path.join(self.folder_dir, filename)
            
            # Only copy files (skip directories)
            if os.path.isfile(file_path):
                shutil.copy(file_path, new_folder_dir)



if __name__ == "__main__":
    from lib.data_classes.folder import Folder

    pass
