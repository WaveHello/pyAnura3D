from lib.data_classes.fileClass import File
from lib.general_functions.general_functions import overwrite_line_after_string

# Inherit the file class and add on the ability to work with files that contains flags

class FlagFile(File):
    """
    A class for managing a file with flags and their values.

    This class inherits from the File class and provides functionality for 
    retrieving and modifying specific flag values within a file.

    Methods
    -------
    modify_single_value_flag(flag, new_value)
        Modifies the value associated with a given flag.
    get_flag_value(init_flag, end_symbol)
        Retrieves the value of a flag between the flag and a specified end symbol.
    """

    def __init__(self, file_dir):
        super().__init__(file_dir)

    def modify_single_value_flags(self, flags, new_values):
        """
        Modify the value of a specific flag in the file.

        Parameters
        ----------
        flag : str
            The flag to search for in the file.
        new_value : str
            The new value to overwrite after the flag.
        """
        # Check that that flags and the new values are lists
        # This will catach the catch the case when the input is a single value 
        if not isinstance(flags, list):
            flags = [flags]

        if not isinstance(new_values, list):
            new_values = [new_values]
    
        for flag, new_value in zip(flags, new_values):
            overwrite_line_after_string(self.file_dir, str(flag), str(new_value))

    def get_flag_value(self, init_flag, end_symbol = "$$"):
        """
        Retrieve the value associated with a specific flag in the file.

        This method searches for the `init_flag` in the file, then extracts the 
        value up until the `end_symbol`.

        Parameters
        ----------
        init_flag : str
            The initial flag to look for in the file.
        end_symbol : str
            The symbol that marks the end of the flag's value.

        Returns
        -------
        str
            The extracted value between the flag and the end symbol, or None if 
            the flag is not found.
        """
        # Init start index
        start_index = None
        return_lines = []

        with open(self.file_dir, 'r') as file:
            for line in file:
                if start_index is not None and not end_symbol in line:
                    return_lines.append(line.strip())
                
                elif init_flag in line:
                    start_index = line.find(init_flag) + len(init_flag)
                
                elif start_index is not None and end_symbol in line:
                    return return_lines

        return None  # Return None if the flag is not found

    def _find_flag_start_end_index(self, flag, end_symbol):
        """
        Find the line index after the line where the flag was found and the line index that 
        the end_symbol (which has to be found after the flag) is found inside of a file.

        Parameters
        ----------
        flag : str
            The flag to search for in the file.
        end_symbol : str
            The symbol that indicates the end of the flag's value.

        Returns
        -------
        tuple
            A tuple containing two integers: the line index after the flag's line and 
            the line index where the end symbol is found. Returns (-1, -1) if not found.
        """
        try:
            with open(self.file_dir, 'r') as file:
                for line_number, line in enumerate(file):
                    # Check if the line contains the flag
                    if flag in line:
                        # Flag found; get the line index after this one
                        start_line_index = line_number
                        
                        # Search for the end symbol in the subsequent lines
                        for subsequent_line_number, subsequent_line in enumerate(file, start=start_line_index):
                            if end_symbol in subsequent_line:
                                return (start_line_index, subsequent_line_number)

                        break  # Exit after searching for the end symbol

            return (-1, -1)  # Return if flag or end symbol not found

        except FileNotFoundError:
            print(f"Error: The file '{self.file_dir}' was not found.")
            return (-1, -1)
        except Exception as e:
            print(f"An error occurred: {e}")
            return (-1, -1)

    def modify_flag(self, flag, new_values, end_symbol = "$$"):
        """
        Modify the values of specific flags in the file. Supports single or multiple values after a flag.

        Parameters
        ----------
        flags : str or list of str
            The flag(s) to search for in the file.
        new_values : str, list of str, or list of list of str
            The new value(s) to overwrite after each flag. Each entry can be a single value (for single-value flags)
            or a list of values (for multi-value flags).
        """

        # Make sure the new values is a list
        if not isinstance(new_values, list):
            new_values = [new_values]

        # Init list to hold the modified file
        modified_lines = []

        # Find the the line that the flag is on and the 
        start_index, end_index = self._find_flag_start_end_index(flag, end_symbol=end_symbol)

        with open(self.file_dir, "r") as file:
            # Read all the files lines
            lines = file.readlines()
        
        # Add the new line character to each of the new values
        modified_values = [str(value) + "\n" for value in new_values]

        # Remove the lines that are between start and end index
        modified_lines.extend(lines[:start_index+1])
        
        # Insert the new values starting at the start index
        modified_lines.extend(modified_values)

        # Add the values after the end index
        modified_lines.extend(lines[end_index+1:])
        
        # Write the modified content back to the file
        with open(self.file_dir, "w") as file:
            file.writelines(modified_lines)


