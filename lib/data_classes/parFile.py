import datetime
import os
import pandas as pd  # Import pandas for easy CSV parsing

# Library imports
from lib.data_classes.fileClass import File

class ParFile(File):
    """
    A class to represent a .PAR_ file with specific parsing functionality.

    This class inherits from the File class, adding specific capabilities for 
    reading and processing .PAR_ files, which are space-separated CSVs with a header.

    Attributes
    ----------
    header : list
        A list to store the header information from the .PAR_ file.
    data : pd.DataFrame
        A DataFrame to store the data from the .PAR_ file.

    Methods
    -------
    load_data()
        Reads the .PAR_ file, extracts the header and data, and stores them.
    """

    def __init__(self, file_dir):
        """
        Initialize a ParFile object with the file directory.

        Parameters
        ----------
        file_dir : str
            The directory of the .PAR_ file to be associated with this ParFile object.
        """
        super().__init__(file_dir)
        self.header = []  # List to store header information
        self.data = pd.DataFrame()  # DataFrame to store data
        self.data_loaded = False # Init flag to keep track when the data is loaded

    def __str__(self):
        info = (
                f"File Name: {self.file_name}\n"
                f"Data Loaded: {self.data_loaded}\n"
        )
        return info
    
    def load_data(self):
        """
        Load the .PAR_ file, extracting the header and data.

        This method reads the file, assumes the header occupies the first line(s),
        and that the data is space-separated. It loads the header and data into 
        the `header` and `data` attributes, respectively.

        Raises
        ------
        FileNotFoundError
            If the .PAR_ file does not exist.
        ValueError
            If the file format is not as expected.
        """
        # Check if file exists
        if not os.path.exists(self.file_dir):
            raise FileNotFoundError(f"The file {self.file_dir} does not exist.")

        with open(self.file_dir, 'r') as f:
            # Read header (assuming it is the first line)
            self.header = f.readline().strip().split()  # Adjust if more header lines exist

        # Load data (assumes space-separated values)
        self.data = pd.read_csv(self.file_dir, sep=r'\s+', skiprows=1, names=self.header)

        # Set the flag since the data is loaded
        self.data_loaded = True

    def get_header(self):
        """
        Returns the header of the .PAR_ file.

        Returns
        -------
        list
            The header information as a list of column names.
        """
        return self.header

    def get_data(self):
        """
        Returns the data from the .PAR_ file.

        Returns
        -------
        pd.DataFrame
            The data contained in the .PAR_ file as a DataFrame.
        """
        return self.data

if __name__ == "__main__":
    # Example usage
    par_file = ParFile("path/to/file.PAR_")
    par_file.load_data()
    print("Header:", par_file.get_header())
    print("Data:\n", par_file.get_data())
