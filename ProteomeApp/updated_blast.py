from os import system 
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast import NCBIXML


#Input file names as a string(seperated by commas)
def blast_proteomes(files_list):
	files = files_list.split(",")
	concatinate = "cat "
	#Create database used to query against (contains both proteomes)
	for i in files:
		 concatinate += i 
		 concatinate += " "
	concatinate += "> all_prot.fasta" 
	system(concatinate)
	system("makeblastdb -in all_prot.fasta -dbtype prot")
	system("mv *.phr *.psq *.pin blastdb/")
	blast_prog = '/usr/bin/blastp' 
	blast_db = 'blastdb/all_prot.fasta'
	output_files=[]
	for i in files:
	#Build the command-line for BLAST Run
		cmdline = NcbiblastpCommandline(cmd=blast_prog,
									query=i,
									db=blast_db,
									evalue=1e-5,
									outfmt=5,
									out ="res"+i+".xml")

	#... and execute.
		stdout, stderr = cmdline()
		output_files.append("res"+i+".xml")
	
	return output_files
