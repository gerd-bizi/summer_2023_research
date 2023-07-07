import os
import argparse
import pandas as pd
import copy
import numpy as np

def tpm_normalize(count_matrix_file, directory, new_directory):
    '''
    Normalize the count matrix using TPM values.
    To do this, sum up the counts for each transcript in each sample.
    Then, divide each count by the sum of counts, and multiply by 1,000,000.
    As a result, the sum of all TPM values for each sample will be 1,000,000.
    This gives the TPM value for each transcript in each sample.
    '''
    df = pd.read_csv(count_matrix_file, delimiter=",")
    #make a new dataframe with the same columns as the original
    new_df = pd.DataFrame(columns=df.columns)
    #for each sample column, sum up the counts for each transcript
    for column in df.columns:
        if column.lower() == "gene_id":
            new_df[column] = df[column]
        else:
            sum = df[column].sum()
            scaling_factor = 1e6 / sum
            new_df[column] = df[column] * scaling_factor
    new_file_name = count_matrix_file.replace(".csv", "_tpm_normalized.csv")
    new_file_name = new_file_name.replace(directory, new_directory)
    new_df.to_csv(new_file_name, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--directory",
        action="store",
        nargs="+",
        required=True,
        help="The directory of count matrices to be filtered"
    )
    args = parser.parse_args()
    directory = args.directory[0]
    new_directory = directory + "/../" + "tpm_normalized_matrices"
    try:
        os.mkdir(new_directory)
    except FileExistsError:
        pass
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            tpm_normalize(directory + "/" + file, directory, new_directory)
