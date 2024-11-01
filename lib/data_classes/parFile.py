import datetime
import os
import pandas as pd  # Import pandas for easy CSV parsing
import matplotlib.pyplot as plt

# Library imports
from lib.data_classes.fileClass import File
from lib.general_functions.invariant_functions import (calc_dev_strain_invariant, calc_mean_stress, calc_q_invariant, 
                                                       calc_volumetric_strain_invariant)

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

    def __init__(self, file_dir, flag_3D):
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
        self.flag_3D = flag_3D

        # Variables to hold the results from the incremental driver run
        # self.time          = None
        self.stress_df     = None
        self.strain_df     = None
        self.state_vars_df = None

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

        # Get the data and store it in the object
        self.header, self.data = self.get_data()

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
        if self.data_loaded:
            return self.header
        else:
            raise AttributeError("Data must be loaded first")

    def get_data(self):
        """
        Returns the data from the .PAR_ file.

        Returns
        -------
        pd.DataFrame
            The data contained in the .PAR_ file as a DataFrame.
        """
        if not self.data_loaded:
            # Check if file exists
            if not os.path.exists(self.file_dir):
                raise FileNotFoundError(f"The file {self.file_dir} does not exist.")

            with open(self.file_dir, 'r') as f:
                # Read header (assuming it is the first line)
                header = f.readline().strip().split()  # Adjust if more header lines exist

            # Load data (assumes space-separated values)
            data = pd.read_csv(self.file_dir, sep=r'\s+', skiprows=1, names=header)
        elif self.data_loaded:
            # The data is already loaded
            header = self.header
            data = self.data
        else:
            raise TypeError(f"self.data_loaded must be bool. Type is {type(self.data_loaded)}")

        return header, data

    def store_times(self,
                    col_names = ["time(1)", "time(2)"]):
        """
        Store the times
        TODO: Don't know the difference between time1 and 2
        """

        if self.output_df is None:
            df = self.get_output_file_as_df()
        else:
            df = self.output_df

        self.time_df = df[col_names]
 
    def store_output_stress(self, col_names = None):
        """
        Store the stress terms
        """
        # full_col_names = ["SigmaXX", "SigmaYY", "SigmaXX", "SigmaYY", "SigmaZZ", "SigmaXY", "SigmaYZ", "SigmaZX"]

        if self.flag_3D and col_names is None:
            col_names = ["SigmaXX", "SigmaYY", "SigmaXX", "SigmaYY", "SigmaZZ", "SigmaXY", "SigmaYZ", "SigmaZX"]
        elif not self.flag_3D and col_names is None:
            # 2d model
            col_names = ["SigmaXX", "SigmaYY", "SigmaZZ", "SigmaXY"] 
        
        # # Get the stress df
        # self.stress_df = pd.DataFrame(columns=full_col_names)
        # display(self.stress_df)
        # display(self.data[col_names])

        # # Get the length of the data
        # num_rows = self.data.shape[0]

        # # Make a list of zeros

        self.stress_df = self.data[col_names]

    def store_output_strains(self, col_names = None):
        # full_col_names = ["EpsilonXX", "EpsilonYY","EpsilonZZ","GammaXY","GammaYZ", "GammaZX"]

        if self.flag_3D and col_names is None:
            col_names = ["EpsilonXX", "EpsilonYY","EpsilonZZ","GammaXY","GammaYZ", "GammaZX"]

        elif not self.flag_3D and col_names is None:
            # 2d model
            col_names = ["EpsilonXX", "EpsilonYY", "EpsilonZZ", "GammaXY"] 

        self.strain_df = self.data[col_names]

    def get_mean_stress(self):
        """
        Returns the mean stress applied to a df
        """

        mean_stress = self.stress_df.apply(calc_mean_stress, axis = 1)

        return mean_stress
    
    def get_q_invariant(self):
        """
        Returns the deviatoric stress invariant
        """

        if self.flag_3D:
            q = self.stress_df.apply(calc_q_invariant, axis = 1)
        else:
            raise NotImplementedError("Calcing q for 2d isn't impelemented")
        
        return q

    def get_volumetric_strain(self):
        """
        Returns the volumetric strain using the strain df
        """
        if self.flag_3D:
            eps_p = self.strain_df.apply(calc_volumetric_strain_invariant, axis = 1)
        else:
            raise NotImplementedError("Calcing epsV for 2d isn't impelemented")
        return eps_p
    
    def get_deviatoric_strain(self):
        """
        Returns the deviatoric strain
        """
        if self.flag_3D:
            eps_q = self.strain_df.apply(lambda row: calc_dev_strain_invariant(row), axis = 1)
        else:
            raise NotImplementedError("Calculating epsq isn't implemented for 2D")
        return eps_q
    
    def quick_plot_stress(self, figsize = (8, 4), compression_pos = True, axs = None, **kwargs):
        """
        Make the q vs. p plot
        """

        # Assumes that the stress variables are already loaded
        # Make the figure if no axs object is passed
        if axs is None:
            fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize = figsize)
        
        # Check if compression should be positive
        if compression_pos:
            sign = -1.0
        else:
            sign = 1.0

        # Calc the q invariant
        mean_stress = sign * self.get_mean_stress()
        q           = self.get_q_invariant()

        axs.plot(mean_stress, q, **kwargs)

        # Format the plot
        axs.set_title("Deviatoric Stress vs. Mean Stress")
        axs.set_xlabel("Mean Stress")
        axs.set_ylabel("Deviatoric Stress")

    def quick_plot_strain(self, figsize = (8, 4), compression_pos = True, axs = None, **kwargs):
        """
        Make the $eps_q$ vs. $eps_v$ plot
        """

        # Check if compression should be positive
        if compression_pos:
            sign = -1.0
        else:
            sign = 1.0

        if axs is None:
            fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize = figsize)
        
        eps_p = sign * self.get_volumetric_strain()
        eps_q = self.get_deviatoric_strain()

        axs.plot(eps_p, eps_q, **kwargs)

        axs.set_title(r"$\epsilon_{q}$ vs. $\epsilon_{p}$ invariants")
        axs.set_xlabel(r"Volumetric strain invariant, $\epsilon_{p}$")
        axs.set_ylabel(r"Deviatoric strain invar, $\epsilon_{q}$")

    def quick_quad_plot(self, axs = None, figsize = (10,10), axial_strain_id = "EpsilonYY",
                        stress_units = "kPa", strain_units = "-",
                        compression_pos = True, legend = False, labels:list = [],
                          **kwargs):
        """
        Make the quad plot that is really helpful for visualizing soil
        """

        # Make the figure and axs if no axs is passed in
        if axs is None:
            fig, axs = plt.subplots(nrows = 2, ncols = 2, figsize = figsize)

        if legend and len(labels) == 1:
            # For the case when the label is the same for all the plots duplicate the single value
            labels = labels * 4

        elif legend and len(labels) != 4:
            raise IndexError("Length of labels has to be 1 or number of axs (4)")
            
        if compression_pos:
            # flip the sign of the values
            sign = -1.0
        else:
            sign = 1.0

        # Get the data
        axial_strain = sign * self.strain_df[axial_strain_id]
        mean_stress  = sign * self.get_mean_stress()
        q            = self.get_q_invariant()
        vol_strain   = sign * self.get_volumetric_strain()


        # Make the q vs. axial strain \epsilon_{a}
        axs[0, 0].plot(axial_strain, q, label = labels[0], **kwargs)

        # Format plot
        axs[0,0].set_title(r"q vs. $\epsilon_{a}$")
        axs[0,0].set_xlabel(r"$\epsilon_{a}$ " + f"[{strain_units}]")
        axs[0,0].set_ylabel(f"q [{stress_units}]")
        
        if legend:
            axs[0,0].legend()

        # Make the q vs. p plot
        axs[0, 1].plot(mean_stress, q, label = labels[1], **kwargs)

        # Format the plot
        axs[0, 1].set_title(r"q vs. p")
        axs[0, 1].set_xlabel(f"p [{stress_units}]")
        axs[0, 1].set_ylabel(f"q [{stress_units}]")

        if legend:
            axs[0, 1].legend()

        # Make the \epislon_{v} vs \epsilon_{a} plot
        axs[1, 0].plot(axial_strain, vol_strain, label = labels[2],**kwargs)
        
        # Format the plot
        axs[1, 0].set_title(r"$\epsilon_{v}$ vs. $\epsilon_{a}$")
        axs[1, 0].set_xlabel(r"$\epsilon_{a}$" +  f"[{strain_units}]")
        axs[1, 0].set_ylabel(r"$\epsilon_{v}$" +  f"[{strain_units}]")

        if legend:
            axs[1, 0].legend()

        # Make the \episilon_{v} vs. p plot
        axs[1, 1].plot(mean_stress, vol_strain, label = labels[3], **kwargs)

        # Format the plots
        axs[1, 1].set_title(r"$\epsilon_{v}$ vs. p")
        axs[1, 1].set_xlabel(f"p [{stress_units}]")
        axs[1, 1].set_ylabel(r"$\epsilon_{v}$" +  f"[{strain_units}]")

        if legend:
            axs[1, 1].legend()

        # Help make the plots not overlap
        plt.tight_layout()


if __name__ == "__main__":
    # Example usage
    par_file = ParFile("path/to/file.PAR_")
    par_file.load_data()
    print("Header:", par_file.get_header())
    print("Data:\n", par_file.get_data())
