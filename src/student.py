Empty = 'Empty'


class Student(object):
    name = None
    papers = list()
    degree = None
    pass

        
    def __str__(self):
        return "%s: %s" % (str(self.name), str(self.papers))
    

    def __add__(self, obj):
        if isinstance(obj, list):
            self.papers.extend(obj)
        elif isinstance(obj, str):
            self.papers.append(obj)
            
        return self

    def __sub__(self, obj):
        if isinstance(obj, list):
            self.papers = [x for x in self.papers if x not in obj]
        elif isinstance(obj, str) and obj in self.papers:
            self.papers.remove(obj)

        return self


    def print_programme(self):
        """Prints out the papers that they have done so far.
        Assumes that 100 level papers come first, then 200 followed by 300 levels.
        Assumes 4 papers a semester.
        @TODO check to see which semester papers wer offered in so far.
        """
        level_1 = [x for x in self.papers if x[4:5] == '1']
        level_2 = [x for x in self.papers if x[4:5] == '2'] + level_1[8:]
        level_3 = [x for x in self.papers if x[4:5] == '3'] + level_2[8:]
        
        level_1 = level_1 + [Empty for x in range(8 - len(level_1))]
        level_2 = level_2 + [Empty for x in range(8 - len(level_2))]
        level_3 = level_3 + [Empty for x in range(8 - len(level_3))]


        print 'Year 1'.ljust(8), 'Year 2'.ljust(8), 'Year 3'.ljust(8)
        print '-'*8, '-'*8, '-'*8
        for x in range(4):
            print level_1[x].ljust(8), level_2[x].ljust(8), level_3[x].ljust(8)
        print '-'*8, '-'*8, '-'*8
        for x in range(4, 8):
            print level_1[x].ljust(8), level_2[x].ljust(8), level_3[x].ljust(8)
        print '-'*8, '-'*8, '-'*8


if __name__ == '__main__':
    stud = Student()
    stud.name = "James"
    
    print stud
    stud + ['159.101', '159.102'] + '161.201'
    """
    print stud - ['161.101', '159.102']
    print stud - '159.101'
    """
    stud.print_programme()
