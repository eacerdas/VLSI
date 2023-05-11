import argparse
import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk 


def count_files():
    count = 0
    for root, dirs, files in os.walk(".", topdown=False):
        for file in files:
            if file.endswith(".v"):
                count += 1
    return count

def get_verilog_file():
    verilog_file = None
    count = 0
    for root, dirs, files in os.walk(".", topdown=False):
        for file in files:
            if file.endswith(".v"):
                count += 1
                if verilog_file is None:
                    verilog_file = file
                else:
                    verilog_file = None  # hay más de un archivo .v, no devolvemos nada
                    break
        if verilog_file is None and count > 1:
            break  # hay más de un archivo .v, no seguimos buscando
    return verilog_file

def process_filename(filename):
    # Obtener el nombre base del archivo
    basename = os.path.basename(filename)
    
    # Verificar si el nombre ya está recortado
    if basename.endswith('.v'):
        return basename
    else:
        # Recortar el nombre y retornar
        return basename.split('\\')[-1]

class FileSelector(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')

        self.file_label = tk.Label(self, text="Select the file you want to compile:")
        self.file_label.pack(side="left")

        self.file_menu = tk.OptionMenu(self, tk.StringVar(), "")
        self.file_menu.config(width=40, padx=5)
        self.file_menu.pack(side="left")

        self.file_menu['menu'].config(bg='#E0E0E0', fg='black')
        self.file_menu['menu'].config(activebackground='#0078D7', activeforeground='white')

        self.quit_button = ttk.Button(self, text="Open", command=self.master.destroy)
        self.quit_button.pack(side="right")

        self.update_file_list()

    def update_file_list(self):
        self.file_menu['menu'].delete(0, 'end')
        for root, dirs, files in os.walk("."):
            for v_file in files:
                if v_file.endswith('.v'):
                    self.file_menu['menu'].add_command(label=os.path.join(root, v_file), command=lambda v=os.path.join(root, v_file): self.set_file(v))

    def set_file(self, v_file):
        self.file_menu['text'] = v_file
        self.selected_file = v_file


# Parse command line arguments
#parser = argparse.ArgumentParser(description="Compiles verilog")
#parser.add_argument("filename", help="name of the file to copy")
#args = parser.parse_args()

num_verilog_files = count_files()


print("DEBUG: Número de archivos .v en la carpeta actual y subdirectorios:", count_files())

# Display a tkinter window if there is more than 1 .v file
if num_verilog_files > 1:
    root = tk.Tk()
    root.title("Verilog file manager")
    file_selector = FileSelector(root)
    root.mainloop()

    verilog_file_ubication = file_selector.selected_file
    print(f"The selected file is: {verilog_file_ubication}")
else: 
    #verilog_file_ubication = args.filename
    verilog_file_ubication = get_verilog_file()

verilog_file_name = process_filename(verilog_file_ubication)

# Set the original directory
original_directory = os.getcwd()

# Set the bin directory
verilog_bin_directory = "C:/iverilog/bin"

# Set the gtkwave directory
gtkwave_bin_directory = "C:/iverilog/gtkwave/bin"


##### MOVING .v TO iverilog\bin #####

# Get the full path to the file
file_path = os.path.abspath(verilog_file_ubication)

# Check if file exists
if not os.path.isfile(file_path):
    print(f"The file {file_path} does not exist.")
    exit()

#os.system('cls' if os.name == 'nt' else 'clear') # not gonna use this for now

# Check if file already exists in destination directory
overwrite_flag = 0
if os.path.isfile(os.path.join(verilog_bin_directory, verilog_file_name)):
    # If it exists, delete it first to overwrite it
    os.remove(os.path.join(verilog_bin_directory, verilog_file_name))
    overwrite_flag = 1

# Copy the file to the destination directory
shutil.copy(file_path, verilog_bin_directory)

# Print success message
if overwrite_flag == 0:
    print(f"Copied \"{verilog_file_name}\" to {verilog_bin_directory} in order to compile it. \n")
else:
    print(f"Copied (overwritten) \"{verilog_file_name}\" on {verilog_bin_directory} in order to compile it. \n")


##### COMPILING VERILOG #####

# Change to the destination directory
os.chdir(verilog_bin_directory)

# Eliminates de .v extension to the name to use it as output name
filename_without_ext = os.path.splitext(verilog_file_name)[0]

# Compile the Verilog code
iverilog_command = f"iverilog.exe -o {filename_without_ext} {verilog_file_name}"
print(f"Compiling Verilog code with command: {iverilog_command}")
if subprocess.call(iverilog_command, shell=True) != 0:
    print("Error: Failed to compile Verilog code.")
    exit()


##### VVP #####

# Simulate the Verilog code
vvp_command = f"vvp {filename_without_ext}"
print(f"Running VVP simulation with command: {vvp_command} \n")
if subprocess.call(vvp_command, shell=True) != 0:
    print("Error: Failed to simulate Verilog code.")
    exit()


##### MOVING AND REMOVING FILES #####

# Move the output file to a 'bin' directory inside the original directory and remove the files from the destination directory
bin_dir_path = os.path.join(original_directory, "bin")
if not os.path.exists(bin_dir_path):
    os.makedirs(bin_dir_path)
output_file_path = os.path.join(verilog_bin_directory, filename_without_ext)
if os.path.isfile(output_file_path):
    shutil.move(output_file_path, os.path.join(bin_dir_path, filename_without_ext))
print(f"Moved   \"{filename_without_ext}\" to {os.path.join(bin_dir_path)} successfully.")

output_file_path = os.path.join(verilog_bin_directory, filename_without_ext)
if os.path.isfile(output_file_path):
    os.remove(output_file_path)

file_path = os.path.join(verilog_bin_directory, verilog_file_name)
if os.path.isfile(file_path):
    os.remove(file_path)
print(f"Removed \"{verilog_file_name}\" from {verilog_bin_directory}. It is no longer needed.")

# Find the generated VCD file
vcd_file = None
for file in os.listdir(verilog_bin_directory):
    if file.endswith(".vcd"):
        vcd_file = file
        break

if vcd_file is None:
    print(f"Error: No VCD file found in {verilog_bin_directory} directory.")
    exit()

# Move .vcd to to a 'bin' directory inside the original directory
vcd_file_path = os.path.join(verilog_bin_directory, vcd_file)
if os.path.isfile(vcd_file_path):
    shutil.move(vcd_file_path, os.path.join(original_directory, "bin", os.path.basename(vcd_file)))
    print(f"Moved \"{vcd_file}\" to {os.path.join(original_directory, 'bin')} successfully.")

##### RUNNING GTKWAVE #####

# Change to the gtkwave directory
os.chdir(gtkwave_bin_directory)

# Run gtkwave with the VCD file
vcd_abs_path = os.path.abspath(os.path.join(bin_dir_path, os.path.basename(vcd_file)))
gtkwave_command = f"gtkwave.exe {vcd_abs_path}"
print(f"\n\nRunning GTKWave with command: {gtkwave_command}")
if subprocess.call(gtkwave_command, shell=True) != 0:
    print("Error: Failed to run GTKWave.")
    exit()

# Print success message
print("GTKWave was run successfully.")
