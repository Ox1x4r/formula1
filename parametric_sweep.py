import os
import subprocess
from multiprocessing import Pool

def run_simulation(case_dir):
    os.chdir(case_dir)
    subprocess.call(["bash", "./Allrun"])  # Explicitly use bash to run the script
    os.chdir("..")

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
