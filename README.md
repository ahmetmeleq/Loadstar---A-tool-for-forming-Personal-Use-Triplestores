# Loadstar---A-tool-for-forming-Personal-Use-Triplestores


**Introduction**

This tool let's you form RDF tables for personal use such as taking notes or forming pages with semantic data. It builds IRI contexts together with the RDF tables, it can pull data from other resources such as DBpedia.

You can download and check out the articles for detailed information. 
In the Loadstar Report file, you will see an introduction to the project.
In the Loadstar - Annotations file, you will see a detailed proposal on how to provide the tool with annotation fuctionality.




**The steps to test the features:**

0.  Project is written on Python 2.7 . Check dependencies from dependencies.png file. All dependencies may not be critical, since some libraries were installed to test features which were cancelled and currently do not exist in the project.


1.  CHECK PATHS.PY FILE. MAKE the necessary adjustments for your default database file path via changing these variable values:

*  DEFAULT_DATABASE_PATH = 'C:/Users/ahmet/PycharmProjects/Loadstar/database/loadstar'

*  DATABASE_FOLDER = 'C:/Users/ahmet/PycharmProjects/Loadstar/database'

*  TEST_DATABASE_PATH = 'C:/Users/ahmet/PycharmProjects/Loadstar/database/loadstartest'



Carefully investigate paths.py file before starting to test anything. Try to understand the variables.
You can also make optional adjustments to the default user, default table name etc. however it is advised to test the project with their original forms at first.




2.  Open the test.py file, and start testing. The operations are ORDERED. So it is advised for you to work them in order. Otherwise there could be complications such as trying to create a table without a database existing.

print_graph functions are optional to run. However they provide nice feedback to check if the operations worked.



3.  In case that you are interested, modify functionsTest.py for ordinary functions and metadataFuncs.py for functions on metatable generation.
