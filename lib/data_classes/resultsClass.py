# Standard imports
import os
import pandas as pd
import matplotlib.pyplot as plt

# Lib imports
from lib.data_classes.parFile import ParFile
from lib.data_classes.outFile import OutFile

from lib.general_functions.invariant_functions import (
     calc_mean_stress, calc_q_invariant, calc_dev_strain_invariant, calc_volumetric_strain_invariant
)

from lib.data_classes.gomClass import GomFile

class ModelResults:
    """
    Class to represent the results of the driver model
    """

    def __init__(self, results_folder_path, flag_3D = True):
        # Store the folder that the results are in
        self.results_folder_path = results_folder_path

        self.par_files = []
        self.num_par_files = len(self.par_files)
        self.out_file = None # init varaible to hold the outfile object
        self.flag_3D = flag_3D # Store if the model is 3D or not

    def __str__(self) -> str:
        return_string = (
                         f"Results folder path: {self.results_folder_path}\n"
                         f"Number of par files: {self.par_files}\n"
        )

        return return_string

    def load_par_files(self, load_all_data: bool, flag_3D):
        """
        Load the .PAR_ files in the results folder and create par file objects.

        Purpose:
        This method iterates through the results folder to find all files with the
        `.PAR_` extension. For each file found, it creates a par file object, and if
        `load_all_data` is True, it loads the data using the appropriate method.

        Parameters:
        load_all_data (bool): If True, calls the par file method to load the data.

        Returns:
        None
        """

        # Get the path to the results folder (assumes self.results_folder is defined)
        results_folder = self.results_folder_path

        # List to store par file objects
        self.par_files = []

        # Traverse through the results folder to find .PAR_ files
        for filename in os.listdir(results_folder):
            if '.PAR_' in filename:
                # Create a par file object (assuming a ParFile class exists)
                par_file_path = os.path.join(results_folder, filename)
                par_file_obj = ParFile(par_file_path, flag_3D)  # Adjust based on actual class

                # Add to par file list
                self.par_files.append(par_file_obj)

                # Load data if load_all_data is True
                if load_all_data:
                    par_file_obj.load_data()  # Adjust based on actual load method

        # Log completion
        print(f"Loaded {len(self.par_files) - self.num_par_files} par files from {results_folder}")
        
        # Update the number of par files
        self.num_par_files = len(self.par_files)
    
    def load_out_file(self):
        """
        Load the out file. This is the file that stores the terminal output of the Anura3D model
        """

        # Get the path to the results folder (assumes self.results_folder is defined)
        results_folder = self.results_folder_path

        for filename in os.listdir(results_folder):
            if '.OUT' in filename:
                # Create a par file object (assuming a ParFile class exists)
                out_file_path = os.path.join(results_folder, filename)
                out_file_obj = OutFile(out_file_path)  # Adjust based on actual class

                # Load the data into the out file obj
                out_file_obj.load_data()

                # Add to par file list
                self.out_file = out_file_obj