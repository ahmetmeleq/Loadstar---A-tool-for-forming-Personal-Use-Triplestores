from rdflib import URIRef
from paths import DEFAULT_LOADSTAR_URI,DEFAULT_DATABASE_PATH, DATABASE_FOLDER, TEST_DATABASE_PATH
from paths import DEFAULT_LOADSTAR_USERNAME, DEFAULT_LOADSTAR_TABLENAME
from urlparse import urljoin
import datetime
from functionsTest import open_db
from rdflib import Literal, XSD


def autoform_metadata(username=DEFAULT_LOADSTAR_USERNAME, for_which_table=DEFAULT_LOADSTAR_TABLENAME, datetime = datetime.datetime.now()):

    URIs = URI_generate(username,for_which_table)
    subjURI= URIs["subjectURI"]
    metaURI= URIs["metaURI"]
    userURI= URIs["userURI"]

    db1 = ["loadstar.com/ontology#creation_time", datetime]
    db2 = ["loadstar.com/ontology#createdBy",userURI ]

    data = [db1, db2]
    mytbl=create_table_meta(metaURI,subjURI,data)

    return mytbl


def print_metadata(username=DEFAULT_LOADSTAR_USERNAME, tablename = DEFAULT_LOADSTAR_TABLENAME, path=DEFAULT_DATABASE_PATH):
    metaURI = URI_generate(username,tablename)["metaURI"]
    myg=open_context_meta(metaURI,path)

    for item in myg:
        print item

    myg.close()


def create_table_meta(contextURI, table_subject_URI, double_data, database_path = DEFAULT_DATABASE_PATH):

    table_context = open_context_meta(contextURI, database_path)
    subject = URIRef(table_subject_URI)



    for item in double_data:
        if type(item[1]) == datetime.datetime:
            table_context.add((subject,URIRef(item[0]), Literal(item[1],datatype=XSD.date)))
        else:
            table_context.add((subject, URIRef(item[0]), URIRef(item[1])))

    table_context.commit()
    return table_context




def open_context_meta(context_URI, database_path):
    my_database = open_db(database_path)

    tbl_URI= context_URI

    table_context = my_database.graph(URIRef(tbl_URI))
    return table_context


def URI_generate(username, tablename):
    usr_URI = urljoin(DEFAULT_LOADSTAR_URI, username)
    subjURI = urljoin(usr_URI, tablename)
    metaURI = urljoin(subjURI, "meta")
    return {"userURI":usr_URI,"subjectURI":subjURI,"metaURI":metaURI}

