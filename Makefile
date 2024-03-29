blastdb: $(patsubst data/%.fa, \
	data/%-blastdb, \
	$(wildcard data/*.fa))

search: $(patsubst data/$(genome)-%.fasta, \
    data/$(genome)-%_blast-results.csv, \
	$(wildcard data/$(genome)-*.fasta))

collect_scaffolds: $(patsubst data/$(genome)-%_blast-results.csv, \
	data/$(genome)-%_scaffolds.fasta, \
	$(wildcard data/$(genome)-*_blast-results.csv))

split:
	cd data/ ; python3 ../scripts/0_fasta_splitter.py $(genome)_*.fasta

data/%_trimmed.fa: data/%.fa
	cd data/ ; python3 ../scripts/1_trim_names.py $(notdir $^)

data/%-blastdb: data/%_trimmed.fa
	cd data/ ; makeblastdb -in $(^F) -blastdb_version 4 -dbtype nucl -parse_seqids -out $*
	mkdir -p $@
	cd data/ ; mv $*.nhr $*.nin $*.nog $*.nsd $*.nsi $*.nsq $(@F)

data/$(genome)-%_blast-results.csv: data/$(genome)-%.fasta
	cd data/ ; python3 ../scripts/2_search.py --evalue=1e-20 $(notdir $^)

data/$(genome)-%_scaffolds.fasta: data/$(genome)-%_blast-results.csv
	cd data/ ; python3 ../scripts/3_collect_scaffolds.py $(notdir $^)

cleantemp:
	cd data/ ; rm -drf *_scaffolds.fasta *_blast-missing.txt

cleansearch:
	cd data/ ; rm -drf *_scaffolds.fasta *-hsp-alignment.fasta.fasta *_*.xml \
	*_blast-results.csv *_blast-missing.txt all_assemblies_index.idx

clean:
	cd data/ ; rm -drf *-*.fasta *_trimmed.fa *-blastdb/ *_*.xml *_blast-results.csv \
	*-hsp-alignment.fasta *_blast-missing.txt all_assemblies_index.idx

cleanall:
	cd data/ ; rm -drf *-*.fasta *_trimmed.fa *-blastdb/ *_*.xml *_blast-results.csv \
	*-hsp-alignment.fasta *_blast-missing.txt all_assemblies_index.idx

.PHONY: clean cleantemp cleanall search split
.DELETE_ON_ERROR:
.PRECIOUS: data/%-assembly.fa data/%-stats.tsv data/%-assembly_cleaned.fasta data/%_trimmed.fa
