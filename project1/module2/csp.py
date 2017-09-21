import itertools
import copy
import GUI

from GAC import GAC


class Variable:
    def __init__(self, index, type, size):
        self.index = index
        self.type = type
        self.size = size

class Constraint:
    def __init__(self, vertices, expr):
        self.vertices = vertices
        self.expr = expr
        self.function = self.makefunc(["x","y"], self.expr)

    def makefunc(self, var_names, expression, envir=globals()):
        args = ",".join(var_names)
        return eval("(lambda " + args + ":" + expression + ")", envir)

    def get_other(self, var):

        if self.vertices[0] == var:
            return [self.vertices[1]]
        if self.vertices[1] == var:
            return [self.vertices[0]]
        else:
            raise AttributeError

class CSP:

    rowVar = []
    colVar = []
    variables = []
    domains = {}
    constraints = {}
    columns = 0
    rows = 0

    def __init__(self, filename):
        self.loadFile(filename)
        self.addConstraints()

    def addConstraints(self):
        for rowVar in self.rowVar:
            for colVar in self.colVar:
                #print rowVar.index
                #print colVar.index
                constraint = Constraint([rowVar, colVar], "x == y")
                if rowVar in self.constraints:
                    self.constraints[rowVar].append(constraint)
                else:
                    self.constraints[rowVar] = [constraint]

                if colVar in self.constraints:
                    self.constraints[colVar].append(constraint)
                else:
                    self.constraints[colVar] = [constraint]

    def generate_segment_domains(self, segments, length):
        """ Generate the initial domain ranges for segments in a row
        Args:
            :param segments:   list of segment sizes, e.g. [2, 1, 3]
            :param length:     the length of the row or column
        Returns:
            :return: a list of lists containing the ranges for each initial segment size, e.g.
            [[0, 1, 2], [3, 4, 5], [5, 6, 7]]
        """
        segment_start_ranges = [0]
        segment_end_ranges = []
        start_total = 0

        for i in range(1, len(segments)):
            start_total += segments[i - 1] + 1
            segment_start_ranges.append(start_total)

        for j in range(0, len(segments)):
            end_total = length + 1
            for k in range(j, len(segments)):
                end_total -= segments[k] + 1
            segment_end_ranges.append(end_total)

        segment_domains = []
        for k in range(len(segments)):
            segment_domains.append([x for x in range(segment_start_ranges[k], segment_end_ranges[k] + 1)])

        return segment_domains

    def calculate_permutations(self, segment_domains, segments):
        """ Calculate all the possible permutations of legal initial segment indexes
            for a row or column

        Args:
            :param segment_domains: a list of lists of ranges of the segments, as calculated
                                    in generate_segment_domains
            :param segments:        a list of segment sizes
        Returns:
            :return: a list of tuples representing all legal permutations of initial segment indices
        """
        permutations = list(itertools.product(*segment_domains))
        for list_element in copy.deepcopy(permutations):
            for i in range(len(list_element) - 1):
                if isinstance(list_element, tuple):
                    if not list_element[i] + segments[i] < list_element[i + 1]:
                        if list_element in permutations:
                            permutations.remove(list_element)
                            break
        return permutations

    def create_true_false_array(self, positionlist, lengthlist, length):
        """ Generate a list of boolean lists representing legal segment places on a row or column

        Args:
            :param positionlist:    a tuple of positions, e.g. one tuple generated in calculate_permutations
            :param lengthlist:      a list of segment sizes
            :param length:          the length of a given row or column
        Returns:
            :return: a list of boolean lists representing legal segment placements on a row or column, e.g.
                     [[T, T, T, T, T, T, F], [F, T, T, T, T, T, T]]
        """
        return_array = [False] * length
        positionlist = list(positionlist)
        for i in range(len(positionlist)):
            for j in range(positionlist[i], positionlist[i] + lengthlist[i]):
                return_array[j] = True
        return return_array


    def loadFile(self, filename):
        """ Initializes a CSP problem with variables and its domains

        Args:
            :param nonogram_file: a .txt file representing the nonogram grid and its segments

        Returns:
            :return: an instance of a mod3GAC object
        """
        #CNET = ConstraintNet()
        #csp = mod3GAC(CNET)
        f = open(filename, 'r')
        columns, rows = [int(x) for x in f.readline().strip().split(' ')]
        self.rows = rows
        self.columns = columns
        for row in reversed(range(rows)):
            segments = [int(x) for x in f.readline().strip().split(' ')]
            segment_domains = self.generate_segment_domains(segments, columns)
            permutations = self.calculate_permutations(segment_domains, segments)
            domain_permutations = [self.create_true_false_array(x, segments, columns) for x in permutations]
            #print domain_permutations
            row = Variable(row, "row", columns)
            self.rowVar.append(row)
            self.variables.append(row)
            self.domains[row] = []
            for i in domain_permutations:
                if i not in self.domains[row]:
                    self.domains[row].append(i)
            #print self.rowVar[0].type
            #print self.domain


        for column in range(columns):
            segments = [int(x) for x in f.readline().strip().split(' ')]
            segment_domains = self.generate_segment_domains(segments, rows)
            permutations = self.calculate_permutations(segment_domains, segments)
            domain_permutations = [self.create_true_false_array(x, segments, rows) for x in permutations]
            #print domain_permutations
            col = Variable(column, "column", rows)
            #print col.size
            self.colVar.append(col)
            self.variables.append(col)
            self.domains[col] = []
            for i in domain_permutations:
                if i not in self.domains[col]:
                    self.domains[col].append(i)

        #for i in self.rowVar:
         #   print self.domains[i]

        f.close()
        #return csp

# chick, clover, reindeer, sailboat, snail2, telephone

'''
print test.variables
for i in test.variables:
    print test.domains[i]
print test.revise(test, test.variables[1],test.constraints[test.variables[1]][4])

'''
#loadFile("Nonograms/nono-cat.txt")
