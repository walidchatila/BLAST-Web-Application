
import sqlite3, sys 
from database_class import * 

db = Database('devdata.sqlite')

db.in_db()
count = 0
mutual_best_hits = []

def best_hit_finder(query_p, best_hit =("", 1e1000,0,0,0)):
	for h in query_p.hits:
		if h.e_value < best_hit[1]:
			best_hit = (h.alignment_protein, h.e_value, h.length,h.positives,h.gaps)
	return best_hit

def ortholog_check(best_hit_1, best_hit_2):
	if best_hit_1[2] < best_hit_2[2]:
		lr = float(best_hit_1[2])/float(best_hit_2[2])
	elif best_hit_1[2] > best_hit_2[2]:
		lr = float(best_hit_2[2])/float(best_hit_1[2]) 
	else:
		lr = 1 
	
	pi_b1 = float(best_hit_1[3])/float(best_hit_1[2])
	pi_b2 = float(best_hit_2[3])/float(best_hit_2[2])
	
	return lr, pi_b1, pi_b2 

for p in Protein.select():
	if len(p.hits) > 0:
		best_hit_1 = best_hit_finder(p)
		if len(best_hit_1[0].hits) > 0:

			best_hit_2 = best_hit_finder(best_hit_1[0])
			if best_hit_2[0].gi == p.gi:	
				if (best_hit_1[0], p) not in mutual_best_hits:
					lr, pi_b1, pi_b2 = ortholog_check(best_hit_1, best_hit_2)
					if (lr > 0.90) and (pi_b1 and pi_b2 > 0.90) 
					and best_hit_1[1] < 1e-20 and best_hit_2[1] < 1e-20:
				
						mutual_best_hits.append((p, best_hit_1[0]))
						count +=1
						
conn = sqlhub.getConnection()
trans = conn.transaction()
for i in mutual_best_hits:
	p = Ortholog(protein_1=i[0], protein_2=i[1], connection=trans)
trans.commit()



