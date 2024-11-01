"""
Class to represent the GOM file
"""
import os

from lib.data_classes.flagFile import FlagFile
from lib.general_functions.general_functions import pad_integer_to_string, overwrite_line_after_string

class GomFile(FlagFile):

    def __init__(self, file_dir):
        super().__init__(file_dir)

    def get_model_dimension(self):
        """
        Get the dimension that the model is
        """

        flag_3D = False

        dim = self.get_flag_value("$$DIMENSION")[0]

        if "3D" in dim:
            flag_3D = True

        return (dim, flag_3D) 
    
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

    def update_ESM_material_props(self, esm_name, props_dict:dict,
                                  new_esm_name = None):
        
        """
        Update the material properties for a ESM material
        """
        # Make function for constructing the material parameters
        def construct_mat_param(int_id):
            id = pad_integer_to_string(int_id, "0", 2)
            base_name = "$$MATERIAL_PARAMETER_SOLID_" 
            
            return base_name + id
        
        def construct_prop_str(prop_dict, init_value = 
                               "$$MATERIAL_MODEL_DLL\nNone\n$$UMAT_DIMENSION\nfull_3D_(default)"):
            # For the string that will overwrite the esm properties
             
            form = init_value
            for key, value in prop_dict.items():
                form = form + f"\n{str(key)}\n{str(value)}"
            return form

        print("Warning: In update_ESM_material_props:\n"
              "This function overwrites all of the values in the ESM material\n"
              "Currently only works for setting the material parameters"
              )
        
        # Construct the param file flags
        param_file_dict = {construct_mat_param(i+1):0.0 for i in range(50)}

        #
        # Overwrite with the material properties inputted. Order is assumed to be correct
        
        # Zip automatically cuts the loop when one of the dicts end
        # In this case the props_dict should end since there usually isn't 50 props that need to be written
        for key, new_value in zip(param_file_dict, props_dict.values()):
             param_file_dict[key] = new_value

        esm_dict = {}
        esm_dict[esm_name] = construct_prop_str(param_file_dict)

        self.modify_flags(esm_dict, "$$INITIAL_STATE_VARIABLE_SOLID_01")
        
        # update the esm name if necessary
        if not new_esm_name is None:
            # Open the file
            with open(self.file_dir, 'r') as file:
                lines = file.readlines()
            
            for i, line in enumerate(lines):
                if esm_name in line:
                    lines[i] = new_esm_name +"\n"
            
            with open(self.file_dir, "w") as file:
                file.writelines(lines)

            # Find the location of the 

        # If update the material name do that

        
        

    