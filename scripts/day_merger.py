import os
import argparse
import pandas as pd
import math

def day_merger(directory):
    """
    Given a directory of count matrices, return a single count matrix with all the data.
    """
    #get filepath of the matrix directory
    if not os.path.isdir(directory):
        raise ValueError(f'{directory} is not a directory')
    if len(os.listdir(directory)) == 0:
        raise ValueError(f'{directory} is empty')
    
    filenames = []

    for filename in os.listdir(directory):
        print(filename)
        if filename.endswith('.csv'):
            filenames.append(filename)

    if len(filenames) == 0:
        raise ValueError(f'{directory} contains no csv files')
    
    #check if the first column heading is gene_id or Gene_id without making dataframe
    
    df1 = None
    #create empty dataframe to append to
    combined_df = pd.DataFrame()

    for i in range(0, len(filenames)):
        df1 = pd.read_csv(os.path.join(directory, filenames[i]), index_col='gene_id', delimiter='\t')
        #name the first column 'gene_id'
        df1.index.name = 'gene_id'
        print(df1)
        #concatenate the two dataframes
        if i == 0:
            #add gene_id column to empty dataframe
            combined_df['gene_id'] = df1['gene_id']
        #rename the column to the filename
        #get name of file
        combined_df[filename[i]] = df1['expected_count']
    
    print('done')

    #save the combined dataframe to a csv file
    combined_df.to_csv(os.path.join(directory, 'combined.csv'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--directory",
        action="store",
        nargs="+",
        required=True,
        help="The directory of raw count files to be merged"
    )
    args = parser.parse_args()
    directory = args.directory[0]
    day_merger(directory)