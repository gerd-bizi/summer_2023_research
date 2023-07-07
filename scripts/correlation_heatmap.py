import pandas as pd
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import os

def get_complete_count_matrix(matrix_dir):
    """
    Given a directory of count matrices, return a single count matrix with all the data.
    """
    #get filepath of the matrix directory
    if not os.path.isdir(matrix_dir):
        raise ValueError(f'{matrix_dir} is not a directory')
    if len(os.listdir(matrix_dir)) == 0:
        raise ValueError(f'{matrix_dir} is empty')
    
    filenames = []

    for filename in os.listdir(matrix_dir):
        print(filename)
        if filename.endswith('.csv'):
            filenames.append(filename)

    if len(filenames) == 0:
        raise ValueError(f'{matrix_dir} contains no csv files')
    
    #check if the first column heading is gene_id or Gene_id without making dataframe
    
    df1 = None
    df2 = None

    try:
        df1 = pd.read_csv(os.path.join(matrix_dir, filenames[0]), index_col='gene_id')
    except ValueError:
        try:
            df1 = pd.read_csv(os.path.join(matrix_dir, filenames[0]), index_col='Gene_id')
        except ValueError:
            df1 = pd.read_csv(os.path.join(matrix_dir, filenames[0]), index_col='Geneid')

    for i in range(1, len(filenames)):
        try:
            df2 = pd.read_csv(os.path.join(matrix_dir, filenames[i]), index_col='gene_id')
        except ValueError:
            try:
                df2 = pd.read_csv(os.path.join(matrix_dir, filenames[i]), index_col='Gene_id')
            except ValueError:
                df2 = pd.read_csv(os.path.join(matrix_dir, filenames[i]), index_col='Geneid')
        #concatenate the two dataframes
        df1 = pd.concat([df1, df2], axis=1)

    #sort the columns by the last number in the column name
    df1 = df1.reindex(sorted(df1.columns), axis=1)
    
    return df1

def correlation_heatmap(df, method):
    '''
    Given a count matrix, perform PCA analysis and plot the results.
    '''
    
    #organize the dataframe by the last number in the column name
    df = df.reindex(sorted(df.columns, key=lambda x: int(x.split('_')[-1])), axis=1)
    print(len(df.columns))

    corr = df.corr(method=method)

    # Plot the heatmap
    plt.figure(figsize=(10, 8))  # Adjust the figure size as per your preference
    sns.heatmap(corr, cmap='coolwarm')

    # Set the axis labels and title
    plt.xlabel('Sample IDs')
    plt.ylabel('Sample IDs')
    plt.title('Correlation Heatmap')

    # Remove the extra lines from the heatmap
    plt.gca().spines['top'].set_visible(False)

    # Show the heatmap
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--directory",
        action="store",
        required=True,
        help="directory containing count matrices"
    )
    parser.add_argument(
        "--method",
        action="store",
        required=True,
        help="method to use for correlation"
    )
    args = parser.parse_args()
    matrix_dir = args.directory
    method = args.method
    complete_count_matrix = get_complete_count_matrix(matrix_dir)
    print(complete_count_matrix)
    correlation_heatmap(complete_count_matrix, method)
