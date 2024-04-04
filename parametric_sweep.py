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
        return None, None, None, None

    # Read the data from coefficient.dat file
    data = np.loadtxt(file_path, comments='#', dtype=float)

    # Extracting time, lift, drag, and moment columns from the data
    time = data[:, 0]
    lift_coef = data[:, 4]
    drag_coef = data[:, 1]
    pitch_moment = data[:, 7]  # CmPitch

    # Extracting data points at every 1 time step until 500
    indices = np.arange(0, 500, 1)
    time_selected = time[indices]
    lift_selected = lift_coef[indices]
    drag_selected = drag_coef[indices]
    moment_selected = pitch_moment[indices]

    # Extracting air density, velocity, and reference area
    with open(file_path, 'r') as file:
        lines = file.readlines()
    air_density = float(lines[7].split(':')[1].split()[0])
    velocity_line = [line for line in lines if 'magUInf' in line][0]
    velocity = float(velocity_line.split(':')[1].split()[0])
    reference_area = float(lines[8].split(':')[1].split()[0])

    # Convert coefficients to forces and moments
    lift_force = 0.5 * air_density * velocity**2 * reference_area * lift_selected
    drag_force = 0.5 * air_density * velocity**2 * reference_area * drag_selected
    pitch_moment_force = 0.5 * air_density * velocity**2 * reference_area * moment_selected

    return time_selected, lift_force, drag_force, pitch_moment_force

def plot_lift_drag(time, lift, drag, moment, case_name):
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Force (N)', color=color)
    ax1.plot(time, lift, label='Lift Force', color=color)
    ax1.plot(time, drag, label='Drag Force', linestyle='--', color='tab:green')  # Green color for drag force
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Moment (Nm)', color=color)  
    ax2.plot(time, moment, label='Pitch Moment', color='tab:orange')  # Orange color for pitch moment
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Lift, Drag, and Pitch Moment Forces for {case_name}')
    fig.tight_layout()  
    plt.grid(True)
    plt.savefig(os.path.join(case_name, f'lift_drag_moment_plot_{case_name}.png'))  # Save plot
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
        time, lift, drag, moment = extract_lift_drag(case_dir)
        if time is not None:
            plot_lift_drag(time, lift, drag, moment, case)
