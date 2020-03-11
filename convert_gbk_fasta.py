from Bio import SeqIO
import re
import sys
import warnings
warnings.filterwarnings("ignore")

"""
Script para extraer CDSs de archvo en formato gbk

pip install biopython
"""

archivo = sys.argv[1]

file = open(archivo, "r")
file = file.read()
line = re.sub('_length_', '\t', file)
line = re.sub('_cov_\d+[.]\d+', '', line)
new = open('new_'+archivo, 'w')
new.write(line)
new.close()
input_handle  = open('new_'+archivo, "r")
output_handle = open(archivo.split('.')[0]+".fasta", "w")
for seq_record in SeqIO.parse(input_handle, "genbank"):
    for seq_feature in seq_record.features:
        if 'locus_tag' in seq_feature.qualifiers.keys():
            if 'translation' in seq_feature.qualifiers.keys():
                if seq_feature.type == "CDS":
                    output_handle.write(">%s %s\n%s\n" % (
                        seq_feature.qualifiers['locus_tag'][0],
                        seq_feature.qualifiers['product'][0],
                        seq_feature.qualifiers['translation'][0]))
output_handle.close()
input_handle.close()