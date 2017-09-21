from collections import deque


class GAC():
    def __init__(self, CSP):
        self.variables = CSP.variables
        self.domains = CSP.domains
        self.constraints = CSP.constraints
        self.rows = CSP.rows
        self.columns = CSP.columns
        self.queue = deque()

    def generate_initial_searchstate(self):
        return NoNoState(self.domains)

    def initialize(self):
        for variable in self.variables:
            for focal_constraint in self.constraints[variable]:
                self.queue.append((self, variable, focal_constraint))

    def domainFilter(self):
        while len(self.queue) > 0:
            focal_state, focal_variable, focal_constraint = self.queue.popleft()
            if self.revise(focal_state, focal_variable, focal_constraint):
                self.add_all_tuples_in_which_variable_occurs(focal_state, focal_variable, focal_constraint)

    def add_all_tuples_in_which_variable_occurs(self, focal_state, focal_variable, focal_constraint):
        for constraint in self.constraints[focal_variable]:
            if constraint != focal_constraint:
                for variable in constraint.get_other(focal_variable):
                    if variable != focal_variable:
                        self.queue.append((focal_state, constraint.get_other(focal_variable)[0], constraint))

    def rerun(self):
        pass

    def revise(self, searchstate, statevariable, focal_constraint):
        """ Revise the domain of a variable based on the domains of a constraint

        Args:
            :param searchstate: the current search state
            :param statevariable: the focal variable on which to revise its domain (x)
            :param focal_constraint: the constraint used to determine which of the focal variables domains to remove (C)
        Returns:
            :return: Boolean indicating whether the focal variable was revised or not
        Comment:
            This revise function assumes that the domain of a variable is a list of lists containing T/F variables
            EXAMPLE:
            [
            [T,F,T,T,T,T,F,T]
            [T,T,T,T,F,F,F,F]
            [F,F,T,F,T,T,F,F]
            ]
        """
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
