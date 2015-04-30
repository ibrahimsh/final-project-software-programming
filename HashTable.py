__author__ = 'MatrixRev'
import codecs
import json
import re
from collections import defaultdict
import Levenshtein
import string
import os
filename='C:/Users/MatrixRev/Desktop/books/output/subjects.txt'
output='C:\\Users\\MatrixRev\\Desktop\\books\\output\\dictionnary.json'
filePath='C:\\Users\\MatrixRev\\Desktop\\books\\output\\'
termfile='C:\\Users\\MatrixRev\\Desktop\\books\\output\\allTerms.txt'
out2='C:\\Users\\MatrixRev\\Desktop\\books\\output\\newprint.txt'
class HashTable():

    def __init__(self):
        self.allTerms={}

        self.symbols={ '**a':'Personal name (NR)','**sub':'subString',
                       '**period':'period',
                         '**location':'location','**date':'date',
                         '**b':'Numeration (NR)',
                         '**c':'Titles and other words associated with a name (R)',
                         '**e':'Relator term (R)',
                         '**f':'Date of a work (NR)',
                         '**g':'Miscellaneous information (R)',
                         '**h':'Medium (NR)A media qualifier.',
                         '**j':'Attribution qualifier (R)',
                         #Attribution information for names when the responsibility is unknown, uncertain, fictitious, or pseudonymous.
                         '**k':'Form subheading (R)',
                         #'**l':'Language of a work (NR)',
                         '**m':'Medium of performance for music (R)',
                         '**n':'Number of part/section of a work (R)',
                         '**o':'Arranged statement for music (NR)',
                         #'**p':'Name of part/section of a work (R)',
                         '**q':'Fuller form of name (NR)',
                         '**r':'Key for music (NR)',
                         #'**s':'Version (NR)',
                         '**t':'Title of a work (NR)',
                         '**u':'Affiliation (NR)',
                         '**v':'Form subdivision (R)',
                         '**x':'General subdivision (R)','u(ג)':'history','u(ה)':'History',
                         '**y':'Chronological subdivision (R)',
                         '**z':'Geographic subdivision (R)',
                         '**0':'Authority record control number or standard number (R)',
                        #See description of this subfield in Appendix A: Control Subfields.
                         '**2':'Source of heading or term (NR)',
                        #Code from: Subject Heading and Term Source Codes.
                         '**3':'Materials specified (NR)',
                         '**4':'Relator code (R)',
                         '**6':'Linkage (NR)',
                        #See description of this subfield in Appendix A: Control Subfields.
                         '**8':'Field link and sequence number (R)',
                         '=':'isA'}

        sym_keys=self.symbols.keys()
        value=self.symbols.values()



    def Relation(self):
            return ({"bookTitle":"",
                "relation":[],
                "objects":[],
                "subClass":[],
                "semilarTerms":[],
                "Link":"",
                "listOFWords":[]})


    def fill_Terms(self,sub):
        terms=self.Relation()
        allterm=self.allTerms
        subStr=""
        if sub.find("***link"):
            terms['Link']=self.setLink(sub)
        newIndex=sub.index("***link")
        sub=sub[:newIndex]
        if sub.rfind("***Title"):
            terms['bookTitle']=self.setTitle(sub)
        newIndex=sub.index("***Title")
        subStr=sub[:newIndex]
        print("all sub str:",subStr)
        if self.find_relation(subStr)==True:
            #for n in self.termValue(subStr):
            terms["relation"]=self.termValue(subStr)

              #print("newValue is :",n)
            minStr=self.CompTermKey(subStr)
            print("the sub string is:",minStr)
            if minStr.find('(')!=-1 and minStr.find(')')!=-1:
                print("yest find para",self.if_FindParanthesis(minStr))
                terms["relation"]=self.getParanthises(minStr)
                insidePara=self.inside_Paranthises(minStr)
                print("insidePrara",insidePara)
                if self.if_compoTerm(insidePara):
                   terms['listOFWords']=self.splitTerms(insidePara)
                if self.check_If_Comma(insidePara)==True:
                    listOfobjects= self.findComma(insidePara)
                    i=len(listOfobjects)-1
                    print("i",i)
                    cls=listOfobjects[i]
                    terms["objects"]=cls
                    for c in range(0,i):
                     subClass=listOfobjects[c]
                     terms["subClass"]=subClass
                    for k in range(0,len(listOfobjects)):
                        minStr=listOfobjects[k]
                        allterm[minStr]=terms
                else:
                    minStr=insidePara
                    allterm[minStr]=terms
            elif self.check_If_Comma(minStr)==True:
                listOfobjects= self.findComma(minStr)
                i= len(listOfobjects)-1
                print("listofbjects is :",listOfobjects[i])
                cls=listOfobjects[i]
                terms['objects']=cls
                for c in range(0,i):
                    subClass=listOfobjects[c]
                    terms["subClass"]=subClass
                for t in range(0,len(listOfobjects)):
                    minStr=listOfobjects[t]
                    allterm[minStr]=terms
            else:
                if self.if_compoTerm(minStr):
                   terms['listOFWords']=self.splitTerms(minStr)
                allterm[minStr]=terms

        elif self.find_relation(subStr)==False:
            if subStr.find('(')!=-1 and subStr.find(')')!=-1:
                terms["relation"]=self.getParanthises(subStr)
                insidePara=self.inside_Paranthises(subStr)
                print("insidePrara",insidePara)
                if self.if_compoTerm(insidePara):
                    terms['listOFWords']=self.splitTerms(insidePara)
                if self.check_If_Comma(insidePara)==True:
                    listOfobjects= self.findComma(insidePara)
                    i= len(listOfobjects)-1
                    cls=listOfobjects[i]
                    terms["objects"]=cls
                    for c in range(0,i):
                        subClass=listOfobjects[c]
                        terms["subClass"]=subClass
                    for t in range(0,len(listOfobjects)):
                        mterm=listOfobjects[t]
                        allterm[mterm]=terms
                else:
                    allterm[insidePara]=terms
                    if self.if_compoTerm(insidePara):
                        terms['listOFWords']=self.splitTerms(insidePara)
            elif self.check_If_Comma(subStr)==True:
                listOfobjects= self.findComma(subStr)
                i= len(listOfobjects)-1
                cls=listOfobjects[i]
                terms["objects"]=cls
                for c in range(0,i):
                    subClass=listOfobjects[c]
                    terms["subClass"]=subClass
                for e in range(0,len(listOfobjects)):
                    tterm=listOfobjects[e]
                    allterm[tterm]=terms
            else:
                if self.if_compoTerm(subStr):
                   terms['listOFWords']=self.splitTerms(subStr)
                allterm[subStr]=terms
        else:
            if self.if_compoTerm(subStr):
                   terms['listOFWords']=self.splitTerms(subStr)
            allterm[subStr]=terms

        return allterm
    #def get_allTerms(self,subject):
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
                                     the_same.append(item)

                            if Levenshtein.ratio(t,item)==0.8:
                                if item not in the_same:
                                    the_same.append(item)
                #print("the ratio is ",the_ratio)

        print("is",the_same)
        return the_same


    def setLink(self,subject):
        if subject.find("***link"):
            linkIndex=subject.index("***link")
            newIndex=linkIndex+len("***link")+1
            link=subject[newIndex:]
        return link

    def setTitle(self,sub):
        if sub.find("***Title"):
            titleIndex=sub.index("***Title")
            newIndex=len("***Title")+titleIndex
            title=sub[newIndex:].strip(":")
        return title


    def find_relation(self, subjects):
        print("relation is check:",subjects)
        counter=0
        is_relation=True
        sub_len = len(subjects)
       # regex = re.compile('('+')')
        for key in self.symbols.keys():
            #keyLength=len(key)
            #substring= subjects.split(key)
            if subjects.rfind(key)!=-1:
                counter=counter+1
                #print(subjects.index(key),key)
                #is_relation=True

        if counter>0:
            print(counter)
            is_relation=True
        #elif regex.match(subjects) or subjects.find(',')!=-1 and counter==0:
          #   is_relation=True
        else:
            is_relation=False
        print("if the relation",is_relation)
        return is_relation


    def termValue(self,subjects):
        counter=0
        val={}
        regex = re.compile('('+')')
        key_index = 0
        key_length = 0
        val_index = 0
        termValue=""
        tValueIndex=[]
        longVal=[]

        if isinstance(subjects,bytes):
            subjects=subjects.decode('ascii')

        for  key in self.symbols.keys():
            if  subjects.find(key)!=-1 :
                counter = counter+1
                key_length=len(key)
                key_index=subjects.index(key)
                print(key,key_index,key_length)
               # val_index=key_length+key_index
                val[key]=key_index


        keyOfvalyes=val.keys()
        valOfValues=list(val.values())
        #print(keyOfvalyes)
       # val=sorted(val,key=val.get)
        #print(val)
        if(counter>1):
            print(counter,"is count")
            for k in val.keys():
                for i in range(0,len(valOfValues)):
                    if val[k]==valOfValues[i]:
                          start = valOfValues[i]
                          print( "is",start)
                          nextVal=valOfValues[0]
                          newNextVal=0
                          print("next is",nextVal)
                         # print(len(keyOfvalyes))
                          if start>nextVal:
                             newNextVal=start
                             print("newValGRT",newNextVal)
                             val_index=len(k)+start
                             print(val_index)

                             tValueIndex=subjects[val_index:len(subjects)]
                             #print(len(subjects),"subject length")
                             termValue=subjects[:start-len(k)]
                             print("1 term value->",termValue)
                             tValueIndex=tValueIndex.strip(":")
                             longVal.append({self.symbols[k]:tValueIndex})
                          elif start==nextVal:
                              print("newNVal",nextVal)
                              val_index=len(k)+start
                              end=valOfValues[i-1]#tsle7
                              print("welcom",end)
                              tValueIndex=subjects[val_index:end]
                              print(tValueIndex)
                              tValueIndex=tValueIndex.strip(":")

                              longVal.append({self.symbols[k]:tValueIndex})

                              #print(longVal)
        elif counter==1:
            for k in val.keys():
                start=val[k]
                val_index= len(k)+start
                sub= subjects[val_index:]
                sub=sub.strip(':')
                longVal.append({self.symbols[k]:sub})
                termIndex=val_index-len(k)
                # termValue=termValue.encode(encoding='utf-8')
                termValue=subjects[:termIndex]
                termValue=termValue.strip('-')
                print("term value  1=",termValue)

        return longVal
    def findComma(self,sub):
        newSub=[]
        if sub.find(',')!=-1:


            for s in sub.split(','):
                newSub.append(s)

        return newSub


    def getParanthises(self,sub):

       # regex = re.compile('('+')')
        longVal=[]

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

                longVal.append({"aspect of ":nValue})
            elif tindex>eindex and tindex<len(termValue)-1:
                nValue=termValue[tindex+1:]
                longVal.append({"aspect of":nValue})
            elif eindex==len(termValue)-1and tindex<eindex:
                nValue=termValue[:tindex-1]
                longVal.append({"aspect of":nValue})
            elif tindex==len(termValue)-1and tindex>eindex:
                nValue=termValue[:eindex-1]
                longVal.append({"aspect of ":nValue})
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
        if term in self.terms.keys():
            existTerm=False
        else:
            existTerm=True
        return existTerm
    def check_value(self,val):
        if val in self.terms.values():
            return False
        else:
            return True
    def if_compoTerm(self,sub):
        counter=0
        for w in sub.split(' '):
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
            for k,v in self.terms.items():
               json.dump({'term':k,'value':v},outfile,ensure_ascii=False,indent=4)
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
ald=Levenshtein.editops("science computer","computer science")
print(ald)
edit=Levenshtein.distance("computer science","computer science")
dist=Levenshtein.apply_edit(ald,"science computer","computer science")
print(dist)
print(edit)
table=HashTable()
samestr=table.similarTerms("science computer")
print("same string is :",samestr)
#term=table.subject_file(filename)
#words=table.splitTerms('Biological transport')
#print("num of words:->",words)
#term=table.text_Analyzer(filename)
#t=hash.terms
#all=table.printTerms(output)
#print("the terms is :",all)
#print(hash.symbols)
#val=table.termValue('Arabic literature**z:Egypt**x:History and criticism')
#key2=table.CompTermKey(u'הבדלים בין המינים (בני אדם) -**x:הבטים ביולוגיים')
#subst=table.CompTermKey('Dresden, Germany **v: Congresses ***Title: Programming languages and system design***link C://Users//MatrixRev//Desktop//library_5//0_dir//0444867945.json')
#print('new key is :',key2)
#print('the sub string is ',subst)
#newVal=table.termValue('הבדלים בין המינים (בני אדם) -**xהבטים ביולוגיים')
#print('new value is ',newVal)
#isrelation=table.find_relation(u'הבדלים בין המינים (בני אדם) -**xהבטים ביולוגיים')
#print(isrelation)
#sub=table.CompTermKey(u'הבדלים בין המינים (בני אדם) -**xהבטים ביולוגיים')
#print(sub)
#print('relation is :',val)
#tofile=hash.printTerms(output)
#num=table.num_there("welcom in 9991")
#print('if has number',num)
#insideP=table.inside_Paranthises("Packet switching (Data transmission)")
#print('insideP is :',insideP)
#outP=table.getParanthises("Packet switching (Data transmission)")
#print("outP is :",outP)
#link=table.setLink("Packet switching (Data transmission) ***Title: X.25 explained***link C://Users//MatrixRev//Desktop//library_5//0_dir//0470201835.json")
#print("theLink:",link)
#title=table.setTitle("Packet switching (Data transmission) ***Title: X.25 explained")
#print(title)
#read=table.text_analyzing(filename,out2)
#comma=table.findComma("London, Ontario, Canada ")
#print(comma)
#i = (len(comma)-1)
#print("main subject is:",comma[i])
#allterm=table.fill_Terms("Social sciences **sub: Methodology ***Title: Introduction to multidimensional scaling"
 #                       "***link C://Users//MatrixRev//Desktop//library_5//I_dir//Introduction to multidimensional scaling.json")
#print("allTermis",allterm)

#exterm=table.fill_Terms("Particle range (Nuclear physics) ***Title: The stopping and range of ions in solids"
 #                       "***link C://Users//MatrixRev//Desktop//library_5//0_dir//008021603X.json")
#print(exterm)
''''
with codecs.open(filename,'rb',encoding='utf-8')as fileInput:
    lines=fileInput.readlines()
    for line in lines:
        if line.find(",etc.")!=-1:
            line=line.replace(',etc.'," ")
        getTerms=table.fill_Terms(line)
with codecs.open(output,'w',encoding='utf-8')as outfile:
    json.dump(table.allTerms,outfile,ensure_ascii=False,indent=4)
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