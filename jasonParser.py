__author__ = 'MatrixRev'

import json
import codecs
import glob
import os
jason_file = 'C:/Users/MatrixRev/Desktop/books/9_dir/*'
files=glob.glob(jason_file)
#output ='C:/Users/MatrixRev/Desktop/books/output/*'
#dir=os.path.join(output,)
for file in files:

    with codecs.open(file,'rb', encoding='utf-8') as fh:
            json_data = json.load(fh)
            select_num=json_data['isbn']
            outFile= 'C:/Users/MatrixRev/Desktop/books/output/'+select_num+'.txt'

            with codecs.open(outFile,'w',encoding = 'utf-8')as fd:
                select_title=json_data['title']
                select_data =json_data['subjects']
                n = len(json_data['subjects'])
                print(n)
               # fd.write(n,"\n",select_title,"\n","subjects","\n")
            #outfile.write(select_title)

                print("book Title  : ",select_title,"\n")
                print("subjects is:")
                for i in range (n-0):
                  print(select_data[i])
                  fd.write(select_data)



s= "schol"
t= "scholar"

def LD(s,t):
    s = ' ' + s
    t = ' ' + t
    d = {}
    S = len(s)
    T = len(t)
    for i in range(S):
        d[i, 0] = i
    for j in range (T):
        d[0, j] = j
    for j in range(1,T):
        for i in range(1,S):
            if s[i] == t[j]:
                d[i, j] = d[i-1, j-1]
            else:
                d[i, j] = min(d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + 1)

       # print(d[S-1, T-1])
    return d[S-1, T-1]
