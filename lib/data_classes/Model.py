import os

from lib.benchmark_info.run_benchmarks_info import benchmark_info_dict
from lib.general_functions.general_functions import get_highest_file,  delete_files_with_extensions
from lib.general_functions.general_functions import overwrite_line_after_string
from lib.general_functions.executing_runs import generate_batch_script, run_batch_script
# Import information about the benchmarks

class model:
    # Purpose to hold information about a model

    def __init__(self, exe_path, model_folder, model_name, benchmark = True, benchmark_name = None ):
        # Init the information about the model
        self.exe_path = exe_path
        self.model_folder = model_folder
        self.model_name = model_name
        self.model_path = os.path.join(model_folder, model_name)
        self.benchmark = benchmark
        self.benchmark_name = benchmark_name

        # Save the name of the benchmark
        self.model_name = model_name

        # Init a variable to store the stage that has been run
        self.current_stage = 0

        if self.benchmark:
            # Get the information about the bench mark
            self.load_benchmark_info()

    def __str__(self):
        return f"Model Name: {self.model_name} \nModel Path: {self.model_path} \nExecutable Path: {self.exe_path}"
    
    def load_benchmark_info(self):
        # Purpose: Load information about a benchmark
        model_info = benchmark_info_dict[self.benchmark_name]

        # Store the number of stages
        self.num_stages = int(model_info["num_stages"])      
        
        # Store the benchmark info in case needed in the future
        self.benchmark_info = model_info



    def modify_CPS(self, from_user_file = False, which_file = "last"):
        # Purpose: Modify the cps file can be used to do the next stage of a model
        
        if from_user_file:
            raise ValueError("From an output file is not implemented")
        else:
            # The information should come from a benchmark test

            # Get the flags that should be modified 
            cps_modify_flags = self.benchmark_info["modify_cps_flags"]

            # Check if the last files should be modified
            if which_file == "last":
                last_CPS = get_highest_file(self.model_folder, ".CPS_")
                print(last_CPS)

                # Create the file dir
                cps_file_dir = os.path.join(self.model_folder, last_CPS)

                # Loop over the flags that need to be modfied and modify them
                for flag, new_value in cps_modify_flags.items():
                    overwrite_line_after_string(cps_file_dir, flag, new_value)
            print(f"Modified {cps_file_dir}")

    def generate_batch_file(self, batch_file_name = "calculate.bat", batch_file_folder = None):
        "Generates the batch file to run the model using the input properties to the model"
        
        # generate the batch script 
        generate_batch_script(self.model_folder, self.exe_path, self.model_name, batch_file_name=batch_file_name, 
                              include_cd=False, batch_file_folder = batch_file_folder)
        
        if batch_file_folder is None: 
            # If no batch file folder is passed the batch file is in the model folder
            # make that path and store it
            self.batch_script_path = os.path.join(self.model_folder, batch_file_name)

        elif isinstance(batch_file_folder, str):
            # If a folder is passed for the batch script make the path to that location 
            # and store it
            self.batch_script_path = os.path.join(batch_file_folder, batch_file_name)

    def run_stage(self, print_output):
        # Purpose: Run a stage of the model 
        # run_executable(self.exe_path, self.model_path)

        # Run the batch file
        run_batch_script(self.batch_script_path, flag_print_Blog=print_output)

    def run_benchmark(self, print_output = True):
        # Purpose: Run a benchmark in one go

        while self.current_stage <= self.num_stages-1:
            # Run the first stage
            self.run_stage(print_output)
            print("----------------------------------------")
            if self.num_stages >= 2 and self.current_stage != self.num_stages -1:
                # Modify the CPS file
                self.modify_CPS()

            # Increment the current stage
            self.current_stage += 1
                # # Run the second stage
                # self.run_stage()
        # elif self.num_stages > 2:
        #     raise ValueError("running more than two stages is not implemented")
         
    def delete_folder_files(self, keep_extensions = ['.CPS_001', '.GOM', '.dll', '.out', '.exe', '.bat']):
        # Purpose: Delete all files in a folder except those with a certain extentension
        delete_files_with_extensions(self.model_folder, keep_extensions)
            

