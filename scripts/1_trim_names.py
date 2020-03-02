'''Usage: paml_cleaner.py <alignment>'''

# Modules
import os  # Manipulating filenames
from Bio import SeqIO  # Reading in alignments


# Check if running interactively in an iPython console, or in a script from the
# command line
def in_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False
# Run in a script from the command line
if in_ipython() is False:
    from docopt import docopt  # Command line argument handler
    cmdln_args = docopt(__doc__)
    alignment = cmdln_args.get('<alignment>')
# Run interactively in an iPython console
if in_ipython() is True:
    alignment = '../data/GMHZ-SOAPdenovo-Trans-assembly.fa'


def name_truncate(record):
    record.description = ''
    record.id = record.id[:50]
    return record.id

alignment_name = os.path.splitext(alignment)[0]  # Retrieve filename
alignment_name = alignment_name.split('_aligned')[0]
alignment_format = os.path.splitext(alignment)[1]  # Retrieve filetype
alignment_format = alignment_format[1:]  # Remove '.' character from filetype

seqs_out = []
seqs_out_name = alignment_name + '_trimmed.' + alignment_format

for record in SeqIO.parse(alignment, format='fasta'):
    name_truncate(record)
    seqs_out.append(record)

SeqIO.write(seqs_out, handle=seqs_out_name, format='fasta')
