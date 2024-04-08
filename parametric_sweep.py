import os
import subprocess
from multiprocessing import Pool
import numpy as np
import matplotlib.pyplot as plt

class SimulationRunner:
    def __init__(self, case_directories):
        self.case_directories = case_directories

    def run(self):
        with Pool(processes=len(self.case_directories)) as pool:
            pool.map(self._run_simulation, self.case_directories)

    @staticmethod
    def _run_simulation(case_dir):
        os.chdir(case_dir)
        subprocess.call(["bash", "./Allrun"])  # Explicitly use bash to run the script
        os.chdir("..")

class DataExtractor:
    @staticmethod
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

    @staticmethod
    def calculate_downforce_and_efficiency(lift, drag):
        downforce = -lift  # Negative lift represents downforce
        efficiency = lift / drag
        return downforce, efficiency

class GraphPlotter:
    @staticmethod
    def plot_lift_drag_moment(time, lift, drag, moment, case_name):
        fig, ax = plt.subplots(figsize=(6, 5))

        ax.set_xlabel('Time')
        ax.set_ylabel('Force (N)')

        # Plot lift force with blue color
        ax.plot(time, lift, label='Lift Force', color='blue')

        # Plot drag force with red color
        ax.plot(time, drag, label='Drag Force', color='red')

        # Plot moment with green dotted line
        ax.plot(time, moment, label='Pitch Moment', linestyle='--', color='green')

        ax.set_title(f'Lift, Drag, and Pitch Moment Forces for {case_name}')
        ax.legend(loc='lower right')  # Change legend position

        plt.grid(True)
        plt.savefig(os.path.join(case_name, f'lift_drag_moment_plot_{case_name}.png'))  # Save plot
        plt.close()

    @staticmethod
    def plot_downforce_efficiency(time, downforce, efficiency, case_name):
        fig, ax = plt.subplots(figsize=(6, 5))

        ax.set_xlabel('Time')
        ax.set_ylabel('Force (N)')

        # Plot downforce with orange color
        ax.plot(time, downforce, label='Downforce', color='orange')

        # Plot efficiency with purple color
        ax.plot(time, efficiency, label='Aerodynamic Efficiency', color='purple')

        ax.set_title(f'Downforce and Aerodynamic Efficiency for {case_name}')
        ax.legend(loc='upper right')  # Keep the legend in the upper right

        plt.grid(True)
        plt.savefig(os.path.join(case_name, f'downforce_efficiency_plot_{case_name}.png'))  # Save plot
        plt.close()

if __name__ == "__main__":
    # Get the current directory where the Python script is located
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # List of case directories
    case_directories = ["fullF1", "noFWF1", "noFWRWF1", "noRWF1"]

    # Full paths to the case directories
    case_paths = [os.path.join(current_directory, case) for case in case_directories]

    # Run simulations
    simulation_runner = SimulationRunner(case_paths)
    simulation_runner.run()

    # Extract and plot lift/drag coefficients for each case
    for case in case_directories:
        case_dir = os.path.join(current_directory, case)
        time, lift, drag, moment = DataExtractor.extract_lift_drag(case_dir)
        if time is not None:
            downforce, efficiency = DataExtractor.calculate_downforce_and_efficiency(lift, drag)
            GraphPlotter.plot_lift_drag_moment(time, lift, drag, moment, case)
            GraphPlotter.plot_downforce_efficiency(time, downforce, efficiency, case)
