import GUI

from GAC import GAC
from csp import CSP

def agac(filename):
    pass


CSP = CSP("Nonograms/nono-telephone.txt")
#print CSP.constraints[CSP.rowVar[0]][0].function
#print CSP.variables
test = GAC(CSP)
test.initialize()
test.domainFilter()
#for i in test.variables:
    #print test.domains[i]
GUI.GUI(test)