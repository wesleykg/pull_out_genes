# pull_out_genes

## How to Use

* `make split` will divide a specified genome or gene-set in fasta format into
   individual genes (file extension .fasta)
* `make blastdb` creates a blast database for each assembly (file extension .fa)
* `make search` performs a `blastn`, and if necessary, a `tblastx` search on all 
   databases using all genes from a specied genome or gene-set
* `make collect_scaffolds` creates an alignment for each gene found in each 
   species

Specify a genome or gene-set by typing genome=CODE 
* Code example: `LAGFR_pt-genes.fasta`


### Prepare Query Sequences
* Download an annotated genome or gene-set and convert names to the following 
   form:
   CODE-geneName (ex. LAGFR-atpF)
* Split each gene into its own file.

### Prepare Local Blast Database
* Trim names in the assembly to be 50 characters or less.
* Create a v4 blast database for each trimmed assembly.

### Search
* Use `blastn` or `tblastx` to find a gene in the assembly from an annotated 
   genome or gene-set. Produces a results file and an alignment of all the 
   significant blast hits from each assembly.

### Collect Scaffolds
1. Collect the full length scaffolds of each hit and place them in an alignment.
