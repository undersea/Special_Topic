import sys
from decorator import decorator
import gtk

outstream = sys.stdout
isdebug = True

def dump(obj):
    for attr in dir(obj):
        if not attr.startswith('__') and not callable(getattr(obj, attr)):
            print >> outstream, '%s:' % attr, getattr(obj, attr)
    if isinstance(obj, gtk.ListStore):
        for row in obj:
            for x in row:
                print >> outstream, '%10s' % (str(x)),
            print >> outstream
    

def setDebug(attr):
    global isdebug
    isdebug = attr


def setOutstream(out):
    global outstream
    outstream = out


def debug(objdict):
    @decorator
    def decorate(func, *args, **kwargs):
        def wrap(*args, **kwargs):
            if isdebug:
                for x in objdict:
                    print >>outstream, ">>>", x, objdict[x]
                    dump(objdict[x])
                    print >>outstream, ">>> finished", x, objdict[x]
                print >>outstream, ">>> calling", getattr(func, '__name__')
            result = func(*args, **kwargs)
            if isdebug:
                print >>outstream, "<<< called", getattr(func, '__name__')
                for x in objdict:
                    print >>outstream, "<<<", x, objdict[x]
                    dump(objdict[x])
                    print >>outstream, "<<< finished", x, objdict[x]
            return result
        
        return wrap(*args, **kwargs)
        
    return decorate


if __name__ == "__main__":
    @debug([list()])
    def test():
        return True

    setDebug(False)
    print test()

    setDebug(True)
    print test()

    help(test)
