import os
import argparse
import pandas as pd
import math

def day_merger(directory):
    #first, we need to get the list of files in the directory in order by their day
    files = os.listdir(directory)
    day_numbers = [int(file.split("_")[3]) for file in files]
    sorted_files = [file for _, file in sorted(zip(day_numbers, files))]
    #Sort day numbers
    day_numbers.sort()
    #print(day_numbers)
    #print(sorted_files)
    gene_list = {}
    dfs = []
    num_entries = 0

    #read in the dataframes
    for i in range(len(sorted_files)):
        dfs.append(pd.read_csv(os.path.join(directory, sorted_files[i]), sep='\t'))
        #get the length of the dataframe
        num_entries_temp = len(dfs[i]['gene_id'])
        if num_entries_temp > num_entries:
            num_entries = num_entries_temp
    
    #go through the list of gene ids
    for i in range(num_entries):
        gene_id = dfs[0]['gene_id'][i]
        #get the TPM values for each day
        tpm_values = []
        for x in range(len(dfs)):
            tpm_values.append(dfs[x]['TPM'][i])
        gene_list[gene_id] = [gene_id] + tpm_values
    

    #create a dataframe from the log_fc_list
    df = pd.DataFrame.from_dict(gene_list, orient='index')
    print(df)

    # Update column headers
    column_headings = ['gene_id'] + ['d{}'.format(day_numbers[i]) for i in range(len(day_numbers))]
    df.columns = column_headings

    #save the dataframe to a csv file
    df.to_csv(os.path.join(directory, directory + ".csv"), index=False)


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
    day_merger(directory)
