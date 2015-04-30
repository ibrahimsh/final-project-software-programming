__author__ = 'MatrixRev'

class SymbolTable():



    dict={ '$a':'Personal name (NR)','$b':'Numeration (NR)',
         '$c':'Titles and other words associated with a name (R)',
         '$d':'Dates associated with a name (NR)','$e':'Relator term (R)',
         '$f':'Date of a work (NR)','$g':'Miscellaneous information (R)',
         '$h':'Medium (NR)A media qualifier.','$j':'Attribution qualifier (R)',
         #Attribution information for names when the responsibility is unknown, uncertain, fictitious, or pseudonymous.
         '$k':'Form subheading (R)',
         '$l':'Language of a work (NR)',
         '$m':'Medium of performance for music (R)',
         '$n':'Number of part/section of a work (R)',
         '$o':'Arranged statement for music (NR)',
         '$p':'Name of part/section of a work (R)',
         '$q':'Fuller form of name (NR)',
         '$r':'Key for music (NR)',
         '$s':'Version (NR)',
         '$t':'Title of a work (NR)',
         '$u':'Affiliation (NR)',
         '$v':'Form subdivision (R)',
         '$x':'General subdivision (R)',
         '$y':'Chronological subdivision (R)',
         '$z':'Geographic subdivision (R)',
         '$0':'Authority record control number or standard number (R)',
        #See description of this subfield in Appendix A: Control Subfields.
         '$2':'Source of heading or term (NR)',
        #Code from: Subject Heading and Term Source Codes.
         '$3':'Materials specified (NR)',
         '$4':'Relator code (R)',
         '$6':'Linkage (NR)',
        #See description of this subfield in Appendix A: Control Subfields.
         '$8':'Field link and sequence number (R)'}
    def get_key(self):
             return dict.keys()
    def get_value(self):
             return dict.values()
    def findKey(key):
        if key in dict.keys():
            return True
        else:
            return False
    def findValue(value):
        if value in dict.values():
            return True
        else:
            return False



temp= SymbolTable().findKey('$x')
print(temp)