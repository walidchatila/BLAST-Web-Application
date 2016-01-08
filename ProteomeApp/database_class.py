from sqlobject import *
import os.path
from Bio.Blast import NCBIXML
from sqlobject import ForeignKey, MultipleJoin
from Bio import SeqIO

class Protein(SQLObject): 
	organism = IntCol()
	gi = StringCol(alternateID=True)
	accesion = StringCol()
	protein_name = StringCol()
	hits = MultipleJoin("Alignment", joinColumn='query_protein_id')


class Alignment(SQLObject): 
	alignment_protein = ForeignKey("Protein")
	query_protein = ForeignKey("Protein")
	length = IntCol()
	e_value = FloatCol()
	score = FloatCol()
	positives = IntCol()
	gaps = IntCol()

class Ortholog(SQLObject):
	protein_1 = ForeignKey("Protein")
	protein_2 = ForeignKey("Protein")





class Database:
	def __init__(self,  dbfile='', fasta='', blast_xml='', prot_num=None, create=''):
		self.dbfile = dbfile
		self.fasta = fasta
		self.blast_xml = blast_xml
		self.prot_num = prot_num
		self.create= create


	def in_db(self, new=False):
		conn_str = os.path.abspath(self.dbfile)
		conn_str = 'sqlite:' + conn_str
		#Connect to Database
		sqlhub.processConnection = connectionForURI(conn_str)
		if new:
			# Create new tables (remove old ones if they exist)
			Protein.dropTable(ifExists=True)
			Alignment.dropTable(ifExists=True)
			Ortholog.dropTable(ifExists=True)
			Protein.createTable()
			Alignment.createTable()
			Ortholog.createTable()


class Tables(Database):
		
	def prot_load(self):
		if self.create:
			self.in_db(new=True)
		else:
			self.in_db()

		handle = open(self.fasta)
		conn = sqlhub.getConnection()
		trans = conn.transaction()
		for record in SeqIO.parse(handle, "fasta"):
			sl = record.description.split('|')
			gi = sl[1].strip()
			accesion =sl[3].strip()
			protein_name = sl[4].strip()
			organism = self.prot_num
			#Check if protein already in table
			try:
				Protein.selectBy(gi=gi, connection=trans)[0]
			except IndexError:
				p = Protein(organism=organism, gi=gi, accesion=accesion,
				 protein_name=protein_name, connection=trans)
		trans.commit()
		handle.close()
			

	def align_load(self):
		self.in_db()
		conn = sqlhub.getConnection()
		trans = conn.transaction()
		
		result_handle = open(self.blast_xml)
		for  blast_result in NCBIXML.parse(result_handle):
			query_name = blast_result.query
			sl = query_name.split('|')
			gi =sl[1].strip()
			query_id = Protein.byGi(gi, connection=trans)
			q_organism = query_id.organism 
			
			for alignment in blast_result.alignments:
				sp = alignment.title.split(' ')
				a_gi = sp[1].split('|')[1]
				alignment_id = Protein.byGi(a_gi, connection=trans)
				a_organism = alignment_id.organism 
				if a_organism != q_organism:
					for hsp in alignment.hsps:
						length = hsp.align_length 
						e_value = hsp.expect
						score = hsp.score
				        positives = int(hsp.positives)	
				        gaps = int(hsp.gaps)
			        	a = Alignment(
				        	alignment_protein = alignment_id, query_protein = query_id,
				        	length = length, e_value = e_value,
				        	score = score,
				        	positives = positives, gaps = gaps, connection=trans)
		trans.commit()
		result_handle.close()
