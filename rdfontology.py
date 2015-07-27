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
from HashTable import HashTable
filename='C:\\Users\\MatrixRev\\Desktop\\books\\output\\subjects.txt' # input file
#output is rdf file created in the same directory of the code 
table=HashTable()
def nltk_analyzer(tr):

                    #NLTK subjects
                    structure=dict()
                    if table.if_compoTerm(tr)==True:
                        sentence1=tr.split()
                        print(sentence1)
                        tokens=nltk.word_tokenize(tr)
                        tag=nltk.pos_tag(sentence1)
                        d=dict(tag[0:6])
                        term=''
                        subclass=[]
                        mainCls=[]
                        cls_counter=0
                        jcount=0
                        secondCls=''
                        startw=sentence1[0]
                        print('start with'+startw)
                        if d[startw]=='JJ' or d[startw]=='JJR':

                            subclass.append(startw)

                            for i in range(1,len(sentence1)):
                                if d[sentence1[i]]=='JJ' or d[sentence1[i]]=='JJR':
                                    subclass.append(sentence1[i])
                                if d[sentence1[i]] == 'NN' or d[sentence1[i]]=='NNS':
                                    cls_counter=cls_counter+1
                                    if cls_counter>0:
                                        mainCls.append(sentence1[i])
                                if d[sentence1[i]]=='VBG' and d[sentence1[i-1]]=='NN'or d[sentence1[i-1]]=='NNS':
                                    mainCls.append(sentence1[i-1]+"_"+sentence1[i])
                            if cls_counter>1:
                                for s in mainCls:
                                    for sub in subclass:
                                        #print(cls[j]+" "+"hasSubClass"+" "+sub)
                                       structure[s]=sub
                            else:
                                for s in mainCls:
                                    for b in subclass:
                                       structure[s]=b

                        if d[startw]=='NN' or d[startw]=='NNS':
                            secondCls=startw
                            for i in range(1,len(sentence1)):
                                if d[sentence1[i]] == 'NN' or d[sentence1[i]]=='NNS':
                                    cls_counter=cls_counter+1
                                    if cls_counter>0:
                                        mainCls.append(sentence1[i])
                                if d[sentence1[i]]=='VBG' and d[sentence1[i-1]]=='NN'or d[sentence1[i-1]]=='NNS':
                                    mainCls.append(sentence1[i-1]+"_"+sentence1[i])
                            #print(cls+':'+'hasSubclass'+":"+secondCls)
                            #print(secondCls+":"+'is class too ')
                        for ms in mainCls:
                            structure[ms]=secondCls
                        return structure


subClass=''
LDT= Namespace("http://www.JceFinalProjectOntology.com/")
ut=Namespace(u"http://www.JceFinalProjectOntology.com/subject/")
usubClass=Namespace(u"http://www.JceFinalProjectOntology.com/subject/subclasses/")
store=IOMemory()
t = ConjunctiveGraph(store=store)
        #t.serialize('test2.owl',format='pretty-xml')
counter=0
booktitle=''
tr=''
address=''
predicate=''

#g = ConjunctiveGraph(store=store,identifier=LDT)



t.add((URIRef(LDT),RDF.type,RDFS.Class))
t.add((URIRef(LDT),RDFS.label,Literal("JFPO")))
t.add((URIRef(LDT),RDFS.comment,Literal('class of all properties')))
counter=0
with codecs.open(filename,'rb',encoding='utf-8')as fh:
    for line in fh:
        counter=counter+1
       # print(line,"is counter:",counter)
        line=str(line)
        line=line.replace(',etc.',' ')
        line=line.replace('etc',' ')
        line=line.strip('\n')
        line=line.strip(' ')

        if line.find("***link"):
           address= table.setLink(line).strip(" ")
        newIndex=line.index("***link")
        sub=line[:newIndex]
        if sub.rfind("***title"):
           booktitle= table.setTitle(sub).strip(" ")
        newIndex=sub.index("***title")
        subStr=sub[:newIndex]
        #print("all sub str:",subStr)
        if len(subStr)>0:
            if table.find_relation(subStr)==True:

                 minStr=table.CompTermKey(subStr)
                 minStr=minStr.strip(' ')
                 #minStr=re.sub('[^a-zA-Z0-9\n\.]',' ',minStr)
                 if len(minStr)>0:
                    if minStr.find('(')!=-1 and minStr.find(')')!=-1:
                        print("yest find para",table.if_FindParanthesis(minStr))
                        insidePara=table.inside_Paranthises(minStr)

                        if table.check_If_Comma(insidePara)==True:
                            listOfobjects= table.findComma(insidePara)
                            i=len(listOfobjects)-1
                            print("i",i)
                            cls=listOfobjects[i]
                            cls=str(cls)
                            tr=cls
                            tr=re.sub('[^a-zA-Z0-9\n\.]',' ',tr)

                            #tr=tr.replace(' ','_')
                            if table.if_compoTerm(tr)==True:
                                print('true')
                                for  term,sub in nltk_analyzer(tr).items():
                                    term=re.sub('[^a-zA-Z0-9\n\.]','',term)
                                    t.add( (ut[term], RDF.type,OWL.Class) )
                                    t.add((ut[term],RDFS.subClassOf,OWL.Thing))
                                    t.add((ut[term],RDFS.label,Literal(term)))
                                    t.add((ut[term],DC.title,Literal(booktitle)))
                                    t.add((ut[term],DC.source,Literal(address)))
                                    t.add((usubClass[sub],RDF.type,OWL.Class))
                                    t.add((usubClass[sub],RDFS.subClassOf,ut[term]))
                                    t.add((usubClass[sub],RDFS.label,Literal(sub)))
                                    t.add((usubClass[sub],DC.title,Literal(booktitle)))
                                    t.add((usubClass[sub],DC.source,Literal(address)))

                                    for key,value in table.termValue(subStr).items():
                                        key=str(key)
                                        #key=key.replace(' ','_')
                                        key=re.sub('[^a-zA-Z0-9\n\.]',' ',key)

                                        rel=''
                                        if table.if_compoTerm(key)==True:
                                            rel=table.splitTerms(key)[0]
                                        else:
                                            rel =key

                                        t.add((URIRef(LDT[rel]),RDF.type,RDF.Property))
                                        t.add((LDT[rel],RDFS.label,Literal('has'+rel)))
                                        t.add((LDT[rel],RDFS.comment,Literal(key)))
                                        t.add((LDT[rel],RDFS.domain,URIRef(LDT)))

                                        t.add((LDT[rel],RDFS.range,ut[term]))

                                        predicate='has'+rel
                                        value=str(value)
                                        value=re.sub('[^a-zA-Z0-9\n\.]',' ',value)
                                        if table.if_compoTerm(value)==True:
                                            #if table.check_If_Comma(value)==True:
                                            values=value.split()
                                            for v in values:
                                                v=re.sub('[^a-zA-Z0-9\n\.]','',v)
                                                #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+v)

                                                t.add((ut[term],LDT[predicate],URIRef(usubClass)))
                                                t.add((usubClass[v],RDF.type,LDT[predicate]))
                                        else:
                                            value=re.sub('[^a-zA-Z0-9\n\.]','',value)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+value)

                                            t.add((ut[term],LDT[predicate],URIRef(usubClass[value])))
                                            #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                            #t.add((LDT[predicate],OWL.hasValue,usubClass))
                                            t.add((URIRef(usubClass[value]),RDF.type,LDT[predicate]))

                                    for key,value in table.getParanthises(minStr).items():
                                        key=str(key)
                                        key=re.sub('[^a-zA-Z0-9\n\.]',' ',key)
                                        #predicate='has'+key
                                        value=str(value)
                                        #value=value.strip(' ')
                                        value=re.sub('[^a-zA-Z0-9\n\.]',' ',value)
                                        rel=''
                                        if table.if_compoTerm(key)==True:
                                            rel=table.splitTerms(key)[0]
                                        else:
                                            rel =key

                                        t.add((LDT[rel],RDF.type,RDF.Property))
                                        t.add((LDT[rel],RDFS.label,Literal('has'+rel)))
                                        t.add((LDT[rel],RDFS.comment,Literal(rel)))
                                        t.add((LDT[rel],RDFS.domain,URIRef(LDT)))

                                        t.add((LDT[rel],RDFS.range,URIRef(ut[term])))

                                        predicate='has'+rel
                                        if table.if_compoTerm(value)==True:
                                            #if table.check_If_Comma(value)==True:
                                            values=value.split()
                                            for v in values:
                                                v=re.sub('[^a-zA-Z0-9\n\.]','',v)
                                                #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+v)

                                                t.add((ut[term],LDT[predicate],URIRef(usubClass[v])))
                                                #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                                t.add((URIRef(usubClass[v]),RDF.type,LDT[predicate]))
                                                #t.add((LDT[predicate],OWL.hasValue,usubClass))
                                        else:
                                            value=re.sub('[^a-zA-Z0-9\n\.]','',value)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+value)

                                            t.add((ut[term],LDT[predicate],URIRef(usubClass[value])))
                                            #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                            t.add((URIRef(usubClass),RDF.type,LDT[predicate]))
                                            #t.add((LDT[predicate],OWL.hasValue,usubClass))
                                    for c in range(0,i):
                                        subClass=listOfobjects[c]
                                        subClass=str(subClass)
                                        subClass=subClass.strip(' ')
                                        subClass=re.sub('[^a-zA-Z0-9\n\.]',' ',subClass)
                                        if table.if_compoTerm(subClass)==True:
                                            subClasses=subClass.split()
                                            for s in subClasses:
                                                s=re.sub('[^a-zA-Z0-9\n\.]','',s)
                                                #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+s)

                                                t.add((ut[term],DC.hasPart,URIRef(usubClass[s])))
                                                #t.add((URIRef(usubClass),RDFS.SubclassOf,ut[tr]))
                                                t.add((URIRef(usubClass[s]),RDFS.subClassOf,ut[term]))
                                                t.add((usubClass[s],RDF.type,OWL.Class))
                                                t.add((usubClass[s],RDFS.label,Literal(s)))
                                                t.add((usubClass[s],DC.title,Literal(booktitle)))
                                                t.add((usubClass[s],DC.source,Literal(address)))
                                        else:
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+subClass)

                                            t.add((ut[term],DC.hasPart,URIRef(usubClass[subClass])))
                                            t.add((URIRef(usubClass[subClass]),RDFS.subClassOf,ut[term]))
                                            t.add( (URIRef(usubClass[subClass]),RDF.type,OWL.Class))
                                            t.add((URIRef(usubClass[subClass]),RDFS.label,Literal(subClass)))
                                            t.add((URIRef(usubClass[subClass]),DC.title,Literal(booktitle)))
                                            t.add((URIRef(usubClass[subClass]),DC.source,Literal(address)))
                            elif table.if_compoTerm(tr)==False:
                                    tr=re.sub('[^a-zA-Z0-9\n\.]','',tr)
                                    t.add( (ut[tr], RDF.type,OWL.Class) )
                                    t.add((ut[tr],RDFS.subClassOf,OWL.Thing))
                                    t.add((ut[tr],RDFS.label,Literal(tr)))
                                    t.add((ut[tr],DC.title,Literal(booktitle)))
                                    t.add((ut[tr],DC.source,Literal(address)))


                                    for key,value in table.termValue(subStr).items():
                                        key=str(key)
                                        #key=key.replace(' ','_')
                                        key=re.sub('[^a-zA-Z0-9\n\.]',' ',key)

                                        rel=''
                                        if table.if_compoTerm(key)==True:
                                            rel=table.splitTerms(key)[0]
                                        else:
                                            rel =key

                                        t.add((URIRef(LDT[rel]),RDF.type,RDF.Property))
                                        t.add((LDT[rel],RDFS.label,Literal('has'+rel)))
                                        t.add((LDT[rel],RDFS.comment,Literal(key)))
                                        t.add((LDT[rel],RDFS.domain,URIRef(LDT)))

                                        t.add((LDT[rel],RDFS.range,ut[tr]))

                                        predicate='has'+rel
                                        value=str(value)
                                        value=re.sub('[^a-zA-Z0-9\n\.]',' ',value)
                                        if table.if_compoTerm(value)==True:
                                            #if table.check_If_Comma(value)==True:
                                            values=value.split()
                                            for v in values:
                                                v=re.sub('[^a-zA-Z0-9\n\.]','',v)
                                                #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+v)

                                                t.add((ut[tr],LDT[predicate],URIRef(usubClass[v])))
                                                t.add((URIRef(usubClass[v]),RDF.type,LDT[predicate]))
                                        else:
                                            value=re.sub('[^a-zA-Z0-9\n\.]','',value)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+value)

                                            t.add((ut[tr],LDT[predicate],URIRef(usubClass[value])))
                                            #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                            #t.add((LDT[predicate],OWL.hasValue,usubClass))
                                            t.add((URIRef(usubClass[value]),RDF.type,LDT[predicate]))

                                    for key,value in table.getParanthises(minStr).items():
                                        key=str(key)
                                        key=re.sub('[^a-zA-Z0-9\n\.]',' ',key)
                                        #predicate='has'+key
                                        value=str(value)
                                        #value=value.strip(' ')
                                        value=re.sub('[^a-zA-Z0-9\n\.]',' ',value)
                                        rel=''
                                        if table.if_compoTerm(key)==True:
                                            rel=table.splitTerms(key)[0]
                                        else:
                                            rel =key

                                        t.add((LDT[rel],RDF.type,RDF.Property))
                                        t.add((LDT[rel],RDFS.label,Literal('has'+rel)))
                                        t.add((LDT[rel],RDFS.comment,Literal(rel)))
                                        t.add((LDT[rel],RDFS.domain,URIRef(LDT)))

                                        t.add((LDT[rel],RDFS.range,URIRef(ut[tr])))

                                        predicate='has'+rel
                                        if table.if_compoTerm(value)==True:
                                            #if table.check_If_Comma(value)==True:
                                            values=value.split()
                                            for v in values:
                                                v=re.sub('[^a-zA-Z0-9\n\.]','',v)
                                                #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+v)

                                                t.add((ut[tr],LDT[predicate],URIRef(usubClass[v])))
                                                #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                                t.add((URIRef(usubClass[v]),RDF.type,LDT[predicate]))
                                                #t.add((LDT[predicate],OWL.hasValue,usubClass))
                                        else:
                                            value=re.sub('[^a-zA-Z0-9\n\.]','',value)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+value)

                                            t.add((ut[tr],LDT[predicate],URIRef(usubClass[value])))
                                            #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                            t.add((URIRef(usubClass[value]),RDF.type,LDT[predicate]))
                                            #t.add((LDT[predicate],OWL.hasValue,usubClass))
                                    for c in range(0,i):
                                        subClass=listOfobjects[c]
                                        subClass=str(subClass)
                                        subClass=subClass.strip(' ')
                                        subClass=re.sub('[^a-zA-Z0-9\n\.]',' ',subClass)
                                        if table.if_compoTerm(subClass)==True:
                                            subClasses=subClass.split()
                                            for s in subClasses:
                                                s=re.sub('[^a-zA-Z0-9\n\.]','',s)
                                                #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+s)

                                                t.add((ut[tr],DC.hasPart,URIRef(usubClass[s])))
                                                #t.add((URIRef(usubClass),RDFS.SubclassOf,ut[tr]))
                                                t.add((URIRef(usubClass[s]),RDFS.subClassOf,ut[tr]))
                                                t.add((usubClass[s],RDF.type,OWL.Class))
                                                t.add((usubClass[s],RDFS.label,Literal(s)))
                                                t.add((usubClass[s],DC.title,Literal(booktitle)))
                                                t.add((usubClass[s],DC.source,Literal(address)))
                                        else:
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+subClass)

                                            t.add((ut[tr],DC.hasPart,URIRef(usubClass[subClass])))
                                            t.add((URIRef(usubClass[subClass]),RDFS.subClassOf,ut[tr]))
                                            t.add( (URIRef(usubClass[subClass]),RDF.type,OWL.Class))
                                            t.add((URIRef(usubClass[subClass]),RDFS.label,Literal(subClass)))
                                            t.add((URIRef(usubClass[subClass]),DC.title,Literal(booktitle)))
                                            t.add((URIRef(usubClass[subClass]),DC.source,Literal(address)))
                            ###############################################################################################
                        else:
                            minStr=insidePara
                            #minStr=minStr.strip(" ")
                            minStr=re.sub('[^a-zA-Z0-9\n\.]',' ',minStr)
                            tr=minStr
                            if table.if_compoTerm(tr)==True:
                                for sterm,subs in nltk_analyzer(tr).items():
                                    sterm=re.sub('[^a-zA-Z0-9\n\.]','',sterm)
                                    t.add((ut[sterm], RDF.type,OWL.Class) )
                                    t.add((ut[sterm],RDFS.subClassOf,OWL.Thing))
                                    t.add((ut[sterm],RDFS.label,Literal(sterm)))
                                    t.add((ut[sterm],DC.title,Literal(booktitle)))
                                    t.add((ut[sterm],DC.source,Literal(address)))

                                    t.add((usubClass[subs], RDF.type,OWL.Class) )
                                    t.add((usubClass[subs],RDFS.subClassOf,ut[sterm]))
                                    t.add((usubClass[subs],RDFS.label,Literal(subs)))
                                    t.add((usubClass[subs],DC.title,Literal(booktitle)))
                                    t.add((usubClass[subs],DC.source,Literal(address)))
                                    for key,value in table.termValue(subStr).items():
                                        key=str(key)
                                        #key=key.replace(' ','_')
                                        key=re.sub('[^a-zA-Z0-9\n\.]',' ',key)
                                        #property=LDT[key]

                                        rel=''
                                        if table.if_compoTerm(key)==True:
                                            rel=table.splitTerms(key)[0]
                                        else:
                                            rel =key

                                        t.add((LDT[rel],RDF.type,RDF.Property))
                                        t.add((LDT[rel],RDFS.label,Literal('has'+rel)))
                                        t.add((LDT[rel],RDFS.comment,Literal(key)))
                                        t.add((LDT[rel],RDFS.domain,URIRef(LDT)))
                                        t.add((LDT[rel],RDFS.range,ut[sterm]))

                                        predicate='has'+rel


                                        value=str(value)
                                        value=re.sub('[^a-zA-Z0-9\n\.]',' ',value)

                                    if table.if_compoTerm(value)==True:
                                        #if table.check_If_Comma(value)==True:
                                        values=value.split()
                                        for v in values:
                                            v=re.sub('[^a-zA-Z0-9\n\.]','',v)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+v)
                                            t.add((ut[sterm],LDT[predicate],URIRef(usubClass[v])))
                                            #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                            t.add((URIRef(usubClass[v]),RDF.type,LDT[predicate]))
                                            #t.add((LDT[predicate],OWL.hasValue,usubClass))

                                    else:
                                        value=re.sub('[^a-zA-Z0-9\n\.]','',value)
                                        #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+value)
                                        t.add((ut[sterm],LDT[predicate],URIRef(usubClass[value])))
                                        #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                        t.add((URIRef(usubClass),RDF.type,LDT[predicate]))
                                        #t.add((LDT[predicate],OWL.hasValue,usubClass))
                            elif table.if_compoTerm(tr)==False:
                                tr=re.sub('[^a-zA-Z0-9\n\.]','',tr)
                                t.add((ut[tr], RDF.type,OWL.Class) )
                                t.add((ut[tr],RDFS.subClassOf,OWL.Thing))
                                t.add((ut[tr],RDFS.label,Literal(tr)))
                                t.add((ut[tr],DC.title,Literal(booktitle)))
                                t.add((ut[tr],DC.source,Literal(address)))
                                for key,value in table.termValue(subStr).items():
                                    key=str(key)
                                    #key=key.replace(' ','_')
                                    key=re.sub('[^a-zA-Z0-9\n\.]',' ',key)
                                    #property=LDT[key]

                                    rel=''
                                    if table.if_compoTerm(key)==True:
                                        rel=table.splitTerms(key)[0]
                                    else:
                                        rel =key

                                    t.add((LDT[rel],RDF.type,RDF.Property))
                                    t.add((LDT[rel],RDFS.label,Literal('has'+rel)))
                                    t.add((LDT[rel],RDFS.comment,Literal(key)))
                                    t.add((LDT[rel],RDFS.domain,URIRef(LDT)))
                                    t.add((LDT[rel],RDFS.range,ut[tr]))

                                    predicate='has'+rel


                                    value=str(value)
                                    value=re.sub('[^a-zA-Z0-9\n\.]',' ',value)

                                    if table.if_compoTerm(value)==True:
                                        #if table.check_If_Comma(value)==True:
                                        values=value.split()
                                        for v in values:
                                            v=re.sub('[^a-zA-Z0-9\n\.]','',v)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+v)
                                            t.add((ut[tr],LDT[predicate],URIRef(usubClass[v])))
                                            #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                            t.add((URIRef(usubClass[v]),RDF.type,LDT[predicate]))
                                            #t.add((LDT[predicate],OWL.hasValue,usubClass))

                                    else:
                                        value=re.sub('[^a-zA-Z0-9\n\.]','',value)
                                        #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+value)
                                        t.add((ut[tr],LDT[predicate],URIRef(usubClass[value])))
                                        #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                        t.add((URIRef(usubClass[value]),RDF.type,LDT[predicate]))
                                        #t.add((LDT[predicate],OWL.hasValue,usubClass))
                    #####################################################################################
                    elif table.check_If_Comma(minStr)==True:
                        listOfobjects= table.findComma(minStr)
                        i= len(listOfobjects)-1
                        print("listofbjects is :",listOfobjects[i])
                        cls=listOfobjects[i]
                        #terms['objects'].append(cls)
                        cls=str(cls)
                        #cls=cls.strip(' ')
                        cls=re.sub('[^a-zA-Z0-9\n\.]',' ', cls)
                        tr=cls
                        if table.if_compoTerm(tr)==True:
                            for terms,substring in nltk_analyzer(tr).items():
                                terms=re.sub('[^a-zA-Z0-9\n\.]','',terms)
                                t.add((ut[terms], RDF.type,OWL.Class) )
                                t.add((ut[terms],RDFS.subClassOf,OWL.Thing))
                                t.add((ut[terms],RDFS.label,Literal(terms)))
                                t.add((ut[terms],DC.title,Literal(booktitle)))
                                t.add((ut[terms],DC.source,Literal(address)))
                                substring=re.sub('[^a-zA-Z0-9\n\.]','',substring)
                                t.add( (usubClass[substring], RDF.type,OWL.Class) )
                                t.add((usubClass[substring],RDFS.subClassOf,ut[terms]))
                                t.add((usubClass[substring],RDFS.label,Literal(substring)))
                                t.add((usubClass[substring],DC.title,Literal(booktitle)))
                                t.add((usubClass[substring],DC.source,Literal(address)))
                                for key,value in table.termValue(subStr).items():
                                        key=str(key)
                                        key=re.sub('[^a-zA-Z0-9\n\.]',' ',key)
                                        #property=LDT[key]

                                        rel=''
                                        if table.if_compoTerm(key)==True:
                                            rel=table.splitTerms(key)[0]
                                        else:
                                            rel =key

                                        t.add((LDT[rel],RDF.type,RDF.Property))
                                        t.add((LDT[rel],RDFS.label,Literal('has'+rel)))
                                        t.add((LDT[rel],RDFS.comment,Literal(key)))
                                        t.add((LDT[rel],RDFS.domain,URIRef(LDT)))
                                        t.add((LDT[rel],RDFS.range,ut[terms]))

                                        predicate='has'+rel
                                        value=str(value)
                                        #value=v.strip(' ')
                                        value=re.sub('[^a-zA-Z0-9\n\.]',' ',value)

                                        if table.if_compoTerm(value)==True:
                                            #if table.check_If_Comma(value)==True:
                                            value=re.sub('[^a-zA-Z0-9\n\.]',' ',value)
                                            values=value.split()
                                            for v in values:
                                                v=re.sub('[^a-zA-Z0-9\n\.]','',v)
                                                #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+v)
                                                t.add((ut[terms],LDT[predicate],URIRef(usubClass[v])))
                                                #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                                t.add((URIRef(usubClass[v]),RDF.type,LDT[predicate]))
                                                #t.add((LDT[predicate],OWL.hasValue,usubClass))
                                        else:
                                            value=re.sub('[^a-zA-Z0-9\n\.]','',value)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+value)
                                            t.add((ut[terms],LDT[predicate],URIRef(usubClass[value])))
                                            #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                            t.add((URIRef(usubClass[value]),RDF.type,LDT[predicate]))
                                            #t.add((LDT[predicate],OWL.hasValue,usubClass))
                                for c in range(0,i):
                                        subClass=listOfobjects[c]
                                        subClass=str(subClass)
                                        subClass=re.sub('[^a-zA-Z0-9\n\.]',' ',subClass)
                                        #subClass=subClass.strip(' ')

                                        if table.if_compoTerm(subClass)==True:
                                            subClass=re.sub('[^a-zA-Z0-9\n\.]',' ',subClass)
                                            subClasses=subClass.split()
                                            for s in subClasses:
                                                s=re.sub('[^a-zA-Z0-9\n\.]','',s)
                                                #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+s)
                                                t.add((ut[terms],DC.hasPart,URIRef(usubClass[s])))
                                                t.add((URIRef(usubClass[s]),RDFS.subClassOf,ut[terms]))
                                                t.add( (usubClass[s],RDF.type,OWL.Class))
                                                t.add((usubClass[s],RDFS.label,Literal(subClass)))
                                                t.add((usubClass[s],DC.title,Literal(booktitle)))
                                                t.add((usubClass[s],DC.source,Literal(address)))
                                        else:
                                            subClass=re.sub('[^a-zA-Z0-9\n\.]','',subClass)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+subClass)
                                            t.add((ut[terms],DC.hasPart,URIRef(usubClass[subClass])))
                                            t.add((URIRef(usubClass[subClass]),RDFS.subClassOf,ut[terms]))
                                            t.add( (usubClass[subClass],RDF.type,OWL.Class))
                                            t.add((usubClass[subClass],RDFS.label,Literal(subClass)))
                                            t.add((usubClass[subClass],DC.title,Literal(booktitle)))
                                            t.add((usubClass[subClass],DC.source,Literal(address)))
                        elif table.if_compoTerm(tr)==False:
                            tr=re.sub('[^a-zA-Z0-9\n\.]','',tr)
                            t.add( (ut[tr], RDF.type,OWL.Class) )
                            t.add((ut[tr],RDFS.subClassOf,OWL.Thing))
                            t.add((ut[tr],RDFS.label,Literal(tr)))
                            t.add((ut[tr],DC.title,Literal(booktitle)))
                            t.add((ut[tr],DC.source,Literal(address)))
                            for key,value in table.termValue(subStr).items():
                                    key=str(key)
                                    key=re.sub('[^a-zA-Z0-9\n\.]',' ',key)
                                    #property=LDT[key]

                                    rel=''
                                    if table.if_compoTerm(key)==True:
                                        rel=table.splitTerms(key)[0]
                                    else:
                                        rel =key

                                    t.add((LDT[rel],RDF.type,RDF.Property))
                                    t.add((LDT[rel],RDFS.label,Literal('has'+rel)))
                                    t.add((LDT[rel],RDFS.comment,Literal(key)))
                                    t.add((LDT[rel],RDFS.domain,URIRef(LDT)))
                                    t.add((LDT[rel],RDFS.range,ut[tr]))

                                    predicate='has'+rel
                                    value=str(value)
                                    #value=v.strip(' ')
                                    value=re.sub('[^a-zA-Z0-9\n\.]',' ',value)

                                    if table.if_compoTerm(value)==True:
                                        #if table.check_If_Comma(value)==True:
                                        value=re.sub('[^a-zA-Z0-9\n\.]',' ',value)
                                        values=value.split()
                                        for v in values:
                                            v=re.sub('[^a-zA-Z0-9\n\.]','',v)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+v)
                                            t.add((ut[tr],LDT[predicate],URIRef(usubClass[v])))
                                            #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                            t.add((URIRef(usubClass[v]),RDF.type,LDT[predicate]))
                                            #t.add((LDT[predicate],OWL.hasValue,usubClass))
                                    else:
                                        value=re.sub('[^a-zA-Z0-9\n\.]','',value)
                                        #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+value)
                                        t.add((ut[tr],LDT[predicate],URIRef(usubClass[value])))
                                        #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                        t.add((URIRef(usubClass[value]),RDF.type,LDT[predicate]))
                                        #t.add((LDT[predicate],OWL.hasValue,usubClass))
                            for c in range(0,i):
                                    subClass=listOfobjects[c]
                                    subClass=str(subClass)
                                    subClass=re.sub('[^a-zA-Z0-9\n\.]',' ',subClass)
                                    #subClass=subClass.strip(' ')

                                    if table.if_compoTerm(subClass)==True:
                                        subClass=re.sub('[^a-zA-Z0-9\n\.]',' ',subClass)
                                        subClasses=subClass.split()
                                        for s in subClasses:
                                            s=re.sub('[^a-zA-Z0-9\n\.]','',s)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+s)
                                            t.add((ut[tr],DC.hasPart,URIRef(usubClass[s])))
                                            t.add((URIRef(usubClass[s]),RDFS.subClassOf,ut[tr]))
                                            t.add( (usubClass[s],RDF.type,OWL.Class))
                                            t.add((usubClass[s],RDFS.label,Literal(s)))
                                            t.add((usubClass[s],DC.title,Literal(booktitle)))
                                            t.add((usubClass[s],DC.source,Literal(address)))
                                    else:
                                        subClass=re.sub('[^a-zA-Z0-9\n\.]','',subClass)
                                        #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+subClass)
                                        t.add((ut[tr],DC.hasPart,URIRef(usubClass[subClass])))
                                        t.add((URIRef(usubClass[subClass]),RDFS.subClassOf,ut[tr]))
                                        t.add( (usubClass[subClass],RDF.type,OWL.Class))
                                        t.add((usubClass[subClass],RDFS.label,Literal(subClass)))
                                        t.add((usubClass[subClass],DC.title,Literal(booktitle)))
                                        t.add((usubClass[subClass],DC.source,Literal(address)))
                                    ##################################################
                    else:
                        #minStr=minStr.strip(" ")
                        minStr=re.sub('[^a-zA-Z0-9\n\.]',' ',minStr)
                        tr=minStr
                        if table.if_compoTerm(tr)==True:
                            for a,b in nltk_analyzer(tr).items():
                                a=re.sub('[^a-zA-Z0-9\n\.]','',a)
                                t.add( (ut[a], RDF.type,OWL.Class) )
                                t.add((ut[a],RDFS.subClassOf,OWL.Thing))
                                t.add((ut[a],RDFS.label,Literal(a)))
                                t.add((ut[a],DC.title,Literal(booktitle)))
                                t.add((ut[a],DC.source,Literal(address)))
                                b=re.sub('[^a-zA-Z0-9\n\.]','',b)
                                t.add( (usubClass[b], RDF.type,OWL.Class) )
                                t.add((usubClass[b],RDFS.subClassOf,ut[a]))
                                t.add((usubClass[b],RDFS.label,Literal(b)))
                                t.add((usubClass[b],DC.title,Literal(booktitle)))
                                t.add((usubClass[b],DC.source,Literal(address)))
                                for key,value in table.termValue(subStr).items():
                                        key=str(key)
                                        #key=key.replace(' ','_')
                                        key=re.sub('[^a-zA-Z0-9\n\.]',' ',key)
                                        #property=LDT[key]

                                        rel=''
                                        if table.if_compoTerm(key)==True:
                                            rel=table.splitTerms(key)[0]
                                        else:
                                            rel =key

                                        t.add((LDT[rel],RDF.type,RDF.Property))
                                        t.add((LDT[rel],RDFS.label,Literal('has'+rel)))
                                        t.add((LDT[rel],RDFS.comment,Literal(key)))
                                        t.add((LDT[rel],RDFS.domain,URIRef(LDT)))
                                        t.add((LDT[rel],RDFS.range,ut[a]))

                                        predicate='has'+rel
                                        value=str(value)
                                        value=re.sub('[^a-zA-Z0-9\n\.]',' ',value)

                                        if table.if_compoTerm(value)==True:

                                                values=value.split()
                                                for vss in values:

                                                    vss=re.sub('[^a-zA-Z0-9\n\.]','',vss)
                                                    #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+vss)
                                                    t.add((ut[a],LDT[predicate],URIRef(usubClass[vss])))
                                                   # t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                                    t.add((URIRef(usubClass[vss]),RDF.type,LDT[predicate]))

                                        else:
                                            value=re.sub('[^a-zA-Z0-9\n\.]','',value)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+value)
                                            t.add((ut[a],LDT[predicate],URIRef(usubClass[value])))
                                            #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                            t.add((URIRef(usubClass[value]),RDF.type,LDT[predicate]))
                                            #t.add((LDT[predicate],OWL.hasValue,usubClass))

                        elif table.if_compoTerm(tr)==False:
                            tr=re.sub('[^a-zA-Z0-9\n\.]','',tr)
                            t.add( (ut[tr], RDF.type,OWL.Class) )
                            t.add((ut[tr],RDFS.subClassOf,OWL.Thing))
                            t.add((ut[tr],RDFS.label,Literal(tr)))
                            t.add((ut[tr],DC.title,Literal(booktitle)))
                            t.add((ut[tr],DC.source,Literal(address)))
                            for key,value in table.termValue(subStr).items():
                                    key=str(key)
                                    #key=key.replace(' ','_')
                                    key=re.sub('[^a-zA-Z0-9\n\.]',' ',key)
                                    #property=LDT[key]

                                    rel=''
                                    if table.if_compoTerm(key)==True:
                                        rel=table.splitTerms(key)[0]
                                    else:
                                        rel =key

                                    t.add((LDT[rel],RDF.type,RDF.Property))
                                    t.add((LDT[rel],RDFS.label,Literal('has'+rel)))
                                    t.add((LDT[rel],RDFS.comment,Literal(key)))
                                    t.add((LDT[rel],RDFS.domain,URIRef(LDT)))
                                    t.add((LDT[rel],RDFS.range,ut[tr]))

                                    predicate='has'+rel
                                    value=str(value)
                                    value=re.sub('[^a-zA-Z0-9\n\.]',' ',value)

                                    if table.if_compoTerm(value)==True:

                                            values=value.split()
                                            for vss in values:

                                                vss=re.sub('[^a-zA-Z0-9\n\.]','',vss)
                                                #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+vss)
                                                t.add((ut[tr],LDT[predicate],URIRef(usubClass[vss])))
                                               # t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                                t.add((URIRef(usubClass[vss]),RDF.type,LDT[predicate]))

                                    else:
                                        value=re.sub('[^a-zA-Z0-9\n\.]','',value)
                                        #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+value)
                                        t.add((ut[tr],LDT[predicate],URIRef(usubClass[value])))
                                        #t.add((LDT[predicate],RDF.type,URIRef(usubClass)))
                                        t.add((URIRef(usubClass[value]),RDF.type,LDT[predicate]))
                                        #t.add((LDT[predicate],OWL.hasValue,usubClass))

            elif table.find_relation(subStr)==False:
            #subStr=subStr.lower()
                subStr=re.sub('[^a-zA-Z0-9\n\.]',' ',subStr)
                if len(subStr)>0:
                    if subStr.find('(')!=-1 and subStr.find(')')!=-1:
                        #terms["relation"].append(table.getParanthises(subStr))
                        insidePara=table.inside_Paranthises(subStr)
                        #print("insidePrara",insidePara)
                        #if self.if_compoTerm(insidePara)==True:
                        #    terms['listOFWords'].append(self.splitTerms(insidePara))
                        if table.check_If_Comma(insidePara)==True:
                            listOfobjects= table.findComma(insidePara)
                            i= len(listOfobjects)-1
                            cls=listOfobjects[i]
                            #terms["objects"].append(cls)
                            cls=str(cls)
                            tr=re.sub('[^a-zA-Z0-9\n\.]',' ',cls)
                            if table.if_compoTerm(tr)==True:
                                for msterm,subt in nltk_analyzer(tr).items():
                                    msterm=re.sub('[^a-zA-Z0-9\n\.]','',msterm)
                                    t.add( (ut[msterm], RDF.type,OWL.Class) )
                                    t.add((ut[msterm],RDFS.subClassOf,OWL.Thing))
                                    t.add((ut[msterm],RDFS.label,Literal(msterm)))
                                    t.add((ut[msterm],DC.title,Literal(booktitle)))
                                    t.add((ut[msterm],DC.source,Literal(address)))
                                    subt=re.sub('[^a-zA-Z0-9\n\.]','',subt)
                                    t.add( (usubClass[subt], RDF.type,OWL.Class) )
                                    t.add((usubClass[subt],RDFS.subClassOf,ut[msterm]))
                                    t.add((usubClass[subt],RDFS.label,Literal(subt)))
                                    t.add((usubClass[subt],DC.title,Literal(booktitle)))
                                    t.add((usubClass[subt],DC.source,Literal(address)))
                                    for c in range(0,i):
                                        subClass=listOfobjects[c]
                                        subClass=str(subClass)
                                        #subClass=subClass.strip('')
                                        subClass=re.sub('[^a-zA-Z0-9\n\.]',' ',subClass)
                                        if table.if_compoTerm(subClass)==True:
                                            subClasses=subClass.split()
                                            for s in subClasses:
                                                s=re.sub('[^a-zA-Z0-9\n\.]','',s)
                                                #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+s)
                                                t.add((ut[msterm],DC.hasPart,URIRef(usubClass[s])))
                                                t.add((URIRef(usubClass[s]),RDFS.subClassOf,ut[msterm]))
                                                t.add((usubClass[s],RDF.type,OWL.Class))
                                                t.add((usubClass[s],RDFS.label,Literal(subClass)))
                                                t.add((usubClass[s],DC.title,Literal(booktitle)))
                                                t.add((usubClass[s],DC.source,Literal(address)))
                                        else:
                                            subClass=re.sub('[^a-zA-Z0-9\n\.]','',subClass)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+subClass)
                                            t.add((ut[msterm],DC.hasPart,URIRef(usubClass[subClass])))
                                            t.add((URIRef(usubClass[subClass]),RDFS.subClassOf,ut[msterm]))
                                            t.add( (usubClass[subClass],RDF.type,OWL.Class))
                                            t.add((usubClass[subClass],RDFS.label,Literal(subClass)))
                                            t.add((usubClass[subClass],DC.title,Literal(booktitle)))
                                            t.add((usubClass[subClass],DC.source,Literal(address)))
                            elif table.if_compoTerm(tr)==False:
                                tr=re.sub('[^a-zA-Z0-9\n\.]','',tr)
                                t.add( (ut[tr], RDF.type,OWL.Class) )
                                t.add((ut[tr],RDFS.subClassOf,OWL.Thing))
                                t.add((ut[tr],RDFS.label,Literal(tr)))
                                t.add((ut[tr],DC.title,Literal(booktitle)))
                                t.add((ut[tr],DC.source,Literal(address)))
                                for c in range(0,i):
                                    subClass=listOfobjects[c]
                                    subClass=str(subClass)
                                    #subClass=subClass.strip('')
                                    subClass=re.sub('[^a-zA-Z0-9\n\.]',' ',subClass)
                                    if table.if_compoTerm(subClass)==True:
                                        subClasses=subClass.split()
                                        for s in subClasses:
                                            s=re.sub('[^a-zA-Z0-9\n\.]','',s)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+s)
                                            t.add((ut[tr],DC.hasPart,URIRef(usubClass[s])))
                                            t.add((URIRef(usubClass[s]),RDFS.subClassOf,ut[tr]))
                                            t.add( (usubClass[s],RDF.type,OWL.Class))
                                            t.add((usubClass[s],RDFS.label,Literal(s)))
                                            t.add((usubClass[s],DC.title,Literal(booktitle)))
                                            t.add((usubClass[s],DC.source,Literal(address)))
                                    else:
                                        subClass=re.sub('[^a-zA-Z0-9\n\.]','',subClass)
                                        #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+subClass)
                                        t.add((ut[tr],DC.hasPart,URIRef(usubClass[subClass])))
                                        t.add((URIRef(usubClass[subClass]),RDFS.subClassOf,ut[tr]))
                                        t.add( (usubClass[subClass],RDF.type,OWL.Class))
                                        t.add((usubClass[subClass],RDFS.label,Literal(subClass)))
                                        t.add((usubClass[subClass],DC.title,Literal(booktitle)))
                                        t.add((usubClass[subClass],DC.source,Literal(address)))
                        else:
                            insidePara=insidePara.strip(' ')
                            #insidePara=insidePara.lower()
                            tr=re.sub('[^a-zA-Z0-9\n\.]',' ',insidePara)
                            if table.if_compoTerm(tr)==True:
                                for a,b in nltk_analyzer(tr).items():
                                    a=re.sub('[^a-zA-Z0-9\n\.]','',a)
                                    t.add( (ut[a], RDF.type,OWL.Class) )
                                    t.add((ut[a],RDFS.subClassOf,OWL.Thing))
                                    t.add((ut[a],RDFS.label,Literal(a)))
                                    t.add((ut[a],DC.title,Literal(booktitle)))
                                    t.add((ut[a],DC.source,Literal(address)))
                                    b=re.sub('[^a-zA-Z0-9\n\.]','',b)
                                    t.add( (usubClass[b], RDF.type,OWL.Class) )
                                    t.add((usubClass[b],RDFS.subClassOf,ut[a]))
                                    t.add((usubClass[b],RDFS.label,Literal(b)))
                                    t.add((usubClass[b],DC.title,Literal(booktitle)))
                                    t.add((usubClass[b],DC.source,Literal(address)))

                            elif table.if_compoTerm(tr)==False:
                                tr=re.sub('[^a-zA-Z0-9\n\.]','',tr)
                                t.add( (ut[tr], RDF.type,OWL.Class) )
                                t.add((ut[tr],RDFS.subClassOf,OWL.Thing))
                                t.add((ut[tr],RDFS.label,Literal(tr)))
                                t.add((ut[tr],DC.title,Literal(booktitle)))
                                t.add((ut[tr],DC.source,Literal(address)))

                    elif table.check_If_Comma(subStr)==True:
                        #subStr=subStr.strip(" ")
                        #subStr=subStr.lower()
                        listOfobjects= table.findComma(subStr)
                        i= len(listOfobjects)-1
                        cls=listOfobjects[i]
                        #terms["objects"].append(cls)
                        cls=str(cls)
                        tr=re.sub('[^a-zA-Z0-9\n\.]',' ',cls)
                        if table.if_compoTerm(tr)==True:
                            for terms,subt in nltk_analyzer(tr).items():
                                terms=re.sub('[^a-zA-Z0-9\n\.]','',terms)
                                t.add( (ut[terms], RDF.type,OWL.Class) )
                                t.add((ut[terms],RDFS.subClassOf,OWL.Thing))
                                t.add((ut[terms],RDFS.label,Literal(terms)))
                                t.add((ut[terms],DC.title,Literal(booktitle)))
                                t.add((ut[terms],DC.source,Literal(address)))
                                subt=re.sub('[^a-zA-Z0-9\n\.]','',subt)
                                t.add( (usubClass[subt], RDF.type,OWL.Class) )
                                t.add((usubClass[subt],RDFS.subClassOf,ut[terms]))
                                t.add((usubClass[subt],RDFS.label,Literal(subt)))
                                t.add((usubClass[subt],DC.title,Literal(booktitle)))
                                t.add((usubClass[subt],DC.source,Literal(address)))
                                for c in range(0,i):
                                        subClass=listOfobjects[c]
                                        subClass=str(subClass)
                                        subClass=subClass.strip(' ')
                                        subClass=re.sub('[^a-zA-Z0-9\n\.]',' ',subClass)
                                        if table.if_compoTerm(subClass)==True:
                                            subClasses=subClass.split()
                                            for s in subClasses:
                                                s=re.sub('[^a-zA-Z0-9\n\.]','',s)
                                                #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+s)
                                                t.add((ut[terms],DC.hasPart,URIRef(usubClass[s])))
                                                t.add((URIRef(usubClass[s]),RDFS.subClassOf,ut[terms]))
                                                t.add( (usubClass[s],RDF.type,OWL.Class))
                                                t.add((usubClass[s],RDFS.label,Literal(subClass)))
                                                t.add((usubClass[s],DC.title,Literal(booktitle)))
                                                t.add((usubClass[s],DC.source,Literal(address)))
                                        else:
                                            subClass=re.sub('[^a-zA-Z0-9\n\.]','',subClass)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+subClass)
                                            t.add((ut[terms],DC.hasPart,URIRef(usubClass[subClass])))
                                            t.add((URIRef(usubClass[subClass]),RDFS.subClassOf,ut[terms]))
                                            t.add( (usubClass[subClass],RDF.type,OWL.Class))
                                            t.add((usubClass[subClass],RDFS.label,Literal(subClass)))
                                            t.add((usubClass[subClass],DC.title,Literal(booktitle)))
                                            t.add((usubClass[subClass],DC.source,Literal(address)))
                        elif table.if_compoTerm(tr)==False:
                            tr=re.sub('[^a-zA-Z0-9\n\.]','',tr)
                            t.add( (ut[tr], RDF.type,OWL.Class) )
                            t.add((ut[tr],RDFS.subClassOf,OWL.Thing))
                            t.add((ut[tr],RDFS.label,Literal(tr)))
                            t.add((ut[tr],DC.title,Literal(booktitle)))
                            t.add((ut[tr],DC.source,Literal(address)))
                            for c in range(0,i):
                                    subClass=listOfobjects[c]
                                    subClass=str(subClass)
                                    subClass=subClass.strip(' ')
                                    subClass=re.sub('[^a-zA-Z0-9\n\.]',' ',subClass)
                                    if table.if_compoTerm(subClass)==True:
                                        subClasses=subClass.split()
                                        for s in subClasses:
                                            s=re.sub('[^a-zA-Z0-9\n\.]','',s)
                                            #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+s)
                                            t.add((ut[tr],DC.hasPart,URIRef(usubClass[s])))
                                            t.add((URIRef(usubClass[s]),RDFS.subClassOf,ut[tr]))
                                            t.add( (usubClass[s],RDF.type,OWL.Class))
                                            t.add((usubClass[s],RDFS.label,Literal(s)))
                                            t.add((usubClass[s],DC.title,Literal(booktitle)))
                                            t.add((usubClass[s],DC.source,Literal(address)))
                                    else:
                                        subClass=re.sub('[^a-zA-Z0-9\n\.]','',subClass)
                                        #usubClass=URIRef("http://www.JceFinalProjectOntology.com/subject/"+subClass)
                                        t.add((ut[tr],DC.hasPart,URIRef(usubClass[subClass])))
                                        t.add((URIRef(usubClass[subClass]),RDFS.subClassOf,ut[tr]))
                                        t.add( (usubClass[subClass],RDF.type,OWL.Class))
                                        t.add((usubClass[subClass],RDFS.label,Literal(subClass)))
                                        t.add((usubClass[subClass],DC.title,Literal(booktitle)))
                                        t.add((usubClass[subClass],DC.source,Literal(address)))
                    else:

                        #subStr=subStr.strip(' ')
                        subStr=re.sub('[^a-zA-Z0-9\n\.]',' ',subStr)
                        tr=subStr
                        print('term:'+tr)
                        print(len(tr))
                        if len(tr)>0:
                            if table.if_compoTerm(tr)==True:
                                    print('compoterm:'+tr)

                                    for terms,subt in nltk_analyzer(tr).items():
                                        terms=re.sub('[^a-zA-Z0-9\n\.]','',terms)
                                        t.add( (ut[terms], RDF.type,OWL.Class) )
                                        t.add((ut[terms],RDFS.subClassOf,OWL.Thing))
                                        t.add((ut[terms],RDFS.label,Literal(terms)))
                                        t.add((ut[terms],DC.title,Literal(booktitle)))
                                        t.add((ut[terms],DC.source,Literal(address)))
                                        subt=re.sub('[^a-zA-Z0-9\n\.]','',subt)
                                        t.add( (ut[subt], RDF.type,OWL.Class) )
                                        t.add((ut[subt],RDFS.subClassOf,ut[terms]))
                                        t.add((ut[subt],RDFS.label,Literal(subt)))
                                        t.add((ut[subt],DC.title,Literal(booktitle)))
                                        t.add((ut[subt],DC.source,Literal(address)))
                            elif table.if_compoTerm(tr)==False:
                                tr=re.sub('[^a-zA-Z0-9\n\.]','',tr)
                                t.add( (ut[tr], RDF.type,OWL.Class) )
                                t.add((ut[tr],RDFS.subClassOf,OWL.Thing))
                                t.add((ut[tr],RDFS.label,Literal(tr)))
                                t.add((ut[tr],DC.title,Literal(booktitle)))
                                t.add((ut[tr],DC.source,Literal(address)))
                else:

                    subStr=subStr.strip(' ')
                    tr=re.sub('[^a-zA-Z0-9\n\.]',' ',subStr)
                    if table.if_compoTerm(tr)==True:
                        for terms,vtr in nltk_analyzer(tr).items():
                            terms=re.sub('[^a-zA-Z0-9\n\.]','',terms)
                            t.add( (ut[terms], RDF.type,OWL.Class) )
                            t.add((ut[terms],RDFS.subClassOf,OWL.Thing))
                            t.add((ut[terms],RDFS.label,Literal(terms)))
                            t.add((ut[terms],DC.title,Literal(booktitle)))
                            t.add((ut[terms],DC.source,Literal(address)))
                            vtr=re.sub('[^a-zA-Z0-9\n\.]','',vtr)
                            t.add( (usubClass[vtr], RDF.type,OWL.Class) )
                            t.add((usubClass[vtr],RDFS.subClassOf,ut[terms]))
                            t.add((usubClass[vtr],RDFS.label,Literal(vtr)))
                            t.add((usubClass[vtr],DC.title,Literal(booktitle)))
                            t.add((usubClass[vtr],DC.source,Literal(address)))
                    elif table.if_compoTerm(tr)==False:
                        tr=re.sub('[^a-zA-Z0-9\n\.]','',tr)
                        t.add( (ut[tr], RDF.type,OWL.Class) )
                        t.add((ut[tr],RDFS.subClassOf,OWL.Thing))
                        t.add((ut[tr],RDFS.label,Literal(tr)))
                        t.add((ut[tr],DC.title,Literal(booktitle)))
                        t.add((ut[tr],DC.source,Literal(address)))
    #tc=Graph(store=store,identifier=usubClass)
t.bind("dc", "http://http://purl.org/dc/elements/1.1/")
t.bind('JFPO',LDT)
t.bind('terms',ut)
t.commit()
t.serialize('file2.rdf',format='turtle',encoding='utf-8')
#t.parse('subjects.owl',format='xml')
print(len(t))

    #fh.close()
