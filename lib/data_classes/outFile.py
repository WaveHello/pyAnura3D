"""
Class to represent the OUT file. 
This file contains the output of the Anura3D simulation
"""
import os

from lib.data_classes.fileClass import File

class OutFile(File):

    def __init__(self, file_dir):
        super().__init__(file_dir)
    
    # Add some other functions here later that let you

    def load_data(self):
        """
        Read in the data from the file
        """
        if not os.path.exists(self.file_dir):
            raise FileNotFoundError(f"The file {self.file_dir} does not exist.")
    
        with open(self.file_dir, "r", encoding='ISO-8859-1') as f:
            self.data = f.readlines()
    
    def print_data(self):
        """
        Returns the file data
        """
        
        for line in self.data:
            print(line.strip())



        
