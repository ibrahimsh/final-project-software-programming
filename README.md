afinal-project-software-programming
==================================

*************************************************************************************************************************
-------------------------------------- JCEontology APPlication ---------------------------------------------------------
*************************************************************************************************************************
Project: Extracting ontological knowledge from keywords describing books in the United Catalogue of the National Library.

*************************************************************************************************************************
created by : ibrahim shweiki.

Email:enge.sibrahim@gmail.com .

github repository : https://github.com/ibrahimsh/final-project-software-programming.

department : computer software engineering.

college : Azrieli Jerusalem engineering collage 
*************************************************************************************************************************
The Tool use books meta-data as input  and builds ontology in formate RDF file and OWL file  
*************************************************************************************************************************
classes and models:
************************************************************************************************************************
MarcParser.py  - class that gets Marc files as input and generates JASON files as output. By creating a folder inside the                   folder json files each file is named by the  name of the  book and the files are arranged by the alphabet A-Z and also contain Arabic books,Hebrew books and books in other language arranged by  the alphabet.

JsonParser.py  - class that read the json files as input and copy the subjects to text file.Each line in this file contains                     subject,bookTitle,and the link were the book exists.

HashTable.py   - class that reads the subjects file as input and analyse each line. 
	       - each line contain data such as bookTitle,link,and subject . this class contains functions to parse the line ,by separating the link,book title ,and term
	       - the term (subject) contains data by analysing the term with NLTK- natural language processing tools , that decide Vocabulary type and grammar analysing
			   - if the word is a Noun or Adverb,adjective,or verb - then function that creates the data structure connected to NLTK Function to decide were the word should be in RDF graph based on three.
			   - the three is (subject,predicate,object) if word type is class or subClass or predicate to build the ontology.
			   - contains functions to find the relation between terms using edit distance algorithm.
			   - contains function for text cleaning .
				 
rdfOntology.py - class that depends on RDFLib models to build and store data into rdfFile as output .

OWL.py         - class that contains W3School models for ontology.
