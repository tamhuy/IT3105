import copy
from GAC import GAC
class searchState:
    def __init__(self, gac,  domains):
        #self.variables = variables
        self.domains = domains
        #self.constraints = constraints
        self.f = float('inf')
        self.g = 0
        self.h = 0
        self.gac = gac


    def findLegalMoves(self):
        successors = []
        short = float('inf')
        domainkey = None
        for key in self.domains.keys():
            if 1 < len(self.domains[key]) < short and isinstance(self.domains[key], list):
                short = len(self.domains[key])
                domainkey = key
        if domainkey is None:
            return []

        for assumption in self.domains[domainkey]:
            assignment = copy.deepcopy(self.domains)
            assignment[domainkey] = [assumption]
            successor = searchState(self.gac,assignment)
            self.gac.rerun(successor, domainkey)
            legal = True
            for key in successor.domains.keys():
                if len(successor.domains[key]) == 0:
                    legal = False
            if legal is True:
                successors.append(successor)
        return successors
    def heuristic(self):
        h = 0
        for key in self.domains.keys():
            if len(self.domains[key]) > 1:
                h+=1
        return h


    def isSolution(self):
        for key in self.domains.keys():
            #print len(self.domains[key])
            if len(self.domains[key]) > 1:
                return False
        return True


