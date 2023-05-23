import argparse
import pandas as pd
from biomart import BiomartServer

def get_gene_name(ensembl_id):
    server = BiomartServer("http://www.ensembl.org/biomart")
    db = server.databases['ENSEMBL_MART_ENSEMBL']
    dataset = db.datasets['hsapiens_gene_ensembl']

    response = dataset.search({
        'attributes': ['external_gene_name'],
        'filters': {'ensembl_gene_id': ensembl_id}
    })

    for record in response.iter_lines():
        gene_name = record.decode('utf-8').split('\t')[0]
        return gene_name

def goi(log_fc_file):
    df = pd.read_csv(log_fc_file)
    num_entries = len(df['gene_id'])

    #open a new file to write genes to:
    new_file_name = log_fc_file.replace("_log_fc.csv", "_goi.txt")
    with open(new_file_name, "w") as new_file:
        for i in range(num_entries):
            gene_id = df['gene_id'][i]
            gene_name = get_gene_name(gene_id)
            new_file.write(gene_id + ': ' + gene_name + "\n")
        new_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log_fc_file",
        action="store",
        nargs="+",
        required=True,
        help="The directory to rename."
    )
    args = parser.parse_args()
    log_fc_file = args.log_fc_file[0]
    goi(log_fc_file)