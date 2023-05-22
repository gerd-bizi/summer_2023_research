import os
import argparse
import GEOparse

def geo_file_renamer(directory):
    for filename in os.listdir(directory):
        if filename.startswith('.DS'):
            continue
        
        access_id = filename[:10]
        gse = GEOparse.get_GEO(geo=access_id, destdir=directory)
        
        if gse is not None:
            sample_title = gse.metadata['title'][0]
            new_filename = f"{sample_title}.txt".replace(" ", "_")[:-4] + "_" + access_id
            old_filepath = os.path.join(directory, filename)
            new_filepath = os.path.join(directory, new_filename + ".txt")

            os.rename(old_filepath, new_filepath) 
            print(f"Renamed {filename} to {new_filename}")
        else:
            print(f"Unable to retrieve sample title for {filename}")


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
    geo_file_renamer(directory)
