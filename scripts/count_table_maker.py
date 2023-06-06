import os
import argparse
import pandas as pd
import math

def _dir_flatten(filedir, curr_files):
    '''
    Given a directory, recursively find the csv files, and add them to a list.
    Once no directories are found, return the list of csv files.
    '''
    #First, we must get all file names in the directory
    files = os.listdir(filedir)
    #Now, we must check to see if the file is a csv file, and if it is a directory, call another function to access the csv files
    for file in files:
        if file.endswith(".csv"):
            curr_files.append(os.path.join(filedir, file))
        elif os.path.isdir(os.path.join(filedir, file)):
            _dir_flatten(os.path.join(filedir, file), curr_files)
    return curr_files


def file_getter(filedir):
    '''
    Given a directory, recursively access the csv representing the TPM values for each gene
    and create a master table of the counts for each gene for each condition (ie. sample, day, etc.)
    '''
    #First, we must get all file names in the directory
    files = os.listdir(filedir)
    #Now, we must check to see if the file is a csv file, and if it is a directory, call another function to access the csv files
    curr_files = []
    for file in files:
        if file.endswith(".csv"):
            curr_files.append(os.path.join(filedir, file))
        elif os.path.isdir(os.path.join(filedir, file)):
            curr_files += _dir_flatten(os.path.join(filedir, file), curr_files)
    return curr_files

def count_table_maker(filedirs):
    '''
    Given a directory with RNA-seq data, specifically including TPM values, create a table of the counts
    for each gene for each condition (ie. sample, day, etc.)
    '''
    #First, we must get all file names in the directory
    files = []
    for filedir in filedirs:
        files += file_getter(filedir)
    print(len(files))
    #Now, we must read in the csv files and create a master table of the counts for each gene for each condition (ie. sample, day, etc.)
    master_table = {}
    for i, file in enumerate(files):
        print(file)
        df = pd.read_csv(file, delimiter='\t')
        #get number of entries in the dataframe
        num_entries = len(df['gene_id'])
        for j in range(num_entries):
            gene_id = df['gene_id'][j]
            if gene_id not in master_table:
                master_table[gene_id] = [gene_id] + [0] * len(files)
            #get the TPM values for each day
            tpm_value = df['TPM'][j]
            master_table[gene_id][i + 1] = tpm_value
    #Now, we must write the master table to a csv file
    df_master_table = pd.DataFrame.from_dict(master_table, orient='index')
    #create new column headings
    column_headings = ['gene_id']
    for i, file in enumerate(files):
        column_headings.append(file.split('/')[-1].replace(".csv", ""))
    df_master_table.columns = column_headings
    #write to csv
    df_master_table.to_csv(os.path.join(filedir, "master_table.csv"), index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--directories",
        action="store",
        nargs="+",
        required=True,
        help="The directory containing the files to combine"
    )
    args = parser.parse_args()
    filedirs = args.directories
    count_table_maker(filedirs)
