import os

from lib.general_functions.executing_runs import run_batch_script
from lib.data_classes.setupClass import ModelSetup
from lib.data_classes.resultsClass import ModelResults

# Import information about the benchmarks

class AnuraModel:
    # Purpose to hold information about a model

    def __init__(self, exe_path, model_folder_path, model_name, benchmark = True, benchmark_name = None ):
        
        # Init setup object
        self.setup = ModelSetup(model_folder_path = model_folder_path, exe_path=exe_path, model_name = model_name, 
                                benchmark = benchmark, benchmark_name = benchmark_name)

        # Init results object
        self.results = ModelResults(results_folder_path=model_folder_path)

        # Init the information about the model
        self.model_folder_path = model_folder_path
        self.model_name = model_name
        self.model_path = os.path.join(model_folder_path, model_name)
        self.benchmark = benchmark
        self.benchmark_name = benchmark_name

        # Save the name of the benchmark
        self.model_name = model_name

        # Init a variable to store the stage that has been run
        self.current_stage = 0

    def __str__(self):
        return f"Model Name: {self.model_name} \nModel Path: {self.model_path} \nExecutable Path: {self.exe_path}"
    

    def run_stage(self, print_output):
        # Purpose: Run a stage of the model 
        # run_executable(self.exe_path, self.model_path)

        # Run the batch file
        run_batch_script(self.setup.batch_script_path, flag_print_Blog=print_output)

    def run_benchmark(self, print_output = True):
        # Purpose: Run a benchmark in one go

        # Store the setup object
        setup = self.setup

        while self.current_stage <= setup.num_stages-1:
            # Run the first stage
            self.run_stage(print_output)
            print("----------------------------------------")
            if setup.num_stages >= 2 and self.current_stage != setup.num_stages -1:
                # Modify the CPS file
                setup.modify_CPS(setup.benchmark_info["modify_cps_flags"], 
                                 which_file="last")

            # Increment the current stage
            self.current_stage += 1

         
            

