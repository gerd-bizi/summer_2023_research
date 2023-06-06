import argparse
import pandas as pd
import requests

# def get_gene_name(ensembl_id):
#     Entrez.email = "gerdbizi@mail.utoronto.ca"  # Replace with your email address
#     Entrez.api_key = "ee1a834186be8c7b72d8e3fcf421bda25208"
#     handle = Entrez.esearch(db="gene", term=ensembl_id)
#     record = Entrez.read(handle)
#     if record["IdList"]:
#         gene_id = record["IdList"][0]
#         gene_handle = Entrez.efetch(db="gene", id=gene_id, retmode="xml")
#         gene_record = Entrez.read(gene_handle)
#         if gene_record:
#             gene_name = gene_record[0]["Entrezgene_gene"]["Gene-ref"]["Gene-ref_locus"]
#             return gene_name
#     return "Not found"

def get_gene_name(ensembl_id):
    url = f"https://rest.ensembl.org/lookup/id/{ensembl_id}?content-type=application/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        gene_symbol = data.get("display_name")
        if not gene_symbol:
            gene_symbol = "Not found"
        return gene_symbol
    else:
        print("Error occurred while fetching gene symbol.")
        return "Not found"

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