import os
import subprocess
from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt

def run_simulation(case_dir):
    os.chdir(case_dir)
    subprocess.call(["bash", "./Allrun"])  # Explicitly use bash to run the script
    os.chdir("..")

def extract_lift_drag(case_dir):
    file_path = os.path.join(case_dir, "postProcessing", "forceCoeffs1", "0", "coefficient.dat")
    if not os.path.exists(file_path):
        print("File not found:", file_path)
        return None, None, None

    # Read the data from coefficient.dat file
    data = np.loadtxt(file_path, comments='#', dtype=float)

    # Extracting time, lift, and drag columns from the data
    time = data[:, 0]
    lift = data[:, 4]
    drag = data[:, 1]

    # Extracting data points at every 1 time step until 500
    indices = np.arange(0, 500, 1)
    time_selected = time[indices]
    lift_selected = lift[indices]
    drag_selected = drag[indices]

    return time_selected, lift_selected, drag_selected

def plot_lift_drag(time, lift, drag, case_name):
    plt.plot(time, lift, label='Lift')
    plt.plot(time, drag, label='Drag')
    plt.xlabel('Time')
    plt.ylabel('Coefficient')
    plt.title(f'Lift and Drag Coefficients for {case_name}')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(case_name, f'lift_drag_plot_{case_name}.png'))  # Save plot
    plt.close()

if __name__ == "__main__":
    # Get the current directory where the Python script is located
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # List of case directories
    case_directories = ["fullF1", "noFWF1", "noFWRWF1", "noRWF1"]

    # Full paths to the case directories
    case_paths = [os.path.join(current_directory, case) for case in case_directories]

    # Create a pool of processes to run simulations simultaneously
    with Pool(processes=len(case_paths)) as pool:
        pool.map(run_simulation, case_paths)

    # Extract and plot lift/drag coefficients for each case
    for case in case_directories:
        case_dir = os.path.join(current_directory, case)
        time, lift, drag = extract_lift_drag(case_dir)
        if time is not None:
            plot_lift_drag(time, lift, drag, case)
