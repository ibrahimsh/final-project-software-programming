__author__ = 'MatrixRev'
import json
import codecs
import glob
import os
import sys

#path = u"C://Users//MatrixRev//Desktop//library_5//"
path="C://Users//MatrixRev//Desktop//mainLib//" # input file 
outFile='C:/Users/MatrixRev/Desktop/books/output/mainsubjects.txt' #output file
pathNew = u"C://Users//MatrixRev//Desktop//newOut"

counter=0
subjects_list=[]
for root,dir,files in os.walk(path):
    for file  in  files:

        counter=counter+1
        print(counter,root,dir,file)
        if len(file)>0 :
            if file.endswith(".json"):
                with codecs.open(os.path.join(root, file), "rb",encoding="UTF-8") as fd:

                    json_data = json.load(fd)
                    select_num=json_data['isbn']
                    select_title=json_data['title']
                    select_data =json_data['subjects']
                    select_subTitle=json_data['subtitle']
                    select_Authors=json_data['authors']
                    select_Comments=json_data['comments']
                    n = len(json_data['subjects'])
                    print(n)
                    newFileName=file.replace('.json','.txt')
                    newdir=os.path.join(pathNew)
                    os.chdir(newdir)
                    with codecs.open(os.path.join(newdir,newFileName),'w',encoding='utf-8')as tf:
                        for l in list(select_data):

                            print(l,file=tf)
                        #for i in list(select_title):
                        print(select_title,file=tf)
                        for i in select_Comments:
                            print(i,file=tf)
                        for i in select_subTitle:
                            print(i,file=tf)
                        for i in range(0,len(select_Authors)):
                            print(select_Authors[i],file=tf)

                           # fd.write(n,"\n",select_title,"\n","subjects","\n")
                        #outfile.write(select_title)
                       # print("book Title  : ",select_title,"\n")
                       # print("subjects is:")
                    for i in range(n-0):
                        print(select_data[i])
                        subjects_list.append(select_data[i]+" "+"***Title:"+" "+select_title+" "+"***link"+" "+root+"//"+file)
                           #fd.writelines(['%s\n'for sub in asubjects])
                       # for s in sub:
                        #    fd.write("".join(s)+'\n')
    f=len(subjects_list)
    print(f)
    #fd.close()
    with codecs.open(outFile,'w',encoding='utf-8')as fh:
        for sub in subjects_list:
            if len(sub)>0:
                #sub=sub.replace('-','')
                sub=sub.lower()
                sub=sub.strip('\n')
               # print(sub,file='subject.txt')
                fh.write(sub)
                fh.write("\n")
