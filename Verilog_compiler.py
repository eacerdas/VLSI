##################################################
#              Verilog Manager V1.0              #
#              github.com/hardcodev              #
##################################################

import argparse
import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk 

# 
def list_files_with_extension(extension, search_in_subdirs):
    count = 0
    if search_in_subdirs == 1: #Current dir and subdirs
        found_files = {}
        for root, dirs, files in os.walk(".", topdown=False):
            for file in files:
                if file.endswith(extension):
                    count = count + 1
                    file_path = os.path.join(root, file)
                    found_files[file] = file_path
        
        if count > 1:
            return found_files, count
        elif count == 1:
            single_found_file = found_files[next(iter(found_files))]
            return single_found_file, count
        elif count == 0:
            print(f"Error: No {extension} file found in {directory} directory.")
            exit()
    
    elif search_in_subdirs == 0: # only in current dir 
        found_files = {}
        for file in os.listdir('.'):
            if file.endswith(extension):
                file_path = os.path.join('.', file)
                found_files[file] = file_path
        return found_files

# Cuts the .v extension at the end of the file name
def get_file_basename(filename):
    # Get the base name of the file
    basename = os.path.basename(filename)
    return basename

# Moves a file from origin to destiny. Checks if there is another file with the same name on destiny
def copy_file(file_realpath, destiny_dir_realpath, filename):

        # Check if a file with the same name already exists in destination directory
        overwrite_flag = 0
        if os.path.isfile(os.path.join(destiny_dir_realpath, filename)):
            
            # If it exists, delete it to overwrite it
            os.remove(os.path.join(destiny_dir_realpath, filename))
            overwrite_flag = 1

        # Copy the file to the destination directory
        shutil.copy(file_realpath, destiny_dir_realpath)

        # Print success message
        if overwrite_flag == 0:
            print(f"Copied \"{filename}\" to {destiny_dir_realpath} in order to compile it. \n")
        else:
            print(f"Copied (overwritten) \"{filename}\" on {destiny_dir_realpath} in order to compile it. \n")

# Compiles the code with iverilog command
def compile_verilog_file(verilog_bin_directory_realpath_, verilog_file_name_, verilog_file_name_without_ext_):
    
    # Change to the destination directory
    os.chdir(verilog_bin_directory_realpath_)

    # Compile the Verilog code
    iverilog_command = f"iverilog.exe -o {verilog_file_name_without_ext_} {verilog_file_name_}"
    print(f"Compiling Verilog code with command: {iverilog_command}")
    if subprocess.call(iverilog_command, shell=True) != 0:
        print("Error: Failed to compile Verilog code.")
        exit()
    
    # Return to base directory
    os.chdir(base_directory_realpath)

# Simulates the verilog code with vvp command
def simulate_verilog_code_vvp(verilog_bin_directory_realpath_, verilog_file_name_without_ext_):
    
    # Change to the iverilog/bin directory
    os.chdir(verilog_bin_directory_realpath_)
    
    # Simulate the Verilog code
    vvp_command = f"vvp {verilog_file_name_without_ext_}"
    print(f"Running VVP simulation with command: {vvp_command} \n")
    if subprocess.call(vvp_command) != 0:
        print("Error: Failed to simulate Verilog code.")
        exit()

    # Return to base directory
    os.chdir(base_directory_realpath)

# Looks for a file that ends with an extension into the directory we provide. For example: ".vcd"
def find_file_with_extension(directory, extension):

    found_file = None
    for file in os.listdir(directory):
        if file.endswith(extension):
            found_file = file
            return found_file

    if found_file is None:
        print(f"Error: No {extension} file found in {directory} directory.")
        exit()

# Creates the folder for output if it does not exist. Returns the path 
def get_output_folder_realpath(destiny_dir, name_of_new_folder):
        # Creates the output folder in the base dir
        new_folder_path = os.path.join(destiny_dir, name_of_new_folder) 
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        
        return new_folder_path

# Moves the outputs (.vcd and verilog binary) to the base directory. Also removes them from the iverilog/bin dir
def move_outputs_to_base_dir(verilog_bin_directory_realpath_, verilog_file_name_without_ext_, verilog_file_name_, output_folder_realpath_, vcd_file_name_):

    # Move the output file to the base directory
    verilog_output_file_path = os.path.join(verilog_bin_directory_realpath_, verilog_file_name_without_ext_)

    if os.path.isfile(verilog_output_file_path):
        shutil.move(verilog_output_file_path, os.path.join(output_folder_realpath_, verilog_file_name_without_ext_))
    print(f"Moved   \"{verilog_file_name_without_ext_}\" to {output_folder_realpath_} successfully.")

    # Remove the verilog file from iverilog/bin directory
    verilog_temp_file_path = os.path.join(verilog_bin_directory_realpath_, verilog_file_name_)
    if os.path.isfile(verilog_temp_file_path):
        os.remove(verilog_temp_file_path)
    #print(f"Removed \"{verilog_file_name_}\" from {verilog_bin_directory_realpath_}. It is no longer needed.")
    
    # Move .vcd to to a 'output_files' directory inside the base directory
    vcd_file_path = os.path.join(verilog_bin_directory_realpath_, vcd_file_name_)
    if os.path.isfile(vcd_file_path):
        shutil.move(vcd_file_path, os.path.join(output_folder_realpath_, vcd_file_name_))
        print(f"Moved \"{vcd_file_name_}\" to {output_folder_realpath_} successfully.")
    
# Runs gtkwave using the file on base_directory/output_files
def run_gtkwave(vcd_file_current_realpath_):
        
        # Change to the gtkwave directory
        os.chdir(gtkwave_bin_directory_realpath)

        # Run gtkwave with the VCD file
        gtkwave_command = f"gtkwave.exe {vcd_file_current_realpath_}"
        print(f"\n\nRunning GTKWave with command: {gtkwave_command}")
        if subprocess.call(gtkwave_command, shell=True) != 0:
            print("Error: Failed to run GTKWave.")
            exit()

        # Print success message
        print("GTKWave was run successfully.")

# Tkinter window to select the .v file we want to compile 
class File_manager(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("400x200")
        self.master.configure(bg='#E0E0E0')
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Set up style for widgets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 14), background='#E0E0E0')

        # Set background color of main window to black
        self.master.configure(bg='black')

        # Create main frame that covers entire window
        main_frame = tk.Frame(self, bg='#F0F0F0')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create variable for file menu and set initial text to display
        self.file_menu_text = tk.StringVar()
        self.file_menu_text.set("Select file to compile")
        
        # Add observer link to watch for changes in file menu variable
        self.file_menu_text.trace("w", self.update_button_state)

        # Create dropdown menu for selecting files to compile
        self.file_menu = tk.OptionMenu(main_frame, self.file_menu_text, "")
        self.file_menu.config(width=40, padx=5, font=('Arial', 14), bg='#E0E0E0', fg='black')
        self.file_menu.pack(side="top", anchor="w", padx=10, pady=10)
        self.file_menu['menu'].config(bg='#E0E0E0', fg='black', font=('Arial', 14))
        self.file_menu['menu'].config(activebackground='#C0C0C0', activeforeground='blue')

        # Create 'Open' button for starting file compilation
        self.quit_button = ttk.Button(main_frame, text="Open", command=self.master.destroy, style='TButton')
        self.quit_button.pack(side="right", padx=10, pady=10)
        self.quit_button['state'] = 'disabled'  # Initially, 'Open' button is disabled

        # Update list of available files for file menu
        self.update_file_list()

    def update_button_state(self, *args):
        # Habilitar o deshabilitar el botón de Open según si se ha seleccionado un archivo válido
        if self.file_menu_text.get() == "Select file to compile":
            self.quit_button['state'] = 'disabled'
        else:
            self.quit_button['state'] = 'normal'

    def update_file_list(self):
        self.file_menu['menu'].delete(0, 'end')
        for root, dirs, files in os.walk("."):
            for v_file in files:
                if v_file.endswith('.v'):
                    self.file_menu['menu'].add_command(label=os.path.join(root, v_file), command=lambda v=os.path.join(root, v_file): self.set_file(v))

    def set_file(self, v_file):
        self.selected_file = v_file
        self.update_file_menu_text(v_file)

    def update_file_menu_text(self, v_file):
        self.file_menu_text.set(os.path.basename(v_file))


# Global variables
base_directory_realpath = "" # Modified in main
verilog_bin_directory_realpath = "C:/iverilog/bin"
gtkwave_bin_directory_realpath = "C:/iverilog/gtkwave/bin"

def main():
    
    _, num_verilog_files_found = list_files_with_extension(".v", search_in_subdirs = 1)
    print(f"\n\nnum_verilog_files_found: {num_verilog_files_found} \n\n")

    # Display a tkinter window if there is more than 1 .v file
    if num_verilog_files_found > 1:
        root = tk.Tk()
        root.title("Verilog file manager")
        file_selector = File_manager(root)
        root.mainloop()

        selected_verilog_file_relative_path = file_selector.selected_file
    
    elif num_verilog_files_found == 1: 
        selected_verilog_file_relative_path, _ = list_files_with_extension(".v", search_in_subdirs = 1)

    # Processing the name to use it later
    verilog_file_name = get_file_basename(selected_verilog_file_relative_path)
    verilog_file_name_without_ext = os.path.splitext(verilog_file_name)[0]

    # Get the verilog .v file's realpath
    verilog_file_realpath = os.path.abspath(selected_verilog_file_relative_path) # Get the full path to the file
    if not os.path.isfile(verilog_file_realpath):
        print(f"The file {verilog_file_realpath} does not exist.")
        exit()

    # Get the directory where the selected verilog file comes from
    global base_directory_realpath
    base_directory_realpath = os.path.dirname(verilog_file_realpath)

    # Moving the verilog file from the base dir to iverilog\bin to compile it
    copy_file(verilog_file_realpath, verilog_bin_directory_realpath, verilog_file_name)

    # Compiling and simulating the verilog code
    compile_verilog_file(verilog_bin_directory_realpath, verilog_file_name, verilog_file_name_without_ext)
    simulate_verilog_code_vvp(verilog_bin_directory_realpath, verilog_file_name_without_ext)
    
    vcd_file_name = find_file_with_extension(verilog_bin_directory_realpath, ".vcd") # Find the generated VCD file

    output_folder_realpath = get_output_folder_realpath(base_directory_realpath, "output_files")

    # Moves the outputs (.vcd and verilog binary) to the base directory. Also removes them from the iverilog/bin dir
    move_outputs_to_base_dir(verilog_bin_directory_realpath, verilog_file_name_without_ext, verilog_file_name, output_folder_realpath, vcd_file_name)
    
    # Once the vcd is moved, lets get the realpath
    vcd_file_current_realpath = os.path.abspath(os.path.join(output_folder_realpath, os.path.basename(vcd_file_name)))

    run_gtkwave(vcd_file_current_realpath)


# Ignore the lines below
if __name__ == "__main__":
    main()