from lib.data_classes.fileClass import File
from lib.general_functions.general_functions import check_ranges_overlap, sort_dict_by_range
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

    def modify_flags(self, flags_dict, end_symbol = "$$"):
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

            # Init list to hold the modified file
            modified_lines = []

            # Store all of the keys
            flag_keys = list(flags_dict.keys())
            
            # Read all of the lines
            with open(self.file_dir, "r") as file:
                lines = file.readlines()

            indices_dict = self.find_flag_start_end_index(lines, flag_keys, end_symbols=end_symbol)

            if check_ranges_overlap(indices_dict):
                # Checking if the ranges of the returned tuples overlap
                raise ValueError("Ranges can't overlap\n"
                                    f"{indices_dict}")
            
            # Reorder the indices dict based on the ranges
            indices_dict = sort_dict_by_range(indices_dict)

            ranges = list(indices_dict.values())

            for i, (flag, curr_range) in enumerate(indices_dict.items()):
                
                # Get the new values for the selected flag
                new_values = flags_dict[flag]

                if not isinstance(new_values, list):
                    new_values = [new_values]
                
                # Track how far the list should be written
                if i < len(ranges)-1:
                    next_start = ranges[i][0]
                else:
                    next_start = -1
                
                # Add the new line character to each of the new values
                modified_values = [str(value) + "\n" for value in new_values]

                if i==0:
                    modified_lines.extend(lines[:curr_range[0]+1])
                else: 
                    prev_range = ranges[i-1]
                    modified_lines.extend(lines[prev_range[1]+1:curr_range[0]+1])

                modified_lines.extend(modified_values)

                if next_start != -1:                
                    modified_lines.extend(lines[curr_range[1]:next_start])
                else:
                    modified_lines.extend(lines[curr_range[1]+1:])

            # Write the modified content back to the file
            with open(self.file_dir, "w") as file:
                file.writelines(modified_lines)
            
    def find_flag_start_end_index(self, lines, flags, end_symbols):
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

        if not isinstance(flags, list):
            flags = [flags]

        if not isinstance(end_symbols, list):
            end_symbols = [end_symbols]

        # If a single end symbol was entered but there are mutltiple flags assume at the end symbol applies to all the 
        if len(end_symbols) ==1 and len(flags) > 1:
            end_symbols = end_symbols * len(flags)
        
        # init dict to hold start and end indices
        indices_dict = {flag: (-1, -1) for flag in flags}

        for line_number, line in enumerate(lines):
            # Check if any of the flags are in the line and if the flag is in the 
            matching_index, matching_value = next(((i, flag) for i, flag in enumerate(flags) if flag in line), (None, None))

            if not matching_index is None:
                # Pop the found value from the list so that that index isn't searched for anymore
                flags.pop(matching_index)

                # Store the start index
                start_line_index = line_number
                
                # Get the end symbol
                end_symbol = end_symbols[matching_index]
                # Pop corresponding end symbol
                end_symbols.pop(matching_index)

                # Loop over the next lines and see if you can find the end symbol
                for subsequent_line_number, subsequent_line in enumerate(lines[start_line_index+1:]):
                            if end_symbol in subsequent_line:
                                # Store the indices of the matching values
                                # This will store the keys in order
                                indices_dict[matching_value] = (start_line_index, subsequent_line_number+start_line_index)

                                break
                
                if len(flags) == 0:
                    # If all the values have been popped return the dict
                    return indices_dict
                
        # If you make it here a flag wasn't found
        raise ValueError("The following flags weren't found.\n"
                         f"flag: {flags}\n",
                         f"End symbols: {end_symbols} ")
        
