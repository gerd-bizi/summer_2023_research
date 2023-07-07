import os
import pickle
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
import pydeseq2.utils
import pandas as pd
import argparse

def zero_filter(count_matrix_file, design_file):
    '''
    Remove all rows that have a zero value in every column.
    '''
    counts_df = pd.read_csv(count_matrix_file, index_col=0, delimiter=",")

    # Transpose the count matrix

    counts_df = counts_df.transpose()

    print(counts_df)

    clinical_df = pd.read_csv(design_file, index_col=0, delimiter=",")

    print(clinical_df)

    genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
    counts_df = counts_df[genes_to_keep]

    dds = DeseqDataSet(
        counts=counts_df,
        clinical=clinical_df,
        design_factors="TimePoint",
        refit_cooks=True,
        n_cpus=None # To use all available CPUs
    )

    dds.deseq2()

    ds = DeseqStats(
        dds=dds,
        contrast=['TimePoint', '1', '0'],
        alpha=0.05,
        cooks_filter=True,
        independent_filter=True,
        n_cpus=None,
        prior_LFC_var=None
    )

    print(dds.X)

    
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--count_matrix",
        action="store",
        nargs="+",
        required=True,
        help="The count matrix to be filtered"
    )
    parser.add_argument(
        "--design_file",
        action="store",
        nargs="+",
        required=True,
        help="The design file to be used for normalization"
    )
    args = parser.parse_args()
    countmatrix = args.count_matrix[0]
    design_file = args.design_file[0]
    zero_filter(countmatrix, design_file)
