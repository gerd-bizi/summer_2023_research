import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from matplotlib.colors import ListedColormap
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

    #sort the columns by day
    df1 = df1.reindex(sorted(df1.columns), axis=1)
    
    return df1
            

def pca_analysis(df):
    '''
    Given a combined matrix, perform PCA analysis and plot the results.
    '''
    pca = PCA(n_components=5)
    pca.fit(df)

    fig = plt.figure(figsize=(10, 8))

    ax = plt.axes()


    #make all datapoints of the same day the same color
    day_to_colour = {}
    for i in range(len(df.columns)):
        #split the column name by the underscore
        split_name = df.columns[i].split('_')
        #get the day, which is the last element of the split name
        day = int(split_name[-1])
        if day not in day_to_colour:
            #assign a random color
            day_to_colour[day] = np.random.rand(3,)
        ax.scatter(pca.components_[0][i], pca.components_[1][i], c = pca.components_[0][i], cmap=ListedColormap(day_to_colour[day]))

    days = sorted(day_to_colour.keys())
    # create a legend where each day uses its assigned colour
    # Add a legend with appropriate labels and colors
    handles, labels = ax.get_legend_handles_labels()
    legend = ax.legend(handles, labels, loc='upper left')

    # Create a custom legend with colored patches for each day
    legend_colors = [day_to_colour[day] for day in days]
    legend_labels = [f'Day {day}' for day in days]
    custom_legend = [plt.Line2D([], [], color=color, marker='o', linestyle='None', markersize=8) for color in legend_colors]
    ax.legend(title='Days', labels=[f'Day {day}' for day in days], loc='upper right')
    ax.set_xlabel('PC1' + ' (' + str(round(pca.explained_variance_ratio_[0] * 100, 2)) + '%)')
    ax.set_ylabel('PC2' + ' (' + str(round(pca.explained_variance_ratio_[1] * 100, 2)) + '%)')

    #ensure that the legend does not overlap with the plot
    ax = plt.title('PCA Analysis')
    ax = plt.show()

    #ensure graph and legend fit in window
    plt.tight_layout()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--directory",
        action="store",
        required=True,
        help="directory containing count matrices"
    )
    args = parser.parse_args()
    matrix_dir = args.directory
    complete_count_matrix = get_complete_count_matrix(matrix_dir)
    print(complete_count_matrix)
    pca_analysis(complete_count_matrix)