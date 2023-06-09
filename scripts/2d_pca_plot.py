import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from matplotlib.colors import ListedColormap

def pca_analysis(count_matrix):
    '''
    Given a count matrix, perform PCA analysis and plot the results.
    '''
    #First, we must read in the count matrix
    df = pd.read_csv(count_matrix, index_col='gene_id')
    #Now, we must perform PCA analysis
    pca = PCA(n_components=3)
    pca.fit(df)

    fig = plt.figure(figsize=(10, 8))

    ax = plt.axes()


    #make all datapoints of the same day the same color
    #find all the days ie. d0, d1, d2, etc.
    day_to_colour = {}
    for i in range(len(df.columns)):
        #split the column name by the underscore
        split_name = df.columns[i].split('_')
        #get the day
        day = int(split_name[3])
        if day not in day_to_colour:
            #assign a random color
            day_to_colour[day] = np.random.rand(3,)
        ax.scatter(pca.components_[1][i], pca.components_[2][i], c = pca.components_[2][i], cmap=ListedColormap(day_to_colour[day]))

    days = sorted(day_to_colour.keys())
    #create a legend where each day uses its assigned colour
    # Add a legend with appropriate labels and colors
    handles, labels = ax.get_legend_handles_labels()
    legend = ax.legend(handles, labels, loc='upper left')

    # Create a custom legend with colored patches for each day
    legend_colors = [day_to_colour[day] for day in days]
    legend_labels = [f'Day {day}' for day in days]
    custom_legend = [plt.Line2D([], [], color=color, marker='o', linestyle='None', markersize=8) for color in legend_colors]
    ax.legend(title='Days', labels=[f'Day {day}' for day in days], loc='upper right')
    ax.set_xlabel('PC2' + ' (' + str(round(pca.explained_variance_ratio_[1] * 100, 2)) + '%)')
    ax.set_ylabel('PC3' + ' (' + str(round(pca.explained_variance_ratio_[2] * 100, 2)) + '%)')

    #ensure that the legend does not overlap with the plot
    ax = plt.title('PCA Analysis')
    ax = plt.show()

    #ensure graph and legend fit in window
    plt.tight_layout()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--countmatrix",
        action="store",
        required=True,
        help="Count matrix for experiment."
    )
    args = parser.parse_args()
    count_matrix = args.countmatrix
    print(count_matrix)
    pca_analysis(count_matrix)
