import os

if __name__ == "__main__":
    # List of case directories
    case_directories = ["fullF1", "noFWF1", "noFWRWF1", "noRWF1"]

    # Loop through each case directory and run the Allclean script
    for case_dir in case_directories:
        os.chdir(case_dir)
        os.system("./Allclean")
        os.chdir("..")
