from grammar import *
import operators
import pygtk, gtk, cairo, gobject
import sys, string

__debug = False

if __debug == True:
    import pdb

#assert that the required version is available
try:
    pygtk.require20()
except AssertionError, e:
    print "Required verion of pygtk not available"
    print e
    sys.exit(1)

major = 'Computer Science'
missing = []
add_papers = []
remove_papers = []

def check_programme(modal):
    programme = []
    [programme.extend([y for y in x if y is not None]) for x in modal]

    #clear the list
    del missing[:]
    
    result = degree.check_programme(major, programme)
    operators.reset_missing()
    print 'passed rules =', result
    if not result:
        for x in degree.rules:
            result = x.check(programme, degree.schedule)
            if not result:
                missing.append((str(x), operators.missing, result,))
            
            operators.reset_missing()
        for x in degree.schedule[major][1]:
            result = x.check(programme, degree.schedule[major][0])
            if not result:
                missing.append((str(x), operators.missing, result,))
            operators.reset_missing()
    max_columns = 1
    rulestore.clear()
    for missed in missing:
        if len(missed[1]) > max_columns:
            max_columns = len(missed[1])
        it = rulestore.append((missed[0],))
    


def on_rule_selected(tree):#, str_path, new_iter, *data):
    global reportstore
    store, store_iter = tree.get_selection().get_selected()
    store_path = store.get_path(store_iter)
    print 'rule_selected', store, store_iter, store_path[0]#, str_path, new_iter, data
    data = missing[store_path[0]]
    dtypes = (bool,) + ((str, bool)*len(data[1]))
    print dtypes
    model = report_tree.get_model()
    del model
    report_tree.set_model(None)

    if len(dtypes) == 0:
        return
    reportstore = gtk.ListStore(*dtypes)
    tmp = string.join([x for x in string.join(str(data[1]), '') if x not in "[()]'"], '')
    def convert(x):
            tmp = x.strip()
            if tmp == 'True':
                return 1
            elif tmp == 'False':
                return 0
            else:
                return tmp
        
    tmp = [True] + [convert(x) for x in tmp.split(',')]
    reportstore.append(tmp)
    
    for column in report_tree.get_columns():
        report_tree.remove_column(column)
    report_tree.set_model(reportstore)
    
    for x in range((len(tmp)-1)/2):
        str_render = gtk.CellRendererText()
        str_column = gtk.TreeViewColumn("Paper", str_render, text=range(len(tmp))[1::2][x])
        report_tree.append_column(str_column)
        bool_render = gtk.CellRendererToggle()
        #bool_render.set_radio(False)
        
        bool_render.connect('toggled', on_paper_missing_toggled, range(len(tmp))[2::2][x], reportstore)
        bool_column = gtk.TreeViewColumn("Enrol?")
        bool_column.pack_start(bool_render)
        bool_column.add_attribute(bool_render, 'active', int(range(len(tmp))[2::2][x]))
                                         
        
            
        #bool_column.set_clickable(True)
        report_tree.append_column(bool_column)


def on_paper_missing_toggled(cell, new_path, column, model):
    if __debug == True:
        pdb.set_trace()
    programme = []
    [programme.extend([y for y in x if y is not None]) for x in planstore]
    new_iter = model.get_iter(new_path)
    paper = model.get_value(new_iter, int(column)-1)
    enrolled = model.get_value(new_iter, int(column))
    if not enrolled:
        print 'paper not in programme', (paper not in programme)
        print programme
        if paper not in programme:
            add_papers.append(paper)
        if paper in remove_papers:
            remove_papers.remove(paper)
    else:
        if paper in programme:
            remove_papers.append(paper)
        if paper in add_papers:
            add_papers.remove(paper)
    model.set_value(new_iter, int(column), not cell.get_active())

    print 'add', add_papers
    print 'remove', remove_papers
    

def on_planstore_row_changed(modal, str_path, new_iter):
    print modal, type(str_path), str_path, new_iter
    check_programme(modal)


def on_year_cellcombo_1_changed(combo, str_path, new_iter, *data):
    print str_path
    it = planstore.get_iter(str_path)
    tmp = paperstore.get_value(new_iter, 0)
    planstore.set_value(it, 0, tmp)


def on_year_cellcombo_2_changed(combo, str_path, new_iter, *data):
    it = planstore.get_iter(str_path)
    tmp = paperstore.get_value(new_iter, 0)
    planstore.set_value(it, 1, tmp)



def on_year_cellcombo_3_changed(combo, str_path, new_iter, *data):
    it = planstore.get_iter(str_path)
    tmp = paperstore.get_value(new_iter, 0)
    planstore.set_value(it, 2, tmp)


if __name__ == '__main__':
    parse_tags('papers/tags.xml')
    degree = degree = parse("BSc.xml")
    builder = gtk.Builder()
    builder.add_from_file('interface.glade')
    
    main_window = builder.get_object('window1')

    paperstore = builder.get_object('paperstore')
    planstore = builder.get_object('planstore')

    reportstore = builder.get_object('reportstore')

    rulestore = builder.get_object('rulestore')

    rules_tree = builder.get_object('rules_tree')

    report_tree = builder.get_object('report_tree')

    papers = parse_papers('papers/papers.xml')


    #print paperstore

    keys = papers.keys()
    keys.sort()

    for x in keys:
        paperstore.append((x,))
    
    sigs = builder.connect_signals({'gtk_main_quit': gtk.main_quit, 'on_year_cellcombo_3_changed': on_year_cellcombo_3_changed, 'on_year_cellcombo_2_changed':on_year_cellcombo_2_changed, 'on_year_cellcombo_1_changed': on_year_cellcombo_1_changed, 'on_planstore_row_changed': on_planstore_row_changed, 'on_rule_selected': on_rule_selected })


    
    main_window.show()

    

    gtk.main()
    
