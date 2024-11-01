import os
import copy

from lib.general_functions.executing_runs import run_batch_script
from lib.general_functions.general_functions import create_folder_if_not_exists
from lib.data_classes.setupClass import ModelSetup
from lib.data_classes.resultsClass import ModelResults
from lib.data_classes.folder import Folder
from lib.general_functions.general_functions import delete_files_with_extensions

# Import information about the benchmarks

class AnuraModel:
    # Purpose to hold information about a model

    def __init__(self, exe_path, model_folder_path, model_name, benchmark = True, benchmark_name = None ):
        
        # Construct a folder object
        self.folder = Folder(model_folder_path)

        # Init setup object
        self.setup = ModelSetup(folder = self.folder, exe_path=exe_path, model_name = model_name, 
                                benchmark = benchmark, benchmark_name = benchmark_name)

        # Init results object
        self.results = ModelResults(self.folder)

        # Init the information about the model
        self.model_name = model_name
        self.model_path = os.path.join(self.folder.folder_dir, model_name)
        self.benchmark = benchmark
        self.benchmark_name = benchmark_name

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

         
    def get_copy(self):
        """
        Make a full copy of current model. This includes all the objects that it's holding
        """

        return copy.deepcopy(self)    

    def get_new_deriv_model(self, new_model_dir, new_model_name=None, delete_files=True, overwrite_files = True):
        """
        Create a derivative model, useful for parametric analysis.
        Copies the current model's files to a new directory, optionally renames core files, 
        and returns a new model object pointing to the copied model.

        Parameters:
        - new_model_dir (str): Directory where the new model will be created.
        - new_model_name (str, optional): New name for the model. If provided, renames CPS and GOM files.
        - delete_files (bool): If True, deletes existing files in the new model directory before copying.

        Returns:
        - AnuraModel: The new model object.
        """
        # Copy all the files from the current model folder to the new model directory
        self.folder.copy_files_2_folder(new_folder_dir=new_model_dir)

        
        # Optionally delete files in the new directory
        if delete_files:
            # Clear the new folder of the all folder dat
            delete_files_with_extensions(new_model_dir, ['.CPS_001', '.GOM', '.dll', '.out', '.exe', '.bat'])

        elif not delete_files and new_model_name:
            raise NotImplementedError("Renaming files without resetting to CPS_001 and GOM is not yet supported.")

        # Create a temporary model to rename files if needed
        temp_model = AnuraModel(
            exe_path=self.setup.exe_path,
            model_folder_path=new_model_dir,
            model_name=self.model_name,
            benchmark=self.benchmark,
            benchmark_name=self.benchmark_name
        )

        # Rename CPS and GOM files if a new model name is provided
        if new_model_name:
            cps = temp_model.setup.get_CPS_file(which_file=1)[0]
            gom = temp_model.setup.get_GOM_file()
            # Get the file dir for the renamed files
            base_file_dir = os.path.join(new_model_dir, new_model_name)
            cps.new_file_name(f"{base_file_dir}.CPS_001")
            gom.new_file_name(f"{base_file_dir}.GOM")

        # Create the new model with updated information
        new_model = AnuraModel(
            exe_path=self.setup.exe_path,
            model_folder_path=new_model_dir,
            model_name=new_model_name or self.model_name,
            benchmark=self.benchmark,
            benchmark_name=self.benchmark_name
        )
        
        return new_model
