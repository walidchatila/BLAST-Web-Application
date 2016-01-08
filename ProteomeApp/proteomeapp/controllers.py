# -*- coding: utf-8 -*-
"""This module contains the controller classes of the application."""

# symbols which are imported by "from proteomeapp.controllers import *"
__all__ = ['Root']

# third-party imports
from turbogears import controllers, expose, flash, validate, validators, widgets, error_handler, paginate
from model import Protein, Alignment, Ortholog

# project specific imports
# from proteomeapp import model
# from proteomeapp import json


# log = logging.getLogger("proteomeapp.controllers")

class SearchFields(widgets.WidgetsList):
	query = widgets.TextField(label="Search Term")
	mode = widgets.SingleSelectField(label="Search Mode",
											options=[
													'Accession',
													'GI'],
											default="GI")
class SearchFieldsSchema(validators.Schema):
    query = validators.String(min=3, strip=True)
    mode = validators.OneOf(['Accession', "GI"])
search_form = widgets.TableForm(
	fields = SearchFields(),
    validator = SearchFieldsSchema(),
	action = "protein",
	submit_text = "Search")

class Root(controllers.RootController):
    """The root controller of the application."""

    @expose(template="proteomeapp.templates.welcome")
    def index(self):
        """"Show the welcome page."""
        return dict(title="These are all the proteomes!")
    
    @expose(template="proteomeapp.templates.search_page")
    def search_page(self):
        title = "Search Page"
        return dict(title=title, form=search_form)

    @expose(template="proteomeapp.templates.protein")
    @validate(form=search_form)
    @error_handler(search_page)
    def protein(self, query, mode):
    	"""Return the Protein object"""
        o = ''
        p=None
        if mode == "GI":
            p = Protein.select(Protein.q.gi.contains(query))
        elif mode == "Accession":
            p = Protein.select(Protein.q.accesion.contains(query))
        if p[0].organism == 1:
            o = "Drosophila melanogaster"
        else:
            o = "Saccaromyces cervisiae"
    	title = "Protein: " + mode + query
    	return dict(title=title, protein=p[0], organism=o)


    @expose(template="proteomeapp.templates.alignment")
    def alignment(self, p_gi, a_gi):
    	"""Return the Alignments object"""
    	p = Protein.byGi(p_gi)
    	a = None
    	for i in p.hits:
    		if i.alignment_protein.gi == (a_gi):
    			a = i  
        
        if a.query_protein.organism == 1:
            q_org = "Drosophila melanogaster"
        else:
            q_org = "Saccaromyces cervisiae"
    	if a.alignment_protein.organism == 1:
            a_org = "Drosophila melanogaster"
        else:
            a_org = "Saccaromyces cervisiae"
        title = "Alignment: " + a_gi + "and" + p_gi
    	return dict(title=title, alignment=a, alignment_organism=a_org, query_organism=q_org)


    

    @expose(template="proteomeapp.templates.protein_list")
    @paginate('proteins')
    def protein_list(self):
        title = "Search Page"
        proteins = Protein.select()
        count = proteins.count()
        return dict(title=title, proteins=proteins, count=count)

    @expose(template="proteomeapp.templates.orthologs")
    @paginate('orthologs')
    def orthologs(self):
        title = "Ortholog"
        orthologs= Ortholog.select()
        count = Ortholog.select().count()
       
        return dict(title=title, orthologs=orthologs, count=count)