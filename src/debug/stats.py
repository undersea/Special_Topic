import sys
from decorator import decorator

outstream = sys.stdout
isdebug = True

def dump(obj):
    for attr in dir(obj):
        print >> outstream, '%s:' % attr, getattr(obj, attr)
    

def setDebug(attr):
    global isdebug
    isdebug = attr


def debug(objlist):
    @decorator
    def decorate(func):
        def wrap(*args, **kwargs):
            if isdebug:
                for x in objlist:
                    print >>outstream, ">>>", type(x), x
                    dump(x)
                    print >>outstream, ">>> finished", type(x), x
            result = func(*args, **kwargs)
            if isdebug:
                for x in objlist:
                    print >>outstream, "<<<", x
                    dump(x)
                    print >>outstream, "<<< finished", x
            return result
        
        return wrap()
        
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
