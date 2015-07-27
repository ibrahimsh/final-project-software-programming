final-project-software-programming
==================================

*************************************************************************************************************************
-------------------------------------- JCEontology APPlication ---------------------------------------------------------
*************************************************************************************************************************
Project: Extracting ontological knowledge from keywords describing books in the United Catalogue of the National Library.

*************************************************************************************************************************
created by : ibrahim shweiki
Email:enge.sibrahim@gmail.com 
git hub repository : https://github.com/ibrahimsh/final-project-software-programming
department : computer software engineering 
collage : Ezrili Jerusalem engineering collage 
*************************************************************************************************************************
This Application get books meta-data and building RDF File 
*************************************************************************************************************************
classes and models:
************************************************************************************************************************
MarcParser.py  - class that get Marc files as input and generate it to JASON files as output. by creating folder inside the                   folder json files each file named in name of book
				         and the files arranged by the alphabet A-Z and also contain Arabic books,Hebrew books and books in other                      language arranged by alphabet.

JsonParser.py  - class the read the json files as input copying the subjects to text file.Each line in this file contains                     subject,bookTitle,link were the book exist.

HashTable.py   - class that read the subjects file as input and analysing each line. 
			   - each line contain data such as bookTitle,link,and subject . this class contains functions to parse the line ,by separating the link,book title ,term
			   - the term (subject) contain data by analysing the term with NLTK- natural language processing tools , that decide             Vocabulary type and grammar analysing
			   - if it word is Noun or Adverb,adjective,verb - then function create the data structure connected to NLTK Function             to decide were the world should be in RDF graph based on three.
			   - the three is (subject,predicate,object) if word type is class or subClass or predicate to build the ontology.
			   - contains functions to find the relation between terms using edit distance algorithm.
			   - contains function for text cleaning .
				 
rdfOntology.py - class that depend on RDFLib models to build and store data into rdfFile as output .
OWL.py         - class that contain W3School models for ontology
