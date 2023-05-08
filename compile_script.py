import argparse
import os
import shutil
import subprocess

# Set the original directory
original_directory = os.getcwd()

# Set the bin directory
verilog_bin_directory = "C:/iverilog/bin"

# Set the gtkwave directory
gtkwave_bin_directory = "C:/iverilog/gtkwave/bin"


##### MOVING .v TO iverilog\bin #####

# Parse command line arguments
parser = argparse.ArgumentParser(description="Copy a verilog file to the iverilog bin directory.")
parser.add_argument("filename", help="name of the file to copy")
args = parser.parse_args()

# Get the full path to the file
file_path = os.path.abspath(args.filename)

# Check if file exists
if not os.path.isfile(file_path):
    print(f"The file {file_path} does not exist.")
    exit()

os.system('cls' if os.name == 'nt' else 'clear')

# Check if file already exists in destination directory
overwrite_flag = 0
if os.path.isfile(os.path.join(verilog_bin_directory, args.filename)):
    # If it exists, delete it first to overwrite it
    os.remove(os.path.join(verilog_bin_directory, args.filename))
    overwrite_flag = 1

# Copy the file to the destination directory
shutil.copy(file_path, verilog_bin_directory)

# Print success message
if overwrite_flag == 0:
    print(f"Copied \"{args.filename}\" to {verilog_bin_directory} in order to compile it. \n")
else:
    print(f"Copied (overwritten) \"{args.filename}\" on {verilog_bin_directory} in order to compile it. \n")


##### COMPILING VERILOG #####

# Change to the destination directory
os.chdir(verilog_bin_directory)

# Eliminates de .v extension to the name to use it as output name
filename_without_ext = os.path.splitext(args.filename)[0]

# Compile the Verilog code
iverilog_command = f"iverilog.exe -o {filename_without_ext} {args.filename}"
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

# Move the output file to the original directory and remove the files from the destination directory
output_file_path = os.path.join(verilog_bin_directory, filename_without_ext)
if os.path.isfile(output_file_path):
    shutil.move(output_file_path, os.path.join(original_directory, filename_without_ext))
print(f"Moved   \"{filename_without_ext}\" from bin to {os.path.join(original_directory)} successfully.")

output_file_path = os.path.join(verilog_bin_directory, filename_without_ext)
if os.path.isfile(output_file_path):
    os.remove(output_file_path)

file_path = os.path.join(verilog_bin_directory, args.filename)
if os.path.isfile(file_path):
    os.remove(file_path)
print(f"Removed \"{args.filename}\" from {verilog_bin_directory}. It is no longer needed.")

# Find the generated VCD file
vcd_file = None
for file in os.listdir(verilog_bin_directory):
    if file.endswith(".vcd"):
        vcd_file = os.path.join(verilog_bin_directory, file)
        break

if vcd_file is None:
    print(f"Error: No VCD file found in {verilog_bin_directory} directory.")
    exit()

# Moving the VCD file to the original directory
shutil.copy(vcd_file, original_directory)
os.remove(vcd_file)

# Print success message
print(f"Moved   \"{os.path.basename(vcd_file)}\" to {original_directory} successfully.")


##### RUNNING GTKWAVE #####

# Change to the gtkwave directory
os.chdir(gtkwave_bin_directory)

# Run gtkwave with the VCD file
vcd_abs_path = os.path.abspath(os.path.join(original_directory, os.path.basename(vcd_file)))
gtkwave_command = f"gtkwave.exe {vcd_abs_path}"
print(f"\n\nRunning GTKWave with command: {gtkwave_command}")
if subprocess.call(gtkwave_command, shell=True) != 0:
    print("Error: Failed to run GTKWave.")
    exit()

# Print success message
print("GTKWave was run successfully.")
