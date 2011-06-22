import sys, string, copy

import pygtk, gtk

import operators
import utility
from grammar import *


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


def cancel_action_activate_cb(action, *args):
    """
    Simply remove any proposed changes to the programme of study
    """
    print 'cancel'
    del add_papers[:], remove_papers[:]


def apply_action_activate_cb(action, *args):
    print 'apply'

    #get current programme
    programme = []
    [programme.extend([y for y in x if y is not None]) for x in planstore]
    #remove unwanted papers
    programme = [x for x in programme if x not in remove_papers]
    #add new papers
    programme.extend(add_papers)

    #sort by level into 3 separate lists (only supports up to 300 level)
    levels = []
    levels.append([x for x in programme if int(float(x) * 1000 % 1000) / 100 == 1])
    levels.append([y for y in programme if int(float(y) * 1000 % 1000) / 100 == 2])
    levels.append([z for z in programme if int(float(z) * 1000 % 1000) / 100 == 3])
             
    
    #separate then into semesters
    semesters = [[],[],[]]
    semesters[0].append([a for a in levels[0]
                         if PAPERS.has_key(a) and
                         'one' in [str(x[2].lower()) for x in PAPERS[a]['offerings']
                                   if str(x[1]).lower() == 'pnth']
                         ])

    semesters[0].append([b for b in levels[0]
                         if PAPERS.has_key(b) and
                         'two' in [str(x[2].lower()) for x in PAPERS[b]['offerings']
                                   if str(x[1]).lower() == 'pnth']
                         ])

    semesters[1].append([c for c in levels[1]
                         if PAPERS.has_key(c) and
                         'one' in [str(x[2].lower()) for x in PAPERS[c]['offerings']
                                   if str(x[1]).lower() == 'pnth']
                         ])

    semesters[1].append([d for d in levels[1]
                         if PAPERS.has_key(d) and
                         'two' in [str(x[2].lower()) for x in PAPERS[d]['offerings']
                                   if str(x[1]).lower() == 'pnth']
                         ])

    semesters[2].append([e for e in levels[2]
                         if PAPERS.has_key(e) and
                         'one' in [str(x[2].lower()) for x in PAPERS[e]['offerings']
                                   if str(x[1]).lower() == 'pnth']
                         ])

    semesters[2].append([f for f in levels[2]
                         if PAPERS.has_key(f) and
                         'two' in [str(x[2].lower()) for x in PAPERS[f]['offerings']
                                   if str(x[1]).lower() == 'pnth']
                         ])


    print 'semesters', semesters

    #clear the planner table of its current contents
    for row in range(len(planstore)):
        for column in range(len(planstore[row])):
            planstore[row][column] = None
        
    #do a count and make sure there is enough slots avalable
    #@TODO
    
    #repopulate the planner table
    appended = list()
    for year in range(len(semesters)):
        for semester in range(len(semesters[year])):
            slot = 0
            for paper in semesters[year][semester]:
                if paper not in appended:
                    planstore[(4 * semester) + slot][year] = paper
                    appended.append(paper)
                    slot += 1
            #we need to check for missing papers and add them to the next year planner list
    
def check_programme(modal):
    programme = []
    [programme.extend([y for y in x if y is not None]) for x in modal]

    #clear the list
    del missing[:]
    
    result = DEGREE.check_programme(major, programme)
    operators.reset_missing()
    #print 'passed rules =', result
    if not result:
        for x in DEGREE.rules:
            result = x.check(programme, DEGREE.schedule)
            if not result:
                missing.append((str(x), copy.deepcopy(operators.missing), result,))
            
            operators.reset_missing()
        for x in DEGREE.schedule[major][1]:
            result = x.check(programme, DEGREE.schedule[major][0])
            if not result:
                missing.append((str(x), copy.deepcopy(operators.missing), result,))
            operators.reset_missing()
    max_columns = 1
    rulestore.clear()
    for missed in missing:
        if len(missed[1]) > max_columns:
            max_columns = len(missed[1])
        it = rulestore.append((missed[0],))
    


def on_rule_selected(tree):#, str_path, new_iter, *data):
    global reportstore
    for column in report_tree.get_columns():
        report_tree.remove_column(column)
    report_tree.set_model(None)
    store, store_iter = tree.get_selection().get_selected()
    store_path = store.get_path(store_iter)
    #print 'rule_selected', store, store_iter, store_path[0]#, str_path, new_iter, data
    data = missing[store_path[0]]
    if len(data[1]) == 0:
        print 'returning as', len(data[1])
        return #don't process a empty list
    dtypes = (bool,) + ((str, bool)*len(data[1]))
    print dtypes
    model = report_tree.get_model()
    del model
    report_tree.set_model(None)

    if len(dtypes) == 0:
        return
    reportstore = gtk.ListStore(*dtypes)
    papers = utility.tuple_to_list(data[1])
    print papers
    for x in range(len(papers)):
        if papers[x][0] in add_papers:
            papers[x][1] = True
            
    tmp = string.join([x for x in string.join(str(papers), '') if x not in "[()]'"], '')
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
    

def on_planstore_row_changed(model, str_path, new_iter):
    #print model, type(str_path), str_path, new_iter
    check_programme(model)


def on_year_cellcombo_1_changed(combo, str_path, new_iter, *data):
    print 'path', str_path
    it = planstore.get_iter(str_path)
    tmp = paperstore.get_value(new_iter, 0)
    
    planstore.set_value(it, 0, tmp)


def on_year_cellcombo_2_changed(combo, str_path, new_iter, *data):
    print 'path', str_path
    it = planstore.get_iter(str_path)
    tmp = paperstore.get_value(new_iter, 0)
    planstore.set_value(it, 1, tmp)



def on_year_cellcombo_3_changed(combo, str_path, new_iter, *data):
    it = planstore.get_iter(str_path)
    tmp = paperstore.get_value(new_iter, 0)
    planstore.set_value(it, 2, tmp)



def fillinplan():
    
    programme = tuple([])
    tmpx = 0
    tmpy = 0
    for x in DEGREE.rules:
        
        result = x.check(programme, DEGREE.schedule)
        if not result:
            if  string.find(str(x), 'or') == -1 and len([y for y in operators.missing
                                                        if 'x' not in y]) == len(operators.missing):
                print 'fillplan 1', string.find(str(x), 'or'), operators.missing
                # assume and so include all papers
                missing = copy.deepcopy(operators.missing) # ensures the list does not just disappear
                for z in missing:
                    it = planstore.get_iter(str(tmpy))
                    planstore.set_value(it, tmpx, z[0])
                    #operators.missing seem to just reset here to []

                    if tmpy < 8:
                        tmpy += 1
                    else:
                        tmpy = 0
                        tmpx += 1
                        
        operators.reset_missing()
        
    if __debug == True:
        pdb.set_trace()
    for x in DEGREE.schedule[major][1]:
        result = x.check(programme, DEGREE.schedule[major][0])
        if not result:
            if string.find(str(x), 'or') == -1 and len([y[0] for y in operators.missing
                                                        if 'x' not in y[0]]) == len(operators.missing):
                print 'fillplan 2', str(x), string.find(str(x), 'or'), operators.missing
                missing = copy.deepcopy(operators.missing)
                # assume and so include all papers
                for z in missing:
                    it = planstore.get_iter(str(tmpy))
                    planstore.set_value(it, tmpx, z[0])

                    if tmpy < 8:
                        tmpy += 1
                    else:
                        tmpy = 0
                        tmpx += 1
                        
        operators.reset_missing()
    
    apply_action_activate_cb(None)



if __name__ == '__main__':
    global PAPERS, DEGREE
    parse_tags('papers/tags.xml')
    DEGREE = parse("BSc.xml")
    builder = gtk.Builder()
    builder.add_from_file('interface.glade')
    
    main_window = builder.get_object('window1')

    paperstore = builder.get_object('paperstore')
    planstore = builder.get_object('planstore')

    reportstore = builder.get_object('reportstore')

    rulestore = builder.get_object('rulestore')

    rules_tree = builder.get_object('rules_tree')

    report_tree = builder.get_object('report_tree')

    PAPERS = parse_papers('papers/papers.xml')



    keys = [x for x in PAPERS.keys()
            if 'pnth' in [str(str(y[1]).lower()) for y in PAPERS[x]['offerings']]
            ]
    keys.sort()

    for x in keys:
        paperstore.append((x,))
    
    sigs = builder.connect_signals({'gtk_main_quit': gtk.main_quit, 'on_year_cellcombo_3_changed': on_year_cellcombo_3_changed, 'on_year_cellcombo_2_changed':on_year_cellcombo_2_changed, 'on_year_cellcombo_1_changed': on_year_cellcombo_1_changed, 'on_planstore_row_changed': on_planstore_row_changed, 'on_rule_selected': on_rule_selected, 'cancel_action_activate_cb': cancel_action_activate_cb, 'apply_action_activate_cb': apply_action_activate_cb })

    fillinplan()
    
    main_window.show()

    

    gtk.main()
    
