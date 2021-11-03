'''Usage: 1_search.py [--evalue=<NUMBER>] <query_gene>'''

# Modules
import os  # Manipulating filenames
from glob import glob  # Finding relevant databases to search
from Bio import SeqIO  # Reading the query sequence for blast
from Bio.Blast import NCBIXML  # Parsing blast results
from Bio.Blast.Applications import NcbiblastnCommandline  # Running blastn
from Bio.Blast.Applications import NcbitblastxCommandline  # Running tblastx


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
    query_file = cmdln_args.get('<query_gene>')
    db_list = glob(os.getcwd() + '/*-blastdb')
    evalue = cmdln_args.get('--evalue')
# Run interactively in an iPython console
if in_ipython() is True:
    query_file = '../data/NOTAE-rps18.fasta'
    db_list = glob('../data/*-blastdb')
    evalue = 1e-20


def blastn(query, evalue, db, out):
    blastn_search = NcbiblastnCommandline(query=query, evalue=evalue,
                                          db=db, num_threads=2,
                                          out=out, outfmt=5)
    blastn_search()  # initializes the search
    print('Searching for', gene_name, 'in', db_name, 'using blastn')


def tblastx(query, evalue, db, out):
    tblastx_search = NcbitblastxCommandline(query=query, evalue=evalue,
                                            db=db, num_threads=2,
                                            out=out, outfmt=5)
    tblastx_search()  # initializes the search
    print('Searching for', gene_name, 'in', db_name, 'using tblastx')


def retrieve_blast_results(results_file, search_type):
    with open(results_file, 'r') as blast_results_file:
        blast_results = NCBIXML.read(blast_results_file)

    if not blast_results.alignments:  # Syntax for checking if no results found
        # Run tblastx
        if search_type == 'blastn':
#            aa_query_seq = query_seq.seq.translate()
#            with open(query_name + '_tblastx-hsp-alignment.fasta', 'a') as \
#                    out_alignment:
#                out_alignment.write('>' + gene_name + '\n' +
#                                    str(aa_query_seq) + '\n')
            tblastx_xml_name = query_name + '_' + db_id + '_tblastx' + '.xml'
            tblastx(query_file, evalue=evalue, db=db_path,
                    out=tblastx_xml_name)
            retrieve_blast_results(tblastx_xml_name, search_type='tblastx')
        elif search_type == 'tblastx':
            with open(query_name + '_blast-results.csv', 'a') as out_results:
                print('No hits found for', gene_name, 'in', db_name)
                out_results.write(query_name + ',' + db_id + ',' +
                                  'None found' + '\n')

    for record in blast_results.alignments:
        hit_len = str(record.length)
        hit_name = record.accession
        for hsps in record.hsps:
            ali_len = str(hsps.align_length)
            query_start_pos = str(hsps.query_start)
            query_end_pos = str(hsps.query_end)
            e_val = str(hsps.expect)
            hit_seq = str(hsps.sbjct[0:])
            hit_start_pos = hsps.sbjct_start
            hit_end_pos = hsps.sbjct_end
            if hit_start_pos - hit_end_pos < 0:
                orientation = 'sense'
            elif hit_start_pos - hit_end_pos > 0:
                orientation = 'antisense'

            # Write fasta alignment of the part of the scaffold that aligns
            # to the query sequence, not the whole scaffold
            with open(query_name + '_' + search_type + '-hsp-alignment.fasta',
                      'a') as out_alignment:
                        out_alignment.write('>' + hit_name + '\n' + hit_seq +
                                            '\n')

            # Append the results of a single blastn match to
            # 'GENOME-gene_blast-results.csv'
            with open(query_name + '_blast-results.csv', 'a') as out_results:
                out_results.write(query_name + ',' + db_id + ',' +
                                  hit_name + ',' + query_len + ',' +
                                  hit_len + ',' + ali_len + ',' +
                                  query_start_pos + ',' + query_end_pos + ',' +
                                  str(hit_start_pos) + ',' + str(hit_end_pos) +
                                  ',' + e_val + ',' + orientation + ',' +
                                  search_type + ',' + '\n')


# There should be at least one blast database in the same folder with the
# name: 'ID-blastdb/ID'

# Reads in the query sequence for blast and records the name and length of
# the gene
query_seq = SeqIO.read(query_file, 'fasta')
query_len = str(len(query_seq))
query_name = query_seq.id
gene_name = query_name.split('-')[1]

# Write header for future blast results file
with open(query_name + '_blast-results.csv', 'a') as out_results:
    out_results.write('query' + ',' + 'blast_db' + ',' + 'hit' + ',' +
                      'query_length' + ',' + 'hit_length' + ',' +
                      'alignment_length' + ',' + 'query_start_position' + ',' +
                      'query_end_position' + ',' + 'hit_start_position' +
                      ',' + 'hit_end_position' + ',' + 'e_value' + ',' +
                      'orientation' + ',' + 'blast_type' + '\n')

# Add the query seq to HSP alignments with all positive hits added
with open(query_name + '_blastn-hsp-alignment.fasta', 'a') as out_alignment:
    out_alignment.write('>' + query_name + '\n' + str(query_seq.seq) + '\n')

# Loop through each database, and search for matches to the query sequence
# using blastn. Results for each search are written to an xml file.
for db in db_list:
    db_name = os.path.split(db)[1]
    db_id = db_name.split('-')[0]
    db_path = db + '/' + db_id

    blastn_xml_name = query_name + '_' + db_id + '_blastn' + '.xml'

    # Search using blastn, and save results to an xml file
    blastn(query_file, evalue=evalue, db=db_path, out=blastn_xml_name)

    # Retrieve the results of the blast run
    retrieve_blast_results(blastn_xml_name, search_type='blastn')
