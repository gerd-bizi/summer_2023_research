import argparse
import pandas as pd
import math

def meets_cut_off(log_fc_values, cut_off_value):
    flag = False
    for i in range(len(log_fc_values)):
        if not flag:
            if log_fc_values[i] < -0.1 * cut_off_value:
                return False
            if log_fc_values[i] >= cut_off_value:
                flag = True
        else:
            if log_fc_values[i] < -0.1 * cut_off_value:
                return False
    return flag

def cut_off(log_tpm_file):
    df = pd.read_csv(log_tpm_file)
    num_entries = len(df['gene_id'])
    num_columns = len(df.columns)

    #temporary hardcoding, value is just a guess
    cut_off_value = 1.5

    #make a new dataframe with the same column headings
    df_sig_log_fc = pd.DataFrame(columns=df.columns)

    for i in range(num_entries):
        gene_id = df['gene_id'][i]
        log_fc_values = []
        for j in range(1, num_columns):
            log_fc_values.append(df.iloc[i, j])
        if meets_cut_off(log_fc_values, cut_off_value):
            #add the row to the new dataframe
            df_sig_log_fc.loc[len(df_sig_log_fc)] = df.iloc[i]
    
    new_file_name = log_tpm_file.replace("_log_fc.csv", "_sig_log_fc.csv")
    df_sig_log_fc.to_csv(new_file_name, index=False)


def filter(log_fc_file, method):
    if method == "cut-off":
        cut_off(log_fc_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log_fc_file",
        action="store",
        nargs="+",
        required=True,
        help="The log fc file to use."
    )
    parser.add_argument(
        "--method",
        action="store",
        nargs="+",
        required=True,
        help="The method to use to find significant log fold changes."
    )
    args = parser.parse_args()
    log_fc_file = args.log_fc_file[0]
    method = args.method[0]
    filter(log_fc_file, method)
