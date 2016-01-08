import sqlite3, sys 
from database_class import * 

db = Database('devdata.sqlite')
db.in_db()

query_protein_input = sys.argv[1]
alignment_protein_input = sys.argv[2]

p = Protein.byGi(query_protein_input)
a = None 
for a in p.hits:
	if i.alignment_protein.gi == alignment_protein_input:
		print "Length:", a.length,
		print "E-Value:", a.e_value,
		print "Score:", a.score
		print "Number of Positives:", a.positives
		print "Number of Gaps:", a.gaps