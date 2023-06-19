import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns

def correlation_heatmap(count_matrix, method):
    '''
    Given a count matrix, perform PCA analysis and plot the results.
    '''
    df = pd.read_csv(count_matrix, index_col='gene_id')

    corr = df.corr(method=method)
    correlation_matrix = df.corr()

    # Plot the heatmap
    plt.figure(figsize=(10, 8))  # Adjust the figure size as per your preference
    sns.heatmap(correlation_matrix, cmap='coolwarm')

    # Set the axis labels and title
    plt.xlabel('Gene IDs')
    plt.ylabel('Gene IDs')
    plt.title('Abundance Heatmap')

    # Show the heatmap
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--countmatrix",
        action="store",
        required=True,
        help="Count matrix for experiment."
    )
    parser.add_argument(
        "--method",
        action="store",
        required=True,
        help="Method to use for correlation analysis."
    )
    args = parser.parse_args()
    count_matrix = args.countmatrix
    method = args.method
    correlation_heatmap(count_matrix, method)
