import GUI
from SearchState import searchState
from GAC import GAC
from csp import CSP
from aStar import aStar

def agac(filename):
    csp = CSP(filename)
    print csp.domains
    gac = GAC(csp)
    gac.initialize()
    gac.domainFilter()
    print gac.domains
    #ss = searchState(gac ,gac.domains)
    #print aStar(ss)
    GUI.GUI(gac)



agac("Nonograms/nono-chick.txt")
#print CSP.constraints[CSP.rowVar[0]][0].function
#print CSP.variables
#gac = GAC()
#gac.initialize(csp)
#gac.domainFilter(csp)
#print csp.domains
#ss = searchState(csp, csp.variables,csp.domains,csp.constraints,csp.rows,csp.columns)
#aStar(ss)
#print aStar(ss).domains
#GUI.draw(aStar(ss),csp )
#for i in test.variables:
    #print test.domains[i]
#GUI.GUI(csp)