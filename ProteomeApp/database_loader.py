from database_class import *
from updated_blast import *

proteome_1 = raw_input("Please enter the name of the file for the first proteome: ")
try:
	open(proteome_1)
except IOError:
	print >>sys.stderr, "Please enter a valid file name."
	sys.exit()
proteome_2 = raw_input("Please enter the name of the file for the second proteome: ")
try:
	open(proteome_2)
except IOError:
	print >>sys.stderr, "Please enter a valid file name."
	sys.exit()
db = raw_input("Please provide the name of the database: ")


input_files = [proteome_1, proteome_2]
output_files = blast_proteomes(proteome_1+','+proteome_2) 

proteomes = ["proteome"+str(x) for x, y in enumerate(output_files)]
prot_instances={}
for num, i in enumerate(output_files):
	if num == 0:
		prot_instances[proteomes[num]] = Tables(db,input_files[num], i, num+1, True)
	else:
		prot_instances[proteomes[num]] = Tables(db,input_files[num], i, num+1, False)

for i in prot_instances:
	prot_instances[i].prot_load()
for i in prot_instances:
	prot_instances[i].align_load()

