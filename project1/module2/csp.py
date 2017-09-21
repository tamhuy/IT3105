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

    def generateSegmentDomains(self, segments, length):
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

    def calculatePermutations(self, segment_domains, segments):
        permutations = list(itertools.product(*segment_domains))
        for list_element in copy.deepcopy(permutations):
            for i in range(len(list_element) - 1):
                if isinstance(list_element, tuple):
                    if not list_element[i] + segments[i] < list_element[i + 1]:
                        if list_element in permutations:
                            permutations.remove(list_element)
                            break
        return permutations

    def createArray(self, positionlist, lengthlist, length):
        return_array = [False] * length
        positionlist = list(positionlist)
        for i in range(len(positionlist)):
            for j in range(positionlist[i], positionlist[i] + lengthlist[i]):
                return_array[j] = True
        return return_array


    def loadFile(self, filename):
        f = open(filename, 'r')
        columns, rows = [int(x) for x in f.readline().strip().split(' ')]
        self.rows = rows
        self.columns = columns
        for row in reversed(range(rows)):
            segments = [int(x) for x in f.readline().strip().split(' ')]
            segment_domains = self.generateSegmentDomains(segments, columns)
            permutations = self.calculatePermutations(segment_domains, segments)
            domain_permutations = [self.createArray(x, segments, columns) for x in permutations]
            row = Variable(row, "row", columns)
            self.rowVar.append(row)
            self.variables.append(row)
            self.domains[row] = []
            for i in domain_permutations:
                if i not in self.domains[row]:
                    self.domains[row].append(i)


        for column in range(columns):
            segments = [int(x) for x in f.readline().strip().split(' ')]
            segment_domains = self.generateSegmentDomains(segments, rows)
            permutations = self.calculatePermutations(segment_domains, segments)
            domain_permutations = [self.createArray(x, segments, rows) for x in permutations]
            col = Variable(column, "column", rows)
            self.colVar.append(col)
            self.variables.append(col)
            self.domains[col] = []
            for i in domain_permutations:
                if i not in self.domains[col]:
                    self.domains[col].append(i)

        f.close()


