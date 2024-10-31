from lib.general_functions.general_functions import get_highest_file, overwrite_line_after_string, delete_files_with_extensions
from lib.general_functions.executing_runs import generate_batch_script
from lib.benchmark_info.run_benchmarks_info import benchmark_info_dict # Dictionary that contains information about the benchmarks.
                                                                       # This should be converted into a JSON file that's loaded in
from lib.data_classes.cpsClass import CPSFile

import os
import glob

class ModelSetup:

    def __init__(self, model_folder_path, exe_path, model_name, benchmark, benchmark_name):
        self.exe_path          = exe_path   # Name of the model
        self.model_folder_path = model_folder_path # Path that all of the model files are contained in
        self.model_name        = model_name
        self.model_path        = os.path.join(model_folder_path, model_name)
        self.benchmark         = benchmark
        self.benchmark_name    = benchmark_name

        if self.benchmark:
            # Get the information about the benchmark
            self._load_benchmark_info()

    def __str__(self):
        """
        prints information about the object when the object is inserted
        into a print statement
        """

        return_string = (
                         f"Model Name: {self.model_name}\n"
                         f"Folder path: {self.model_folder_path}\n"
                         f"Exe path: {self.exe_path}\n"
                         )
        
        return return_string
    def _get_benchmark_info(self):
        
        # Print the benchmark info
        print("Avaliable AutoRun benchmarks are:")
        for name in benchmark_info_dict.keys():
            print(name)

    def _load_benchmark_info(self):
        # Purpose: Load information about a benchmark
        benchmark_name = self.benchmark_name

        if benchmark_name in benchmark_info_dict:
            model_info = benchmark_info_dict[self.benchmark_name]
        else:
            self._get_benchmark_info()
            raise KeyError(f"{benchmark_name} is not a valid key")
        
        # Store the number of stages
        self.num_stages = int(model_info["num_stages"])      
        
        # Store the benchmark info in case needed in the future
        self.benchmark_info = model_info

    def modify_CPS(self, modify_dict, which_file = "last"):
        """
        Purpose: Modify the cps file can be used to do the next stage of a model
        """

        # Returns a list so get the first element in the list
        cps_file_obj = self.get_CPS_file(which_file=which_file)[0]
        
        cps_file_obj.modify_single_value_flags(modify_dict.keys(), modify_dict.values())
        
        print(f"Modified {cps_file_obj.get_file_name()}")

    def generate_batch_file(self, batch_file_name = "calculate.bat", batch_file_folder = None):
        "Generates the batch file to run the model using the input properties to the model"
        
        print(self.model_folder_path)
        print(self.exe_path)
        print(self.model_path)
        
        # generate the batch script 
        generate_batch_script(self.model_folder_path, self.exe_path, self.model_path, batch_file_name=batch_file_name, 
                              include_cd=False, batch_file_folder = batch_file_folder)
        
        if batch_file_folder is None: 
            # If no batch file folder is passed the batch file is in the model folder
            # make that path and store it
            self.batch_script_path = os.path.join(self.model_folder_path, batch_file_name)

        elif isinstance(batch_file_folder, str):
            # If a folder is passed for the batch script make the path to that location 
            # and store it
            self.batch_script_path = os.path.join(batch_file_folder, batch_file_name)

    def delete_folder_files(self, keep_extensions = ['.CPS_001', '.GOM', '.dll', '.out', '.exe', '.bat']):
        # Purpose: Delete all files in a folder except those with a certain extentension
        delete_files_with_extensions(self.model_folder_path, keep_extensions)

    def get_CPS_file(self, which_file = "all"):
        # Load all of the CPS files
        
        file_extension = ".CPS_"
        cps_file_objs = []
        cps_file_paths = [] # List to store all of the CPS file paths

        if which_file == "all":
            # Get all of the CPS files
            raise NotImplementedError("Get all of the CPS files isn't implemented")
        
            # Make the file paths
        elif which_file == "first":
            first_cps_file_id = 1

            # Get the id of the CPS file
            cps_id = self._pad_integer_to_string(first_cps_file_id, pad_char="0", max_str_length=3)
            
            # Construct the cps file name
            file_name = self._make_id_file_name(self.model_name, file_extension, cps_id)
            
            # Append the path to the file paths list
            cps_file_paths.append(self._make_file_path(file_name))

            # Make the file path
        elif which_file == "last":
            # Get the last CPS file
            file_name = get_highest_file(self.model_folder_path, file_extension)
            
            cps_file_paths.append(self._make_file_path(file_name))

        elif isinstance(which_file, int):
            # Get the id of the CPS file
            cps_id = self._pad_integer_to_string(which_file, pad_char="0", max_str_length=3)
            
            # Construct the cps file name
            file_name = self._make_id_file_name(self.model_name, file_extension, cps_id)
            
            cps_file_paths.append(self._make_file_path(file_name))

        else: 
            raise ValueError("Only first, last, and file id is currently implemented")

        for path in cps_file_paths:
            print(path)
            # Make the object
            obj = CPSFile(path)

            # Append the object to the path
            cps_file_objs.append(obj)

        return cps_file_objs
    
    @staticmethod
    def _pad_integer_to_string(integer, pad_char, max_str_length):
        """
        Returns an integer inset into a string with length max_str_length that is padded with the pad
        character
        """

        integer_str = str(integer)

        if len(integer_str) > max_str_length:
            raise ValueError("The length of the integer is too long.\n"
                             f"Integer length: {len(integer_str)}\n"
                             f"Max string length: {max_str_length}")
        
        padded_integer = integer_str.rjust(max_str_length, pad_char)

        return padded_integer
    
    def _make_file_path(self, file_name, folder_path = None):
        "Returns a file name that is assumed to be inside of the model folder"
        if folder_path is None:
            # Assume that it's the model folder path
            file_path = os.path.join(self.model_folder_path, file_name)
        else:
            file_path = os.path.join(folder_path, file_name)

        return file_path
    
    @staticmethod
    def _make_id_file_name(base_file_name, file_extension, file_id):
        """
        Makes the file name for a CPS file
        """

        return base_file_name + file_extension + file_id
