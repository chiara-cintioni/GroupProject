import pandas as pd


def reduce_file():
    input_file = input("Insert file name with file extension (txt) to modify: ")
    output_file = input("Insert file name with file extension (csv) where to save file rows without duplicates: ")
    data = pd.read_table(input_file, low_memory=False)
    data.drop_duplicates(['organism_name'], keep='last').to_csv(output_file, sep='	')


def reduce_file2():
    input_file = input("Insert file name with file extension (txt) to modify: ")
    output_file = input("Insert file name with file extension (csv) where to save file rows without duplicates: ")
    data = pd.read_table(input_file, low_memory=False)
    data.drop_duplicates(['benchmark id'], keep='last').to_csv(output_file, sep='	', skipinitialspace=True)


def remove_duplicates(file):
    output_dup = input("Insert file name with file extension (csv) where to save file rows without duplicates: ")
    k = []
    for line in file:
        words = line.split('	')
        i = words[4]
        if i not in k:
            k.append(i)
            output_dup.write(line)


def remove_diamonds(file):
    file = open(file, "r")
    output = open("files/taxonomy/TaxaName_TaxaRank.txt", "w")
    for line in file:
        taxa_name = line.split(sep="\t")[0]
        taxa_rank = line.split(sep="\t")[1]
        if "<" in taxa_name:
            taxa_name = taxa_name.split(sep=" <")[0]
        output.write(taxa_name + "\t" + taxa_rank)

