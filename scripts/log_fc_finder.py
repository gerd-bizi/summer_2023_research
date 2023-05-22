import os
import argparse
import pandas as pd
import math

def log_fc_finder(tpm_file):
    log_fc_list = {}
    num_entries = 0

    #read in the tpm_file into a dataframe
    df = pd.read_csv(tpm_file)

    #get number of entries in the dataframe
    num_entries = len(df['gene_id'])

    #get number of columns
    num_columns = len(df.columns)

    for i in range(num_entries):
        gene_id = df['gene_id'][i]
        #get the TPM values for each day
        tpm_values = []
        for j in range(1, num_columns):
            tpm_values.append(df.iloc[i, j])
        if max(tpm_values) >= 0.5:
            log_fc_vals = []
            for x in range(len(tpm_values) - 1):
                tpm1 = tpm_values[x]
                tpm2 = tpm_values[x + 1]
                if tpm1 == 0 or tpm2 == 0:
                    tpm1 += 0.01
                    tpm2 += 0.01
                log_fc = math.log2(tpm2 / tpm1)
                log_fc_vals.append(log_fc)
            log_fc_list[gene_id] = [gene_id] + log_fc_vals

    df_log_fc = pd.DataFrame.from_dict(log_fc_list, orient='index')

    days = df.columns[1:]

    #create new column headings
    day_comps = []
    for i in range(len(days) - 1):
        day_comps.append('{}v{}'.format(days[i+1], days[i]))

    #update column headings
    df_log_fc.columns = ['gene_id'] + day_comps

    new_file_name = tpm_file.replace(".csv", "") + "_log_fc.csv"

    #write to csv
    df_log_fc.to_csv(new_file_name, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tpm_file",
        action="store",
        nargs="+",
        required=True,
        help="The directory to rename."
    )
    args = parser.parse_args()
    tpm_file = args.tpm_file[0]
    log_fc_finder(tpm_file)
