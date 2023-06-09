import os
import argparse
import pandas as pd
import copy

def zero_filter(count_matrix_file):
    '''
    Remove all rows that have a zero value in every column.
    '''
    df = pd.read_csv(count_matrix_file, delimiter=",")
    new_df = copy.deepcopy(df)
    #get name of gene_id column
    gene_id_column = df.columns[0]
    num_entries = len(df[gene_id_column])
    num_columns = len(df.columns)

    for i in range(num_entries):
        gene_id = df[gene_id_column][i]
        values = []
        for j in range(1, num_columns):
            values.append(df.iloc[i, j])
        if all(v == 0 for v in values):
            new_df.drop(i, inplace=True)
    new_file_name = count_matrix_file.replace(".csv", "_zero_filtered.csv")
    new_df.to_csv(new_file_name, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--countmatrix",
        action="store",
        nargs="+",
        required=True,
        help="The count matrix to be filtered"
    )
    args = parser.parse_args()
    countmatrix = args.countmatrix[0]
    zero_filter(countmatrix)
