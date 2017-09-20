class CSP:

    rowVar = []
    colVar = []
    rowDomain = []
    colDomain = []
    constraints = []

    def __init__(self, filename):
        self.csp = self.loadFile(filename)

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

    def loadFile(self, filename):
        f = open(filename, 'r')
        columns, rows = [int(x) for x in f.readline().strip().split(' ')]

        print columns, rows
        print "Row"
        for row in reversed(range(rows)):
            segments = [int(x) for x in f.readline().strip().split(' ')]
            self.rowVar.append(segments)
            segment_domains = self.generate_segment_domains(segments, columns)
            print segment_domains
            self.rowDomain.append(segment_domains)

        print "---"
        print "Column"
        for column in range(columns):
            segments = [int(x) for x in f.readline().strip().split(' ')]
            self.colVar.append(segments)
            segment_domains = self.generate_segment_domains(segments, rows)
            print segment_domains
            self.colDomain.append(segment_domains)
        f.close()
        #print segments_domains


CSP = CSP("Nonograms/test.txt")
print CSP.rowVar
print CSP.colVar


#loadFile("Nonograms/nono-cat.txt")
