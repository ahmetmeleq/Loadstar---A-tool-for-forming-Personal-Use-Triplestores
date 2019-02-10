from rdflib import Dataset, Namespace
from rdflib.store import NO_STORE, VALID_STORE
from rdflib.plugins.sparql import prepareQuery
from rdflib import URIRef
from paths import DEFAULT_LOADSTAR_URI,DEFAULT_DATABASE_PATH, DATABASE_FOLDER, TEST_DATABASE_PATH
from paths import DEFAULT_LOADSTAR_USERNAME, DEFAULT_LOADSTAR_TABLENAME
from urlparse import urljoin
import os.path
from rdflib.plugins.sparql import prepareQuery
import rdflib





#tested, works, creates database if it does not exist on the path
def create_db(path=DATABASE_FOLDER, db_name='loadstar'):

    path=os.path.join(path,db_name)
    my_graph = Dataset('Sleepycat')
    store_state = my_graph.open(path, create=False)
    assert store_state == NO_STORE, 'There is a database in this path already.'
    if store_state == NO_STORE:
        my_graph.open(path, create=True)
        my_graph.commit()

    else:
        assert store_state == VALID_STORE, 'The underlying store is corrupt'

    return my_graph




#our database has several contexts in it currently. every table founds a context in our database.
#this function returns all contexts gathered in an object. That object's type is Dataset. (it is defined in RDFLib)
#tested, works, returns the aggragate database as a Dataset object.
def open_db(path = DEFAULT_DATABASE_PATH):
    my_graph = Dataset('Sleepycat')
    store_state = my_graph.open(path, create=False)

    assert store_state != NO_STORE, 'Store does not exist'
    assert store_state == VALID_STORE, 'The underlying store is corrupt'

    return my_graph




#creates a context in our database.
#tested, works, creates a table with a list of triples. (subject + doubles)
def create_table(username, table_name, table_subject_URI, double_data, database_path = DEFAULT_DATABASE_PATH):

    table_context = open_context(username, table_name, database_path)
    subject = URIRef(table_subject_URI)



    for item in double_data:
        table_context.add((subject, URIRef(item[0]), URIRef(item[1])))

    table_context.commit()
    return table_context




#adds data into a context.
#tested, works, adds a list of triples to the graph (triples being equal to subject + doubles)
def table_add_tri(username, table_name, table_subject_URI, double_data, database_path = DEFAULT_DATABASE_PATH):

    table_context=open_context(username,table_name,database_path)
    subject = URIRef(table_subject_URI)


    for item in double_data:
        table_context.add((subject, URIRef(item[0]), URIRef(item[1])))

    table_context.commit()
    return table_context




#deletes a triple from a particular context.
#tested, works, deletes only one row from the table. designed as the backend function for a cross button (delete button) of a row.
def table_del_tri_one(username, table_name, table_subject_URI, double, database_path = DEFAULT_DATABASE_PATH):
    table_context = open_context(username, table_name, database_path)
    subject = URIRef(table_subject_URI)
    triple = (subject, URIRef(double[0]), URIRef(double[1]))
    table_context.remove(triple)




#deletes a list of triples from a particular context.
def table_del_tri_list(username, table_name, table_subject_URI, doubles, database_path = DEFAULT_DATABASE_PATH):
    table_context = open_context(username, table_name, database_path)
    subject = URIRef(table_subject_URI)
    for item in doubles:
        triple = (subject, URIRef(item[0]), URIRef(item[1]))
        table_context.remove(triple)




#opens a context. this means creating a graph object on computer memory. the data of the object had been in the database before.
def open_context(username,table_name,database_path):
    my_database = open_db(database_path)

    usr_URI=urljoin(DEFAULT_LOADSTAR_URI, username)
    tbl_URI=urljoin(usr_URI,table_name)

    table_context = my_database.graph(URIRef(tbl_URI))
    return table_context




#tested, works. prints a tables contents.
def print_graph(path=DEFAULT_DATABASE_PATH, username=DEFAULT_LOADSTAR_USERNAME, tablename = DEFAULT_LOADSTAR_TABLENAME):
    myg=open_context(username,tablename,path)

    for item in myg:
        print item

    myg.close()




#loads a topic from a resource, returns a new graph that has the data on it.
def load_resource(resource_name='http://dbpedia.org/resource/', topic_on_resource='Mathematics'):
    mysub = urljoin(resource_name,topic_on_resource)
    mydum = rdflib.Graph('IOMemory')
    mydum.load(mysub)
    return mydum



#tested, works. a query which finds the common objects in two graphs.
def sparqlCommonObj(usr1, usr2, tbl1, tbl2, database_path = DEFAULT_DATABASE_PATH):
    loadstar = Namespace('https://loadstar.com/ontology#')

    myg = open_context(usr1, tbl1, database_path)
    for item in myg:
        if item != None:
            subj1=item[0]
            break

    myg2 = open_context(usr2, tbl2, database_path)
    for item in myg2:
        if item != None:
            subj2=item[0]
            break

    mydum = myg + myg2
    myquer = prepareQuery("""SELECT ?object ?a ?b WHERE {?subject1 ?a ?object .
                                                   ?subject2 ?b ?object .}""",
                          initNs= {"load": loadstar})

    for row in mydum.query(myquer, initBindings={"subject1": subj1, "subject2": subj2}):
        print row




#tested, works. pulls data to a table from an outside resource.
def autopull(username, table_name, topic, source="http://dbpedia.org/resource/", database_path = DEFAULT_DATABASE_PATH):
    mysub = urljoin(source,topic)
    mysub = URIRef(mysub)
    myg = open_context(username, table_name, database_path)
    mydum = load_resource(source,topic)

    for item in mydum:
        if item[0] == URIRef(mysub):
            myg.add(item)
        elif item[2] == URIRef(mysub):
            myg.add((item[2],item[1],item[0]))
        else:
            continue
    myg.commit()
    myg.close()
    mydum.close()
    return




def parse_to_source_URI(resource_name):
    if resource_name == 'dbpedia':
        resource_name='http://dbpedia.org/resource/'
    elif resource_name == 'wikidata':
        resource_name='https://www.wikidata.org/wiki/'
    else:
        assert False, 'This is not a known resource type for Loadstar.'

    resource_name = Namespace(resource_name)
    return resource_name