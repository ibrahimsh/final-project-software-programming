__author__ = 'MatrixRev'
import codecs
import json
import re
from collections import Mapping
from collections import defaultdict
from collections import Counter
import Levenshtein
import nltk
from nltk.corpus import stopwords
import fileinput
import string
import os

import collections
import rdflib
from rdflib.namespace import OWL, RDF, RDFS,DC,FOAF
from rdflib import Graph, Literal, Namespace, URIRef,BNode
from rdflib.plugins.memory import IOMemory
from rdflib.graph import Graph, ConjunctiveGraph
from rdflib import plugin
from tempfile import mkdtemp
from rdflib.store import Store, NO_STORE, VALID_STORE


filename='C:\\Users\\MatrixRev\\Desktop\\books\\output\\subjects.txt' # the input file
output='C:\\Users\\MatrixRev\\Desktop\\books\\output\\dictionnary.json'
filePath='C:\\Users\\MatrixRev\\Desktop\\books\\output\\foaf.rdf'
termfile='C:\\Users\\MatrixRev\\Desktop\\books\\output\\allTerms.txt'
out2='C:\\Users\\MatrixRev\\Desktop\\books\\output\\newprint.txt'
class HashTable():

    def __init__(self):
        self.allTerms={}

        self.symbols={ '**a':'Personal name','**sub':'subString',
                       '**period':'period',
                         '**location':'location','**date':'date',
                         '**b':'Numeration',
                         '**c':'Titles and other words associated with a name',
                         '**e':'Relator term',
                         '**f':'Date of a work',
                         '**g':'Miscellaneous information',
                         '**h':'Medium A media qualifier.',
                         '**j':'Attribution qualifier',
                         #Attribution information for names when the responsibility is unknown, uncertain, fictitious, or pseudonymous.
                         '**k':'Form subheading',
                         #'**l':'Language of a work (NR)',
                         '**m':'Medium of performance for music',
                         '**n':'Number of part/section of a work',
                         '**o':'Arranged statement for music',
                         #'**p':'Name of part/section of a work (R)',
                         '**q':'Fuller form of name',
                         '**r':'Key for music',
                         #'**s':'Version (NR)',
                         '**t':'Title of a work',
                         '**u':'Affiliation',
                         '**v':'Form subdivision',
                         '**x':'General subdivision',
                         '**y':'Chronological subdivision',
                         '**z':'Geographic subdivision',
                         '**0':'Authority record control number or standard number',
                        #See description of this subfield in Appendix A: Control Subfields.
                         '**2':'Source of heading or term',
                        #Code from: Subject Heading and Term Source Codes.
                         '**3':'Materials specified',
                         '**4':'Relator code',
                         '**6':'Linkage',
                        #See description of this subfield in Appendix A: Control Subfields.
                         '**8':'Field link and sequence number',
                         '=':'isA'}

        sym_keys=self.symbols.keys()
        value=self.symbols.values()



    def Relation(self):
            return ({"@bookTitle":[],
                     "relation":[],
                     "objects":[],
                     "subClass":[],
                     "semilarTerms":[],
                     "@link":[],
                     "listOFWords":[]})


    def fill_Terms(self,sub):
        terms=self.Relation()
        allterm=self.allTerms
        subStr=""
        if sub.find("***link"):
            terms['@link'].append((self.setLink(sub).strip(" ")))
        newIndex=sub.index("***link")
        sub=sub[:newIndex]
        if sub.rfind("***title"):
            terms['@bookTitle'].append('@'+self.setTitle(sub).strip(" "))
        newIndex=sub.index("***title")
        subStr=sub[:newIndex]
        #print("all sub str:",subStr)
        if self.find_relation(subStr)==True:
            for k,v in self.termValue(subStr).items():
                 terms.setdefault("relation",[]).append((k,v))

            minStr=self.CompTermKey(subStr)
            #print("the sub string is:",minStr)
            if minStr.find('(')!=-1 and minStr.find(')')!=-1:
                print("yest find para",self.if_FindParanthesis(minStr))
                terms["relation"].append(self.getParanthises(minStr))
                insidePara=self.inside_Paranthises(minStr)
                #print("insidePrara",insidePara)
                if self.if_compoTerm(insidePara)==True:
                   terms['listOFWords'].append(self.splitTerms(insidePara))
                if self.check_If_Comma(insidePara)==True:
                    listOfobjects= self.findComma(insidePara)
                    i=len(listOfobjects)-1
                    print("i",i)
                    cls=listOfobjects[i]
                    terms["objects"].append(cls)
                    for c in range(0,i):
                     subClass=listOfobjects[c]
                     terms["subClass"].append(subClass)
                    for k in range(0,len(listOfobjects)):
                        minStr=listOfobjects[k]
                        minStr=minStr.strip(" ")
                        if self.check_terms(minStr)==True:
                            allterm[minStr]=self.updateTerm(minStr,terms)
                        elif self.check_terms(minStr)==False:
                            allterm[minStr]=terms
                else:
                    minStr=insidePara
                    minStr=minStr.strip(" ")
                    if self.check_terms(minStr)==True:
                        allterm[minStr]=self.updateTerm(minStr,terms)
                    elif self.check_terms(minStr)==True:
                        allterm[minStr]=terms
            elif self.check_If_Comma(minStr)==True:
                listOfobjects= self.findComma(minStr)
                i= len(listOfobjects)-1
                print("listofbjects is :",listOfobjects[i])
                cls=listOfobjects[i]
                terms['objects'].append(cls)
                for c in range(0,i):
                    subClass=listOfobjects[c]
                    terms["subClass"].append(subClass)
                for t in range(0,len(listOfobjects)):
                    minStr=listOfobjects[t]
                    minStr=minStr.strip(" ")
                    if self.check_terms(minStr)==True:
                     #allterm[minStr].update(terms)
                      allterm[minStr]=self.updateTerm(minStr,terms)
                    elif self.check_terms(minStr)==False:
                      allterm[minStr]=terms
            else:
                if self.if_compoTerm(minStr)==True:
                   terms['listOFWords'].append(self.splitTerms(minStr))
                minStr=minStr.strip(" ")
                #minStr=minStr.lower()
                if self.check_terms(minStr)==True:
                   allterm[minStr]=self.updateTerm(minStr,terms)
                elif self.check_terms(minStr)==False:
                    allterm[minStr]=terms

        elif self.find_relation(subStr)==False:
            #subStr=subStr.lower()

            if subStr.find('(')!=-1 and subStr.find(')')!=-1:
                terms["relation"].append(self.getParanthises(subStr))
                insidePara=self.inside_Paranthises(subStr)
                #print("insidePrara",insidePara)
                if self.if_compoTerm(insidePara)==True:
                    terms['listOFWords'].append(self.splitTerms(insidePara))
                if self.check_If_Comma(insidePara)==True:
                    listOfobjects= self.findComma(insidePara)
                    i= len(listOfobjects)-1
                    cls=listOfobjects[i]
                    terms["objects"].append(cls)
                    for c in range(0,i):
                        subClass=listOfobjects[c]
                        terms["subClass"].append(subClass)
                    for t in range(0,len(listOfobjects)):
                        mterm=listOfobjects[t]

                        if self.check_terms(mterm)==True:
                            allterm[mterm]=self.updateTerm(mterm,terms)
                        elif self.check_terms(mterm)==False:
                            allterm[mterm]=terms
                else:
                    insidePara=insidePara.strip('')
                    #insidePara=insidePara.lower()
                    if self.check_terms(insidePara)==True:
                        allterm[insidePara]=self.updateTerm(insidePara,terms)
                        #print("after update",terms)
                    elif self.check_terms(insidePara)==False:
                        allterm[insidePara]=terms
                    if self.if_compoTerm(insidePara)==True:
                        terms['listOFWords'].append(self.splitTerms(insidePara))
            elif self.check_If_Comma(subStr)==True:
                #subStr=subStr.strip(" ")
                #subStr=subStr.lower()
                listOfobjects= self.findComma(subStr)
                i= len(listOfobjects)-1
                cls=listOfobjects[i]
                terms["objects"].append(cls)
                for c in range(0,i):
                    subClass=listOfobjects[c]
                    terms["subClass"].append(subClass)
                for e in range(0,len(listOfobjects)):
                    tterm=listOfobjects[e]
                    #tterm=tterm.strip(" ")
                 #   tterm=tterm.lower()
                    if self.check_terms(tterm)==True:
                        allterm[tterm]=self.updateTerm(tterm,terms)
                    elif self.check_terms(tterm)==False:
                        allterm[tterm]=terms
            else:
                #subStr=subStr.strip(" ")
                #subStr=subStr.lower()
                if self.if_compoTerm(subStr)==True:
                   terms['listOFWords'].append(self.splitTerms(subStr))
                if self.check_terms(subStr)==True:
                   allterm[subStr]=self.updateTerm(subStr,terms)
                elif self.check_terms(subStr)==False:
                    allterm[subStr]=terms
        else:
            #subStr=subStr.strip('')
            #subStr=subStr.lower()
            if self.if_compoTerm(subStr)==True:
                terms['listOFWords'].append(self.splitTerms(subStr))
            if self.check_terms(subStr)==True:
              allterm[subStr]=self.updateTerm(subStr,terms)
            elif self.check_terms(subStr)==False:
              allterm[subStr]=terms

        return allterm

    def updateTerm(self,term,rvalue):
        tvalue=self.allTerms[term]

        for key in tvalue.keys():
            for k in rvalue.keys():
                if key == k:
                    if key is 'listOFWords':
                        break
                    else:
                        for i in rvalue[k]:
                            if  i in tvalue[key]:
                                break
                            else:
                                tvalue[key].append(i)


        return tvalue

    def similarTerms(self,target):
        the_same=[]
        counter=0
        with codecs.open(termfile,'rb',encoding='utf-8')as tf:
            list_of_t=tf.readlines()
            for item in list_of_t:
              item=item.strip('\n')
              if  item!=target:
                if self.if_compoTerm(target):

                        List_target=self.splitTerms(target)
                        for t in List_target:

                            if item.find(t)!=-1:
                                 if item not in the_same:
                                     dist=Levenshtein.distance(item,target)
                                     print("the dist:",dist)
                                     if item!=target:
                                        the_same.append(item)

                            if Levenshtein.ratio(t,item)==0.8:
                                if item not in the_same:
                                    if re.fullmatch(item,target):
                                        the_same.append(item)

                #print("the ratio is ",the_ratio)

        #print("is",the_same)
        return the_same


    def setLink(self,subject):
        if subject.find("***link"):
            linkIndex=subject.index("***link")
            newIndex=linkIndex+len("***link")+1
            link=subject[newIndex:]
        return link

    def setTitle(self,sub):
        if sub.find("***title"):
            titleIndex=sub.index("***title")
            newIndex=len("***title")+titleIndex
            title=sub[newIndex:].strip(":")

        return title


    def find_relation(self, subjects):
        #print("relation is check:",subjects)
        counter=0
        is_relation=True
        sub_len = len(subjects)
        for key in self.symbols.keys():
            if subjects.rfind(key)!=-1:
                counter=counter+1

        if counter>0:
            print(counter)
            is_relation=True
        else:
            is_relation=False
        print("if the relation",is_relation)
        return is_relation


    def termValue(self,subject):
        #longVal={}
        if subject.find('etc')!=-1or subject.rfind(',etc.')!=-1 or subject.rfind(',etc')!=-1:
            subject=subject.replace('etc.',' ')
            subject=subject.replace(',etc.',' ')
            subject=subject.strip('etc')
        if subject.find('*')!=-1:
            sindex=subject.index('*')
            nsubject=subject[sindex:]
            list_of_values=list(nsubject.split('*'))
            longVal={}
            for i in list_of_values:
                if i=='':
                 list_of_values.remove(i)
            for key in self.symbols.keys():

                for sym in list_of_values:
                    sym='**'+sym
                    if sym.find(key)!=-1:
                        sym_index=sym.index(key)
                        tofsym=len(key)+sym_index
                        nsym=sym[tofsym:].strip(':').strip(' ')
                        longVal.setdefault(self.symbols[key],[]).append(nsym)




        return longVal

    def findComma(self,sub):
        newSub=[]
        if sub.find(',')!=-1:
            for s in sub.split(','):
                newSub.append(s)

        return newSub


    def getParanthises(self,sub):

       # regex = re.compile('('+')')
        longVal=collections.defaultdict(list)

        if sub.find('(')!=-1 and sub.find(')')!=-1:
            termValue=sub.strip('-')
            termValue=termValue.strip(' ')
           # print("the last char ",termValue[len(termValue)-1])
            #print("term length",len(termValue))
            #print(termValue)
            tindex=termValue.index('(')

            print("the (",tindex)
            eindex=termValue.index(')')
            print("the )",eindex)
            if eindex>tindex and eindex<len(termValue)-1:
                nValue=termValue[eindex+1:]

                longVal.setdefault('aspect_of',[]).append(nValue)
            elif tindex>eindex and tindex<len(termValue)-1:
                nValue=termValue[tindex+1:]
                #longVal.append({"aspect_of":nValue})
                longVal.setdefault('aspect_of',[]).append(nValue)
            elif eindex==len(termValue)-1and tindex<eindex:
                nValue=termValue[:tindex-1]
                #longVal.append({"aspect_of":nValue})
                longVal.setdefault('aspect_of',[]).append(nValue)
            elif tindex==len(termValue)-1and tindex>eindex:
                nValue=termValue[:eindex-1]
               # longVal.append({"aspect_of ":nValue})
                longVal.setdefault('aspect_of',[]).append(nValue)
        return longVal

    def inside_Paranthises(self,sub):
        term=""
        if sub.rfind('(')!=-1 and sub.rfind(')')!=-1:
            s=sub.index('(')
            f=sub.index(')')
            print("start",s,"end with",f)
            if s>f:

                term=sub[f:s]
                term=term.strip(")/(")
            elif s<f:

                term=sub[s:f]
                term=term.strip(")/(")
        return term
    '''
    def CompTermKey(self,sub):
        NumOfKeys=0
        term=""
        counter=0
        #regex = re.compile('('+')')
        kindex=[]
        if sub.find('***Title')!=-1:
         title_index=sub.index('***Title')
         sub=sub[:title_index]

        for key in self.symbols.keys():
            if sub.find(key)!=-1:
                key_length=len(key)
                key_index=sub.index(key)
                kindex.append(key_index)
                counter=counter+1
                print('the key',key_index)

        if len(kindex)>0:
            for i in range(len(kindex)):
              min=kindex[0]
            if kindex[i]<min:
              min=kindex[i]
            if min >0:
             term=sub[:min]


        return term
    '''
    def CompTermKey(self,sub):
        t=''
        tindex=0
        if sub.find('*')!=-1:
            tindex=sub.index('*')
            t=sub[:tindex]
        return  t
    def if_FindParanthesis(self,sub):
        #regex = re.compile('('+')')
        yes=True
        if sub.find('(')and sub.find(')'):
            yes= True
        else:
            yes=False
        return yes
    def check_If_Comma(self,subject):
        if subject.find(",")!=-1:
            return True
        else:
            return False

    def check_terms(self,term):
        existTerm= True
        if term in self.allTerms.keys():
            existTerm=True
        else:
            existTerm=False
        return existTerm
    def check_value(self,val):
        if val in self.terms.values():
            return False
        else:
            return True
    def if_compoTerm(self,sub):
        arr=sub.split()
        counter=0
        for a in arr:
            counter=counter+1
        if counter>1:
            return True
        else:
            return False
    def splitTerms(self,subString):
        allWords=[]
        for world in subString.split(' '):
            allWords.append(world)
        return (allWords)
    def printTerms(self,output):
        with codecs.open(output,'w',encoding='utf-8')as outfile:
            for item in self.allTerms.items():
                #print("term:",k,outfile)
                json.dump(item,outfile,ensure_ascii=False,indent=4)

       # return self.terms
    #def Find_similarity(self,source,target):


    def num_there(self,txt):
        counter=0
        for c in txt:
            if c.isdigit():
                counter=counter+1
        if counter>=1:
            return True
        else:
            return False
    def create_ontology(self,tr,predicate,subClass,address,booktitle):
        LDT= Namespace("http://www.JceFinalProjectOntology.com/")
        ut=Namespace("http://www.JceFinalProjectOntology.com/subject/#")
        usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+subClass.strip()+'#')
        #LDT.subClass=LDT[subClass]
        print(ut)
        print(usubClass)

        store=IOMemory()

        sty=LDT[predicate]
        g = rdflib.Graph(store=store,identifier=LDT)
        t = ConjunctiveGraph(store=store,identifier=ut)
        print ('Triples in graph before add: ', len(t))
        #g.add((LDT,RDF.type,RDFS.Class))
        g.add((URIRef(LDT),RDF.type,RDFS.Class))
        g.add((URIRef(LDT),RDFS.label,Literal("JFPO")))
        g.add((URIRef(LDT),RDFS.comment,Literal('class of all properties')))
        for  v in self.symbols.values():
            if self.if_compoTerm(v)==True:
                vs=self.splitTerms(v)[0]
            else:
                vs =v
            g.add((LDT[vs],RDF.type,RDF.Property))
            g.add((LDT[vs],RDFS.label,Literal('has'+vs)))
            g.add((LDT[vs],RDFS.comment,Literal(v)))
            g.add((LDT[vs],RDFS.range,OWL.Class))
            g.add((LDT[vs],RDFS.domain,Literal(vs)))
        g.bind('JFPO',LDT)
        #g.commit()
        g.serialize('trtst.rdf',format='turtle')

        t.add( (ut[tr], RDF.type,OWL.Class) )
        t.add((ut[tr],RDFS.subClassOf,OWL.Thing))
        t.add((ut[tr],RDFS.label,Literal(tr)))
        t.add((ut[tr],DC.title,Literal(booktitle)))
        t.add((ut[tr],DC.source,Literal(address)))

        t.add((ut[tr],DC[predicate],URIRef(usubClass)))
        t.add((ut[tr],LDT[predicate],RDF.Property))

        t.add((ut[tr],DC[predicate],URIRef(usubClass)))

        t.add((ut[tr],DC[predicate],URIRef(usubClass)))
        relation='has'+predicate
        t.add((ut[tr],LDT.term(predicate),URIRef(usubClass)))

        t.add( (usubClass,RDF.type,OWL.Class))
        t.add((usubClass,RDFS.subClassOf,OWL.Thing))
        t.add((usubClass,RDFS.subClassOf,URIRef(sty)))
        t.add((usubClass,RDFS.label,Literal(subClass)))

        #tc=Graph(store=store,identifier=usubClass)
        t.bind("dc", "http://http://purl.org/dc/elements/1.1/")
        t.bind('JFPO',LDT)
        t.commit()
                #print(t.serialize(format='pretty-xml'))

        t.serialize('test2.owl',format='turtle')

'''
ald=Levenshtein.editops("science computer","computer science")
print(ald)
edit=Levenshtein.distance("computer science","computer science")
dist=Levenshtein.apply_edit(ald,"science computer","computer science")
print(dist)
print(edit)
'''
table=HashTable()

rdf=table.create_ontology('naturalTresure','location','amman','bokAddr','/t/welcm.json') # function to create ontology
print(rdf)

'''
with codecs.open(output,'w',encoding='utf-8')as outfile:
        for k,v in table.allTerms.items():
            #if len(k) !=0:
                    #melon["item"]=list(k)
                #melon["Relation"]=list(v)
                json.dump({"item":k,"subClasses":v},outfile,ensure_ascii=False,indent=4)
                #json.dump(melon,outfile,ensure_ascii=False,indent=4)
''''''
with codecs.open(os.path.join(filePath,"allTerms.txt"),'w',encoding='utf-8')as termFile:
    list_of_terms= table.allTerms.keys()
    for k in list_of_terms:
        print(k,'\n',file=termFile)
with codecs.open(os.path.join(filePath,"value.json"),'w',encoding='utf-8')as valueFile:
    list_of_values=table.allTerms.values()
    for v in list_of_values:
        json.dump(v,valueFile,ensure_ascii=False,indent=4)
'''
