import os
import argparse

def renamer(directory):
    for filename in os.listdir(directory):
        new_filename = filename.replace(".txt", "") + ".csv"
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--directory",
        action="store",
        nargs="+",
        required=True,
        help="The directory to rename."
    )
    args = parser.parse_args()
    directory = args.directory[0]
    renamer(directory)