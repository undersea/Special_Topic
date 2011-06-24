import sys

outstream = sys.stdout

def dump(obj):
    print >>outstream,">>>", obj
    for attr in dir(obj):
        print >> outstream, '%s:' % attr, getattr(obj, attr)
    print >>outstream, "<<<", obj



def 
