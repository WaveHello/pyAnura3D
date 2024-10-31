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

class ModelResults:
    """
    Class to represent the results of the driver model
    """

    def __init__(self, results_folder_path):
        # Store the folder that the results are in
        self.results_folder_path = results_folder_path

        self.par_files = []
        self.num_par_files = len(self.par_files)
        self.out_file = None # init varaible to hold the outfile object
        # # Variables to hold the results from the incremental driver run
        # self.time          = None
        # self.stress_df     = None
        # self.strain_df     = None
        # self.state_vars_df = None

    def __str__(self) -> str:
        return_string = (
                         f"Results folder path: {self.results_folder_path}\n"
                         f"Number of par files: {self.par_files}\n"
        )

        return return_string

    def load_par_files(self, load_all_data: bool):
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
                par_file_obj = ParFile(par_file_path)  # Adjust based on actual class

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

    # def get_output_file_as_df(self):
    #     """
    #     Return the output file as a df
    #     """

    #     # Read the file as a df, delim using white space
    #     df = pd.read_csv(self.output_file_path, sep = '\\s+')

    #     return df

    # def store_output_file_as_df(self):
    #     """
    #     Read the output file
    #     """
    #     df = self.get_output_file_as_df()

    #     # Store the df
    #     self.output_df = df

    # def store_times(self,
    #                 col_names = ["time(1)", "time(2)"]):
    #     """
    #     Store the times
    #     TODO: Don't know the difference between time1 and 2
    #     """

    #     if self.output_df is None:
    #         df = self.get_output_file_as_df()
    #     else:
    #         df = self.output_df

    #     self.time_df = df[col_names]
 
    # def store_output_stress(self, 
    #                        col_names = ["stress(1)", "stress(2)", "stress(3)", 
    #                                     "stress(4)", "stress(5)", "stress(6)"]):
    #     """
    #     Store the stress terms
    #     """

    #     if self.output_df is None:
    #         df = self.get_output_file_as_df()
    #     else:
    #         # df already stored
    #         df = self.output_df

    #     self.stress_df = df[col_names]

    # def store_output_strains(self,
    #                          col_names = ["stran(1)", "stran(2)", "stran(3)",
    #                                       "stran(4)", "stran(5)", "stran(6)"]):
    #     if self.output_df is None:
    #         df = self.get_output_file_as_df()
    #     else:
    #         df = self.output_df

    #     self.strain_df = df[col_names]

    # def store_output_state_vars(self, substring = "statev"):
    #     """
    #     Gets the state variables from the output.txt file
    #     """

    #     if self.output_df is None:
    #         df = self.get_output_file_as_df()
    #     else:
    #         df = self.output_df
        
    #     # Get the column names that have statv in them
    #     # The number of them depends on the model
    #     # Incremental driver always outputs at least one even if zero are passed
    #     # TODO: look into this
    #     col_names = [name for name in df.columns if "statev" in name]

    #     self.state_vars_df = df[col_names]

    # def store_all(self):
    #     """
    #     Store the df and each of the variables
    #     """
    #     self.store_output_file_as_df()

    #     # Store the stress variables
    #     self.store_output_stress()
        
    #     # Store the strain variables
    #     self.store_output_strains()

    #     # Store the state variables
    #     self.store_output_state_vars()

    # def get_mean_stress(self):
    #     """
    #     Returns the mean stress applied to a df
    #     """

    #     mean_stress = self.stress_df.apply(calc_mean_stress, axis = 1)

    #     return mean_stress
    
    # def get_q_invariant(self):
    #     """
    #     Returns the deviatoric stress invariant
    #     """

    #     q = self.stress_df.apply(calc_q_invariant, axis = 1)

    #     return q

    # def get_volumetric_strain(self):
    #     """
    #     Returns the volumetric strain using the strain df
    #     """
    #     eps_p = self.strain_df.apply(calc_volumetric_strain_invariant, axis = 1)

    #     return eps_p
    
    # def get_deviatoric_strain(self):
    #     """
    #     Returns the deviatoric strain
    #     """
    #     eps_q = self.strain_df.apply(lambda row: calc_dev_strain_invariant(row), axis = 1)

    #     return eps_q
    
    # def quick_plot_stress(self, figsize = (8, 4), compression_pos = True, axs = None, **kwargs):
    #     """
    #     Make the q vs. p plot
    #     """

    #     # Assumes that the stress variables are already loaded
    #     # Make the figure if no axs object is passed
    #     if axs is None:
    #         fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize = figsize)
        
    #     # Check if compression should be positive
    #     if compression_pos:
    #         sign = -1.0
    #     else:
    #         sign = 1.0

    #     # Calc the q invariant
    #     mean_stress = sign * self.get_mean_stress()
    #     q           = self.get_q_invariant()

    #     axs.plot(mean_stress, q, **kwargs)

    #     # Format the plot
    #     axs.set_title("Deviatoric Stress vs. Mean Stress")
    #     axs.set_xlabel("Mean Stress")
    #     axs.set_ylabel("Deviatoric Stress")

    # def quick_plot_strain(self, figsize = (8, 4), compression_pos = True, axs = None, **kwargs):
    #     """
    #     Make the $eps_q$ vs. $eps_v$ plot
    #     """

    #     # Check if compression should be positive
    #     if compression_pos:
    #         sign = -1.0
    #     else:
    #         sign = 1.0

    #     if axs is None:
    #         fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize = figsize)
        
    #     eps_p = sign * self.get_volumetric_strain()
    #     eps_q = self.get_deviatoric_strain()

    #     axs.plot(eps_p, eps_q, **kwargs)

    #     axs.set_title(r"$\epsilon_{q}$ vs. $\epsilon_{p}$ invariants")
    #     axs.set_xlabel(r"Volumetric strain invariant, $\epsilon_{p}$")
    #     axs.set_ylabel(r"Deviatoric strain invar, $\epsilon_{q}$")

    # def quick_quad_plot(self, axs = None, figsize = (10,10), axial_strain_id = "stran(1)",
    #                     stress_units = "kPa", strain_units = "-",
    #                     compression_pos = True, legend = False, **kwargs):
    #     """
    #     Make the quad plot that is really helpful for visualizing soil
    #     """

    #     # Make the figure and axs if no axs is passed in
    #     if axs is None:
    #         fig, axs = plt.subplots(nrows = 2, ncols = 2, figsize = figsize)

    #     if compression_pos:
    #         # flip the sign of the values
    #         sign = -1.0
    #     else:
    #         sign = 1.0

    #     # Get the data
    #     axial_strain = sign * self.strain_df[axial_strain_id]
    #     mean_stress  = sign * self.get_mean_stress()
    #     q            = self.get_q_invariant()
    #     vol_strain   = sign * self.get_volumetric_strain()


    #     # Make the q vs. axial strain \epsilon_{a}
    #     axs[0, 0].plot(axial_strain, q, **kwargs)

    #     # Format plot
    #     axs[0,0].set_title(r"q vs. $\epsilon_{a}$")
    #     axs[0,0].set_xlabel(r"$\epsilon_{a}$ " + f"[{strain_units}]")
    #     axs[0,0].set_ylabel(f"q [{stress_units}]")
        
    #     if legend:
    #         axs[0,0].legend()

    #     # Make the q vs. p plot
    #     axs[0, 1].plot(mean_stress, q, **kwargs)

    #     # Format the plot
    #     axs[0, 1].set_title(r"q vs. p")
    #     axs[0, 1].set_xlabel(f"p [{stress_units}]")
    #     axs[0, 1].set_ylabel(f"q [{stress_units}]")

    #     if legend:
    #         axs[0, 1].legend()

    #     # Make the \epislon_{v} vs \epsilon_{a} plot
    #     axs[1, 0].plot(axial_strain, vol_strain, **kwargs)
        
    #     # Format the plot
    #     axs[1, 0].set_title(r"$\epsilon_{v}$ vs. $\epsilon_{a}$")
    #     axs[1, 0].set_xlabel(r"$\epsilon_{a}$" +  f"[{strain_units}]")
    #     axs[1, 0].set_ylabel(r"$\epsilon_{v}$" +  f"[{strain_units}]")

    #     if legend:
    #         axs[1, 0].legend()

    #     # Make the \episilon_{v} vs. p plot
    #     axs[1, 1].plot(mean_stress, vol_strain, **kwargs)

    #     # Format the plots
    #     axs[1, 1].set_title(r"$\epsilon_{v}$ vs. p")
    #     axs[1, 1].set_xlabel(f"p [{stress_units}]")
    #     axs[1, 1].set_ylabel(r"$\epsilon_{v}$" +  f"[{strain_units}]")

    #     if legend:
    #         axs[1, 1].legend()

    #     # Help make the plots not overlap
    #     plt.tight_layout()


