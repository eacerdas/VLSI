import argparse
import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk 

# Counts the number of .v files under the current directory and sub directories 
def count_files(): 
    count = 0
    for root, dirs, files in os.walk(".", topdown=False):
        for file in files:
            if file.endswith(".v"):
                count += 1
    print("DEBUG: Número de archivos .v en la carpeta actual y subdirectorios:", count)
    return count

# returns the name of the .v file that is found under the current directory and sub directories useful when there is only one
def find_verilog_file(): 
    verilog_file = None
    for root, dirs, files in os.walk(".", topdown=False):
        for file in files:
            if file.endswith(".v"):
                verilog_file = file
                break
        if verilog_file is not None:
            break
    return verilog_file

# Cuts the .v extension at the end of the file name
def get_file_basename(filename):
    # Get the base name of the file
    basename = os.path.basename(filename)
    return basename

# Moves a file from origin to destiny. Checks if there is another file with the same name on destiny
def copy_file(file_realpath, destiny_dir, filename):

        # Check if a file with the same name already exists in destination directory
        overwrite_flag = 0
        if os.path.isfile(os.path.join(destiny_dir, filename)):
            
            # If it exists, delete it to overwrite it
            os.remove(os.path.join(destiny_dir, filename))
            overwrite_flag = 1

        # Copy the file to the destination directory
        shutil.copy(file_realpath, destiny_dir)

        # Print success message
        if overwrite_flag == 0:
            print(f"Copied \"{filename}\" to {destiny_dir} in order to compile it. \n")
        else:
            print(f"Copied (overwritten) \"{filename}\" on {destiny_dir} in order to compile it. \n")

# Compiles the code with iverilog command
def compile_verilog_file(verilog_bin_directory_, verilog_file_name_, verilog_file_name_without_ext_, base_directory_):
    
    # Change to the destination directory
    os.chdir(verilog_bin_directory_)

    # Compile the Verilog code
    iverilog_command = f"iverilog.exe -o {verilog_file_name_without_ext_} {verilog_file_name_}"
    print(f"Compiling Verilog code with command: {iverilog_command}")
    if subprocess.call(iverilog_command, shell=True) != 0:
        print("Error: Failed to compile Verilog code.")
        exit()
    
    # Return to base directory
    os.chdir(base_directory_)

# Simulates the verilog code with vvp command
def simulate_verilog_code_vvp(verilog_bin_directory_, verilog_file_name_without_ext_, base_directory_):
    
    # Change to the iverilog/bin directory
    os.chdir(verilog_bin_directory_)
    
    # Simulate the Verilog code
    vvp_command = f"vvp {verilog_file_name_without_ext_}"
    print(f"Running VVP simulation with command: {vvp_command} \n")
    if subprocess.call(vvp_command) != 0:
        print("Error: Failed to simulate Verilog code.")
        exit()

    # Return to base directory
    os.chdir(base_directory_)

def find_file_with_extension(directory, extension):
    # Find the generated VCD file
    found_file = None
    for file in os.listdir(directory):
        if file.endswith(extension):
            found_file = file
            return found_file

    if found_file is None:
        print(f"Error: No {extension} file found in {directory} directory.")
        exit()

# 
def get_output_folder_path(destiny_dir, name_of_folder):
        # Creates the output folder in the base dir
        output_folder_path_ = os.path.join(destiny_dir, name_of_folder) 
        if not os.path.exists(output_folder_path_):
            os.makedirs(output_folder_path_)
        
        return output_folder_path_

# Runs gtkwave using the file on base_directory/output_files
def run_gtkwave(output_folder_path_):
        
        vcd_file_name = find_file_with_extension(output_folder_path_, ".vcd") # Find the generated VCD file
        print(f"\n\nvcd_file: {vcd_file_name} \n\n")
        # Change to the gtkwave directory
        os.chdir(gtkwave_bin_directory)

        # Run gtkwave with the VCD file
        vcd_abs_path = os.path.abspath(os.path.join(output_folder_path_, os.path.basename(vcd_file_name))) # Change "verilog_bin_directory" for "output_folder_path" if you are moving outputs to original directory
        gtkwave_command = f"gtkwave.exe {vcd_abs_path}"
        print(f"\n\nRunning GTKWave with command: {gtkwave_command}")
        if subprocess.call(gtkwave_command, shell=True) != 0:
            print("Error: Failed to run GTKWave.")
            exit()

        # Print success message
        print("GTKWave was run successfully.")

# Moves the outputs (.vcd and verilog binary) to the base directory. Also removes them from the iverilog/bin dir
def move_outputs_to_base_dir(verilog_bin_directory_, verilog_file_name_without_ext_, verilog_file_name_, output_folder_path_):

    # Move the output file to the original directory
    verilog_output_file_path = os.path.join(verilog_bin_directory_, verilog_file_name_without_ext_)

    if os.path.isfile(verilog_output_file_path):
        #shutil.move(verilog_output_file_path, os.path.join(output_folder_path_, verilog_file_name_without_ext_))
        shutil.move(verilog_output_file_path, os.path.join(output_folder_path_, verilog_file_name_without_ext_))
    print(f"Moved   \"{verilog_file_name_without_ext_}\" to {output_folder_path_} successfully.")

    # Remove the verilog file from iverilog/bin directory
    verilog_temp_file_path = os.path.join(verilog_bin_directory_, verilog_file_name_)
    if os.path.isfile(verilog_temp_file_path):
        os.remove(verilog_temp_file_path)
    #print(f"Removed \"{verilog_file_name_}\" from {verilog_bin_directory_}. It is no longer needed.")

    vcd_file_name = find_file_with_extension(verilog_bin_directory_, ".vcd") # Find the generated VCD file
    
    print(f"\n\nvcd_file: {vcd_file_name} \n\n")

    # Move .vcd to to a 'output_files' directory inside the base directory
    vcd_file_path = os.path.join(verilog_bin_directory_, vcd_file_name)
    if os.path.isfile(vcd_file_path):
        shutil.move(vcd_file_path, os.path.join(output_folder_path_, vcd_file_name))
        print(f"Moved \"{vcd_file_name}\" to {output_folder_path_} successfully.")

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
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 14))

        self.file_menu_text = tk.StringVar()
        self.file_menu_text.set("Select file to compile")
        self.file_menu = tk.OptionMenu(self, self.file_menu_text, "")
        self.file_menu.config(width=40, padx=5, font=('Arial', 14))
        self.file_menu.pack(side="top", anchor="w", padx=10, pady=10)

        self.file_menu['menu'].config(bg='#E0E0E0', fg='black', font=('Arial', 14))
        self.file_menu['menu'].config(activebackground='#0078D7', activeforeground='white')

        self.quit_button = ttk.Button(self, text="Open", command=self.master.destroy)
        self.quit_button.pack(side="right", padx=10, pady=10)

        self.update_file_list()

        # Agregamos un nuevo widget para el fondo gris
        self.bg_frame = tk.Frame(self.master, bg='#E0E0E0')
        self.bg_frame.pack(fill='both', expand=True)

        # Agregamos una nueva variable para guardar el valor del checkbox
        self.generate_output = False

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

    # Agregamos un método para obtener el valor del checkbox
    def get_generate_output(self):
        self.generate_output = self.generate_output_var.get()
        return self.generate_output

# Global variables
verilog_bin_directory = "C:/iverilog/bin"
gtkwave_bin_directory = "C:/iverilog/gtkwave/bin"

def main():

    num_verilog_files = count_files()

    # Display a tkinter window if there is more than 1 .v file
    if num_verilog_files > 1:
        root = tk.Tk()
        root.title("Verilog file manager")
        file_selector = File_manager(root)
        root.mainloop()

        selected_verilog_file_relative_path = file_selector.selected_file
        print(f"\nThe selected file is: {selected_verilog_file_relative_path}\n")
    else: 
        selected_verilog_file_relative_path = find_verilog_file()

    # Processing the name to use it later
    verilog_file_name = get_file_basename(selected_verilog_file_relative_path)

    print(f"FLAG 1")

    verilog_file_name_without_ext = os.path.splitext(verilog_file_name)[0]

    # Get the verilog .v file's realpath
    verilog_file_realpath = os.path.abspath(selected_verilog_file_relative_path) # Get the full path to the file
    if not os.path.isfile(verilog_file_realpath):
        print(f"The file {verilog_file_realpath} does not exist.")
        exit()

    # Get the directory where the verilog file comes from
    base_directory = os.path.dirname(verilog_file_realpath)

    # Moving the verilog file from the base dir to iverilog\bin to compile it
    copy_file(verilog_file_realpath, verilog_bin_directory, verilog_file_name)

    # Compiling and simulating the verilog code
    compile_verilog_file(verilog_bin_directory, verilog_file_name, verilog_file_name_without_ext, base_directory)
    simulate_verilog_code_vvp(verilog_bin_directory, verilog_file_name_without_ext, base_directory)
    
    output_folder_path = get_output_folder_path(base_directory, "output_files")

    print(f"folder path: {output_folder_path}")

    # Moves the outputs (.vcd and verilog binary) to the base directory. Also removes them from the iverilog/bin dir
    move_outputs_to_base_dir(verilog_bin_directory, verilog_file_name_without_ext, verilog_file_name, output_folder_path)
    
    run_gtkwave(output_folder_path)


# Ignore the lines below
if __name__ == "__main__":
    main()