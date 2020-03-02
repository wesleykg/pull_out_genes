'''Usage: 0_fasta-splitter.py <fasta_file>'''

# Modules
from Bio import SeqIO  # Reading fasta sequences
import os  # Manipulating filenames


# Check if running interactively in an iPython console, or in a script
# from the command-line
def in_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False
# Run in a script from the command-line
if in_ipython() is False:
    from docopt import docopt  # Command-line argument handler
    cmdln_args = docopt(__doc__)
    in_fasta_path = cmdln_args.get('<fasta_file>')
# Run interatively in an iPython console
if in_ipython() is True:
    in_fasta_path = '../data/PHYPA.fasta'

# Retrieve just the filename, dropping the 'data/' part of the path
in_fasta = os.path.split(in_fasta_path)[1]

# Read the entire fasta file into memory and then loop through each sequence
# record and write it to file. The filename is derived from the .id of the
# sequence record; this should usually be the name, but can be different if '|'
# characters are used in the sequence name
for record in list(SeqIO.parse(in_fasta, 'fasta')):
    filename = record.id + '.fasta'
    with open(filename, 'w') as out_fasta:
        SeqIO.write(record, out_fasta, 'fasta')
