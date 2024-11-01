import subprocess
import os

# def run_executable(executable_path, argument):
#     try:
#         # Run the executable with the specified argument
#         subprocess.run([executable_path, argument], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Error: {e}")
#     except FileNotFoundError:
#         print("Error: Executable not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")


def get_highest_file(directory, base_extension):
    # Get a list of files in the directory
    files = os.listdir(directory)
    
    # Filter the files to only include those with the specified extension
    files = [file for file in files if base_extension in file]
    
    if not files:
        return None  # No matching files found

    # Extract the numeric parts of the filenames and convert them to integers
    file_numbers = [int(file.split(base_extension)[1]) for file in files]
    
    # Find the maximum number
    highest_number = max(file_numbers)
    
    highest_file_extension = f"{base_extension}{highest_number:03d}"
    # Construct the filename with the highest number
    highest_file = [file for file in files if highest_file_extension in file][0]  # Assuming the filenames are zero-padded
    
    return highest_file

def overwrite_line_after_string(filename, target_string, new_value):
    # Open the file in read mode
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Open the file in write mode to overwrite it
    with open(filename, 'w') as file:
        found_string = False
        for i, line in enumerate(lines):
            # Check if the target string is found in the current line
            if target_string in line:
                found_string = True
                # Write the string unchanged
                file.write(line)
            # If the target string was found in the previous line, overwrite the current line
            elif found_string:
                file.write(new_value + '\n')
                found_string = False
            # Otherwise, write the current line unchanged
            else:
                file.write(line)

def delete_files_with_extensions(directory, keep_extensions):
    try:
        # List all files in the directory
        files = os.listdir(directory)
        
        # Filter out the files with extensions you want to keep
        files_to_keep = [file for file in files if any(file.endswith(ext) for ext in keep_extensions)]
        
        # Delete the files that don't have the specified extensions
        for file in files:
            if not file in files_to_keep:
                os.remove(os.path.join(directory, file))
        
        print("Files deleted successfully.")
    except Exception as e:
        print("An error occurred:", e)


def check_ranges_overlap(d):
    """
    Check if any of the ranges in the dictionary overlap.
    
    Parameters
    ----------
    d : dict
        A dictionary where values are tuples representing ranges (start, end).

    Returns
    -------
    bool
        True if there is any overlap between the ranges, False otherwise.
    """
    # Extract the ranges from the dictionary
    ranges = list(d.values())
    
    # Sort ranges by their start values to simplify overlap checking
    ranges.sort(key=lambda x: x[0])

    # Check each range against the next one in the sorted list
    for i in range(1, len(ranges)):
        prev_end = ranges[i - 1][1]
        current_start = ranges[i][0]
        
        # If the end of the previous range is greater than the start of the current range, they overlap
        if prev_end > current_start:
            return True  # Overlap found

    return False  # No overlap found

def sort_dict_by_range(d):
    """
    Sort a dictionary where keys are exclusive ranges represented as tuples.

    Parameters
    ----------
    d : dict
        A dictionary with tuple keys representing ranges (start, end).

    Returns
    -------
    dict
        A new dictionary sorted by the starting values of the range keys.
    """
    # Sort the items in the dictionary by the start of the range (the first element in each tuple key)
    sorted_items = sorted(d.items(), key=lambda item: item[1][0])

    
    # Create a new dictionary to maintain the sorted order
    sorted_dict = dict(sorted_items)
    return sorted_dict

def pad_integer_to_string(integer, pad_char, max_str_length):
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

def create_folder_if_not_exists(folder_path):
    os.makedirs(folder_path, exist_ok=True)