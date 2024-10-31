# Class to represent a CPS file and get information from it
# It inherits flagFile
import os
from lib.data_classes.flagFile import FlagFile

class CPSFile(FlagFile):

    def __init__(self, file_dir):
        super().__init__(file_dir)
    
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
        Print the CPS file.
        """

        for line in self.data:
            print(line.strip())
    
    def update_output_mat_points(self, point_ids, 
                                 num_mat_points_flag = "$$OUTPUT_NUMBER_OF_MATERIAL_POINTS",
                                 mat_point_ids_flag = "$$OUTPUT_MATERIAL_POINTS"
        ):
        
        """
        Update the material points that are going to be updated
        """

        if not isinstance(point_ids, list):
            point_ids = [point_ids]

        num_material_points = len(point_ids)

        # update the number of material points
        self.modify_flag(num_mat_points_flag, num_material_points)

        # Update the output material point ids
        self.modify_flag(mat_point_ids_flag, point_ids)