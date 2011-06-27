import sys, string, copy

from debug.stats import debug, setOutstream, setDebug

import pygtk, gtk

import operators
import utility
import widgets

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


def add_paper(widget, row, column, *data):
    print widget, row, column, data
    
    model = column.get_tree_view().get_model()
    new_iter = model.get_iter_from_string(str(row))
    print 'value:', model.get_value(new_iter, 0)
    try:
        float(model.get_value(new_iter, 0))
    except:
        pass
    else:
        add_papers.append(model.get_value(new_iter, 0))
        apply_action.activate()
        fillinplan()


def display_info(widget, row, column, *data):
    print widget, row, column, data


    pass


def on_plancell_edit_1(renderer, npath, new_text, *data):
    print data, npath
    niter = planstore.get_iter_from_string(npath)
    try:
        paper = PAPERS[new_text]
        
        if len([x for x in paper['offerings']
                if (x[1] is not None and
                    str(x[1].lower()) == 'pnth')]) > 0  or len(new_text) == 0:
            planstore.set_value(niter, 0, new_text)
        else:
            print new_text, 'Does not contain a palmerston north offering'
    except:
        if len(new_text) == 0:
            planstore.set_value(niter, 0, new_text)
        else:
            print new_text, 'is not a valid paper'
    pass


def on_plancell_edit_2(renderer, npath, new_text, *data):
    print data, npath, len(new_text), new_text, type(new_text)
    niter = planstore.get_iter_from_string(npath)
    try:
        paper = PAPERS[new_text]
        
        if len([x for x in paper['offerings']
                if (x[1] is not None and
                    str(x[1].lower()) == 'pnth')]) > 0  or len(new_text) == 0:
            planstore.set_value(niter, 1, new_text)
        else:
            print new_text, 'Does not contain a palmerston north offering'
    except:
        if len(new_text) == 0:
            planstore.set_value(niter, 1, new_text)
        else:
            print new_text, 'is not a valid paper'
    pass


def on_plancell_edit_3(renderer, npath, new_text, *data):
    print data, npath
    niter = planstore.get_iter_from_string(npath)
    try:
        paper = PAPERS[new_text]
        
        if len([x for x in paper['offerings']
                if (x[1] is not None and
                    str(x[1].lower()) == 'pnth')]) > 0  or len(new_text) == 0:
            planstore.set_value(niter, 2, new_text)
        else:
            print new_text, 'Does not contain a palmerston north offering'
    except:
        if len(new_text) == 0:
            planstore.set_value(niter, 2, new_text)
        else:
            print new_text, 'is not a valid paper'



if __name__ == '__main__':
    global PAPERS, DEGREE
    setDebug(True)
    debug_file = open('debug.txt', 'w')
    setOutstream(debug_file)
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

    treeviewcolumn7 = builder.get_object('treeviewcolumn7')
    widgets.add_button(2, treeviewcolumn7, add_paper)

    treeviewcolumn8 = builder.get_object('treeviewcolumn8')
    widgets.add_button(3, treeviewcolumn8, display_info)

    paper_choice_store = builder.get_object('paper_choice_store')

    PAPERS = parse_papers('papers/papers.xml')
    TAGS = tagsdict

    

    keys = [x for x in PAPERS.keys()
            if 'pnth' in [str(str(y[1]).lower()) for y in PAPERS[x]['offerings']]
            ]
    keys.sort()

    for tag_key in TAGS:
        if TAGS[tag_key][2] != 'template':
            paper_choice_store.append(("%s" % (TAGS[tag_key][0]), None, None, None, 20))
            for code in [x for x in TAGS[tag_key][1] if x in keys]:
                paper_choice_store.append((code, PAPERS[code]['name'],
                                           'images/add_button.png',
                                           'images/info_button.png', 16))

    for x in keys:
        paperstore.append((x,))
    

    apply_action = builder.get_object('apply_action')


def cancel_action_activate_cb(action, *args):
    """
    Simply remove any proposed changes to the programme of study
    """
    print 'cancel'
    del add_papers[:], remove_papers[:]


def get_prerequisites(code, programme):
    """
    return only papers that are not a choice of this or that
    add the rest as a rule to rulesstore
    """
    #clear the list
    del missing[:]
    
    paper = PAPERS[code]
    rule = paper['prerequisites']
    if rule != None:
        result = rule.check(programme)
        if (result == False and
            string.find(str(rule), 'or') == -1 and
            len([y for y in operators.missing
                 if 'x' not in y]) == len(operators.missing)):
            rulestore.append((str(rule), DEGREE.name,
                              copy.deepcopy(operators.missing), result,))
            operators.reset_missing()
            return list()
        missing = copy.deepcopy(operators.missing)
        operators.reset_missing()
        return [x for x, y in missing if not isinstance(x, bool)]

    return list()

@debug({'planstore':planstore, 'rulesstore': rulestore,})
def apply_action_activate_cb(action, *args):
    print 'apply', action, args

    #get current programme
    programme = []
    [programme.extend([y for y in x if y is not None and len(y) > 0]) for x in planstore]
    #remove unwanted papers
    programme = [x for x in programme if x not in remove_papers and x != '']
    #add new papers
    programme.extend(add_papers)

    #make sure no duplicates are present
    programme = set(programme)

    print programme

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
                                   if (x[1] is not None and
                                       str(x[1]).lower() == 'pnth')]
                         ])

    semesters[0].append([b for b in levels[0]
                         if PAPERS.has_key(b) and
                         'two' in [str(x[2].lower()) for x in PAPERS[b]['offerings']
                                   if (x[1] is not None and
                                       str(x[1]).lower() == 'pnth')]
                         ])

    semesters[1].append([c for c in levels[1]
                         if PAPERS.has_key(c) and
                         'one' in [str(x[2].lower()) for x in PAPERS[c]['offerings']
                                   if str(x[1]).lower() == 'pnth']
                         ])

    semesters[1].append([d for d in levels[1]
                         if PAPERS.has_key(d) and
                         'two' in [str(x[2].lower()) for x in PAPERS[d]['offerings']
                                   if (x[1] is not None and
                                       str(x[1]).lower() == 'pnth')]
                         ])

    semesters[2].append([e for e in levels[2]
                         if PAPERS.has_key(e) and
                         'one' in [str(x[2].lower()) for x in PAPERS[e]['offerings']
                                   if (x[1] is not None and
                                       str(x[1]).lower() == 'pnth')]
                         ])

    semesters[2].append([f for f in levels[2]
                         if PAPERS.has_key(f) and
                         'two' in [str(x[2].lower()) for x in
                                   PAPERS[f]['offerings']
                                   if (x[1] is not None and
                                       str(x[1]).lower() == 'pnth')]
                         ])

    

    #clear the planner table of its current contents
    for row in range(len(planstore)):
        for column in range(len(planstore[row])):
            planstore[row][column] = None
        
    #do a count and make sure there is enough slots avalable
    #@TODO
    sort_overflows(semesters, 0, 0)
    sort_overflows(semesters, 1, 0)
    #sort_overflows(semesters, 2, 0)

    sort_overflows(semesters, 0, 1)
    sort_overflows(semesters, 1, 1)
    #sort_overflows(semesters, 2, 1)

    
    print semesters
    
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

def sort_overflows(semesters, year, semester):
    if len(semesters[year][semester]) == 0:
        return
    tmp = semesters[year][semester].pop()
    semesters[year][semester].insert(0, tmp) #put back at begining
    paper = None
    while (len(semesters[year][semester]) > 4 and
           tmp != paper):
        paper = semesters[year][semester].pop()
        if not check_if_prerequisite(paper, semesters[1][0]):
            semesters[year+1][semester].append(paper)
        else:
            semesters[year][semester].insert(0, paper)


def check_if_prerequisite(paper, semesters):
    return False

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
                missing.append((str(x), DEGREE.name, copy.deepcopy(operators.missing), result,))
            
            operators.reset_missing()
        for x in DEGREE.schedule[major][1]:
            result = x.check(programme, DEGREE.schedule[major][0])
            if not result:
                missing.append((str(x), major, copy.deepcopy(operators.missing), result,))
            operators.reset_missing()
    for code in programme:
        try:
            rule = PAPERS[code]['prerequisites']
        except:
            pass
        else:
            if rule != None:
                result = rule.check(programme)
                if not result:
                    missing.append((str(rule), code, copy.deepcopy(operators.missing), result,))
                        
                operators.reset_missing()
    max_columns = 1
    rulestore.clear()
    for missed in missing:
        if len(missed[1]) > max_columns:
            max_columns = len(missed[2])
        it = rulestore.append((missed[0],missed[1], "TODO"))
    


def on_rule_selected(tree):#, str_path, new_iter, *data):
    global reportstore
    for column in report_tree.get_columns():
        report_tree.remove_column(column)
    report_tree.set_model(None)
    store, store_iter = tree.get_selection().get_selected()
    store_path = store.get_path(store_iter)

    data = missing[store_path[0]]
    if len(data[2]) == 0:
        print 'returning as length of missing papers is', len(data[2])
        return #don't process a empty list
    dtypes = (bool,) + ((str, bool)*len(data[2]))
    print dtypes
    model = report_tree.get_model()
    del model
    report_tree.set_model(None)

    if len(dtypes) == 0:
        return
    reportstore = gtk.ListStore(*dtypes)
    papers = utility.tuple_to_list(data[2])
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
    print 'tmp', tmp
    reportstore.append(tmp)
    

    report_tree.set_model(reportstore)
    
    for x in range((len(tmp)-1)/2):
        str_render = gtk.CellRendererText()
        str_column = gtk.TreeViewColumn("Paper", str_render, text=range(len(tmp))[1::2][x])
        report_tree.append_column(str_column)
        bool_column = gtk.TreeViewColumn("Enrol?")

        if 'x' not in tmp[range(len(tmp))[1::2][x]]:
            bool_render = gtk.CellRendererToggle()
            #bool_render.set_radio(False)
        
            bool_render.connect('toggled', on_paper_missing_toggled, range(len(tmp))[2::2][x], reportstore)
            bool_column.pack_start(bool_render)
            bool_column.add_attribute(bool_render, 'active', int(range(len(tmp))[2::2][x]))
        
            
        #bool_column.set_clickable(True)
        report_tree.append_column(bool_column)

    str_column = gtk.TreeViewColumn()
    report_tree.append_column(str_column)




def on_paper_missing_toggled(cell, new_path, column, model):
    if __debug == True:
        pdb.set_trace()
    programme = []
    [programme.extend([y for y in x if y is not None]) for x in planstore]
    new_iter = model.get_iter(new_path)
    paper = model.get_value(new_iter, int(column)-1)
    enrolled = model.get_value(new_iter, int(column))
    if not enrolled:
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

    apply_action.activate()
    


def on_planstore_row_changed(model, str_path, new_iter):
    #print model, type(str_path), str_path, new_iter
    check_programme(model)





def fillinplan():
    programme = []
    [programme.extend([y for y in x if y is not None and len(y) > 0]) for x in planstore]
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
    #get current programme
    programme = []
    [programme.extend([y for y in x if y is not None and len(y) > 0]) for x in planstore]
    for code in programme:
        rule = PAPERS[code]['prerequisites']
        if rule != None:
            result = rule.check(programme)
            if not result:
                if (string.find(str(rule), 'or') == -1 and
                    len([y[0] for y in operators.missing
                         if 'x' not in y[0]]) == len(operators.missing)):
                
                    missing = copy.deepcopy(operators.missing)
                    # assume and so include all papers
                    for z in missing:
                        it = planstore.get_iter(str(tmpy))
                        planstore.set_value(it, tmpx, z[0])

                        if tmpy < 8:
                            tmpy += 1
                        else:
                            if temx < 3:
                                tmpy = 0
                                tmpx += 1
                            else:
                                print 'ran out of space, to many papers'
                                break
                        
                    operators.reset_missing()
    
    apply_action.activate()

    

if __name__ == "__main__":
    sigs = builder.connect_signals({'gtk_main_quit': gtk.main_quit, 'on_planstore_row_changed': on_planstore_row_changed, 'on_rule_selected': on_rule_selected, 'cancel_action_activate_cb': cancel_action_activate_cb, 'apply_action_activate_cb': apply_action_activate_cb, 'on_possible_activated': widgets.on_possible_activated, 'on_plancell_edit_1': on_plancell_edit_1, 'on_plancell_edit_2': on_plancell_edit_2, 'on_plancell_edit_3': on_plancell_edit_3 })

    fillinplan()
    
    main_window.show()

    

    gtk.main()

    debug_file.close()
