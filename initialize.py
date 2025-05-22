import os
import sys


def get_workdir_path():
    current_file_path = os.path.abspath(__file__)
    print("file: ", current_file_path)
    current_directory = os.path.dirname(current_file_path)
    print("working directory: ", current_directory)
    return current_directory


def main():
    # add_directory_to_path
    print("adding working directory to path variable")
    sys.path.append(get_workdir_path())
    print("new paths: \n", sys.path)


if __name__ == "__main__":
    main()

    print("initialization complete!\n If you have problems in the future, try re-running initialization.")
