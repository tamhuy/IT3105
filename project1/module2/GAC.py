from collections import deque


class GAC():
    def __init__(self, csp):

        self.variables = csp.variables
        self.domains = csp.domains
        self.constraints = csp.constraints

        self.rows = csp.rows
        self.columns = csp.columns



        self.queue = deque()

    def initialize(self):
        for variable in self.variables:
            for focal_constraint in self.constraints[variable]:
                self.queue.append((self, variable, focal_constraint))

    def domainFilter(self):
        while len(self.queue) > 0:
            focal_state, focal_variable, focal_constraint = self.queue.popleft()
            if self.revise(focal_state, focal_variable, focal_constraint):
                self.addAllTuples(focal_state, focal_variable, focal_constraint)

    def addAllTuples(self, focal_state, focal_variable, focal_constraint):
        for constraint in self.constraints[focal_variable]:
            if constraint != focal_constraint:
                for variable in constraint.get_other(focal_variable):
                    if variable != focal_variable:
                        self.queue.append((focal_state, constraint.get_other(focal_variable)[0], constraint))

    def addAllTuplesSpecificConstraint(self, focal_state, focal_variable):
        for focal_constraint in self.constraints[focal_variable]:
            for other_var in focal_constraint.get_other(focal_variable):
                if other_var != focal_variable:
                    print focal_state, other_var, focal_constraint
                    self.queue.append((focal_state, other_var, focal_constraint))

    def rerun(self, state, var):
        self.addAllTuplesSpecificConstraint(state, var)
        self.domainFilter()

    def revise(self, searchstate, statevariable, focal_constraint):
        revised = False
        for other_variable in focal_constraint.vertices:
            if other_variable != statevariable:
                boolset = set()
                for other_value in searchstate.domains[other_variable]:
                    boolset.add(other_value[statevariable.index])
                for value in searchstate.domains[statevariable]:
                    satisfies_constraint = False
                    for some_value in searchstate.domains[other_variable]:
                        if focal_constraint.function(value[other_variable.index], some_value[statevariable.index]):
                            satisfies_constraint = True
                            break
                    if not satisfies_constraint:
                        searchstate.domains[statevariable].remove(value)
                        revised = True
                    else:
                        if len(boolset) > 0:
                            if not value[other_variable.index] in boolset:
                                print "here"
                                searchstate.domains[statevariable].remove(value)

        return revised
