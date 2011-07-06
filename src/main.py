#!/usr/bin/env python


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
    pygtk.require('2.0')
except AssertionError, e:
    print "Required verion of pygtk not available"
    print e
    sys.exit(1)

major = 'Computer Science'
missing = []
add_papers = []
remove_papers = []
Extra_Papers = []

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
    apply_action.activate()
    fillinplan()


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
    apply_action.activate()
    fillinplan()


def on_plancell_edit_3(renderer, npath, new_text, *data):
    print data, npath
    niter = planstore.get_iter_from_string(npath)
    try:
        paper = PAPERS[new_text]
        
        if len([x for x in paper['offerings']
                if (x[1] is not None and
                    str(x[1].lower()) == 'pnth')]) > 0  or len(new_text) == 0:
            planstore.set_value(niter, 2, "%s %s" % (new_text, paper['name'][:10]))
        else:
            print new_text, 'Does not contain a palmerston north offering'
    except:
        if len(new_text) == 0:
            planstore.set_value(niter, 2, new_text)
        else:
            print new_text, 'is not a valid paper'

    apply_action.activate()
    fillinplan()

def on_major_filter_changed(widget, *data):
	print 'on_major_filter_changed:', widget, data
	print major_store[widget.get_active()][1]
	
	paper_choice_store.clear()
	if major_store[widget.get_active()][1] == None:
		add_tag ()
	else:
		add_tag (major_store[widget.get_active()][1])

def fill_major_store():
	for tag_key in TAGS:
		if TAGS[tag_key][2] != 'template':
			major_store.append((str(TAGS[tag_key][0]), tag_key,))
	
def add_tag(tag='All'):
	print 'tag:', tag
	if tag == 'All' or len(tag) == 0:
		for tag_key in TAGS:
		    if TAGS[tag_key][2] != 'template':
		        print tag_key
		        paper_choice_store.append(("%s" % (TAGS[tag_key][0]), '', None, None, None, 20))
		        for code in [x for x in TAGS[tag_key][1] if x in keys]:
		            semesters = string.join([x[2] for x in PAPERS[code]['offerings']
		                                     if (x[1] is not None and
		                                         str(x[1].lower()) == 'pnth')], ',')
		            paper_choice_store.append((code, PAPERS[code]['name'], semesters,
		                                       'images/add_button.png',
		                                       'images/info_button.png', 16))
		        
		        paper_choice_store.append(([None]*5)+[0])
	else:
		tag_key = tag
		if TAGS[tag_key][2] != 'template':
		    paper_choice_store.append(("%s" % (TAGS[tag_key][0]), '', None, None, None, 20))
		    for code in [x for x in TAGS[tag_key][1] if x in keys]:
		        semesters = string.join([x[2] for x in PAPERS[code]['offerings']
		                                 if (x[1] is not None and
		                                     str(x[1].lower()) == 'pnth')], ',')
		        paper_choice_store.append((code, PAPERS[code]['name'], semesters,
		                                   'images/add_button.png',
		                                   'images/info_button.png', 16))
		    
		    paper_choice_store.append(([None]*5)+[0])
	
	
if __name__ == '__main__':
    global PAPERS, DEGREE
    setDebug(True)
    debug_file = open('debug.txt', 'w')
    setOutstream(debug_file)
    parse_tags('papers/tags.xml')
    DEGREE = parse("BSc.xml")
    builder = gtk.Builder()
    builder.add_from_file('interface.glade')

    extras_buffer = builder.get_object('extras_textbuffer')
    
    main_window = builder.get_object('window1')

    paperstore = builder.get_object('paperstore')
    planstore = builder.get_object('planstore')

    reportstore = builder.get_object('reportstore')

    rulestore = builder.get_object('rulestore')

    rules_tree = builder.get_object('rules_tree')

    report_tree = builder.get_object('report_tree')

    treeviewcolumn7 = builder.get_object('treeviewcolumn7')
    widgets.add_button(3, treeviewcolumn7, add_paper)

    treeviewcolumn8 = builder.get_object('treeviewcolumn8')
    widgets.add_button(4, treeviewcolumn8, display_info)

    paper_choice_store = builder.get_object('paper_choice_store')

    PAPERS = parse_papers('papers/papers.xml')
    TAGS = tagsdict

    major_store = builder.get_object('major_store')

    keys = [x for x in PAPERS.keys()
            if ('pnth' in [str(str(y[1]).lower()) for y in PAPERS[x]['offerings']])
            ]
    keys.sort()

    
    
    add_tag()

    fill_major_store()


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
    global missing
    #clear the list
    del missing[:]
    
    paper = PAPERS[code]
    rule = paper['prerequisites']
    if rule != None:
        result = rule.check(programme)
        """
        if (result == False and
            string.find(str(rule), 'or') == -1 and
            len([y for y in operators.missing
                 if 'x' not in y]) == len(operators.missing)):
            rulestore.append((str(rule), DEGREE.name,
                              copy.deepcopy(operators.missing), result,))
            missing.append((str(x), DEGREE.name,
                            copy.deepcopy(operators.missing), result,))
            operators.reset_missing()
            return list()
        """
        missing = copy.deepcopy(operators.missing)
        operators.reset_missing()
        return [x for x, y in missing if not isinstance(x, bool)]

    return list()

@debug({'Extra_Papers': Extra_Papers, 'planstore':planstore, 'rulesstore': rulestore,})
def apply_action_activate_cb(action, *args):
    print 'apply', action, args

    #get current programme
    programme = []
    [programme.extend([y.split()[0] for y in x if y is not None and len(y) > 0]) for x in planstore]
    #remove unwanted papers
    programme = [x for x in programme if x not in remove_papers and x != '']
    #add new papers
    programme.extend(add_papers)

    #make sure no duplicates are present and the extras are included
    programme = set(programme)
    programme.update(Extra_Papers)

    #remove previous extras
    del Extra_Papers[:]
    
    #sort by level into 3 separate lists (only supports up to 300 level)
    levels = []

    levels.append([x.split(' ')[0]
                   for x in programme
                   if int(float(x.split(' ')[0]) * 1000 % 1000) / 100 == 1])
    levels.append([y.split(' ')[0]
                   for y in programme
                   if int(float(y.split(' ')[0]) * 1000 % 1000) / 100 == 2])
    levels.append([z.split(' ')[0]
                   for z in programme
                   if int(float(z.split(' ')[0]) * 1000 % 1000) / 100 == 3])
             
    
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
    #fix papers like 160.101 and others prerequisite requirements
    sort_prerequisites(semesters, 0, 0)
    sort_prerequisites(semesters, 0, 1)
    sort_prerequisites(semesters, 1, 0)
    sort_prerequisites(semesters, 1, 1)
    
    sort_overflows(semesters, 0, 0)
    sort_overflows(semesters, 0, 1)
    
    sort_overflows(semesters, 1, 0)
    sort_overflows(semesters, 1, 1)

    
    
    
    #repopulate the planner table
    appended = list()
    for year in range(len(semesters)):
        for semester in range(len(semesters[year])):
            slot = 0
            semester_papers = list(set(semesters[year][semester]))
            for paper in semester_papers:
                if paper not in appended:
                    planstore[(4 *
                               semester) +
                               slot][year] = (
                        			"%s %s" % (paper,
                                   	PAPERS[paper]['name'])
                        	 )
                    appended.append(paper)
                    slot += 1
            #we need to check for missing papers and add them to the next year planner list
            if len(semester_papers) > 4:
                Extra_Papers.extend(semester_papers[4:])
    print Extra_Papers
    if len(Extra_Papers) > 0:
        extras_buffer.set_text("Papers That have dropped off\n%s" % 
                                (string.join(Extra_Papers, ', ')))
    else:
        extras_buffer.set_text('')
    del add_papers[:]
    del remove_papers[:]
                
def has_prerequisite(paper, programme):
    prereqs = get_prerequisites(paper, [])
    for tmp in prereqs:
        if tmp in programme:
            return True
    return False


def sort_prerequisites(semesters, year, semester):
    if len(semesters[year][semester]) == 0:
        return
    
    done = False
    while not done:
        again = False
        for yr in range(year + 1):
            for sem in range(semester + 1):
                if len(semesters[yr][sem]) == 0:
                    break
                tmp = semesters[yr][sem].pop()
                semesters[yr][sem].insert(0, tmp) #put back at begining
                paper = None
                while tmp != paper:
                    paper = semesters[yr][sem].pop()
                    same = False
                    for yr2 in range(yr, 3):
                        for sem2 in range(sem, 2):
                            if has_prerequisite(paper, semesters[yr2][sem2]):
                                #maybe it's available in semester 2
                                if (sem2 == 0 and
                                    len([x for x in PAPERS[paper]['offerings']
                                         if (x[2] is not None and
                                             str(x[2].lower()) == 'two')]) > 0):
                                    semesters[yr2][sem2+1].append(paper)
                                #otherwise put it in next years offerings
                                elif yr2 != 2:
                                    if len([x for x in PAPERS[paper]['offerings']
                                            if (x[2] is not None and
                                                str(x[2].lower()) == 'one')]) > 0:
                                        semesters[yr2+1][0].append(paper)
                                    else:
                                        semesters[yr2+1][1].append(paper)
                                else:
                                    raise ConstraintException(
                                        "%s can't be included" %
                                        paper)
                                again = True
                                same = False
                                break
                            
                            else:
                                same = True
                        
                        if again:
                            break
                    if same:
                        semesters[yr][sem].insert(0, paper)
                    if again:
                        break
        else:
           
            done = True
            


    



def sort_overflows(semesters, year, semester):
    if len(semesters[year][semester]) == 0:
        return
    #remove duplicates
    semesters[year][semester] = list(set(semesters[year][semester]))
    tmp = semesters[year][semester].pop()
    semesters[year][semester].insert(0, tmp) #put back at begining
    paper = None
    done = False
    while not done:
        while (len(semesters[year][semester]) > 4 and
               tmp != paper):
            paper = semesters[year][semester].pop()
            if (not check_if_prerequisite(paper,
                                          semesters,
                                          year+1,
                                          semester) and
                # does previous semester have a paper that
                # has this as a prerequisite?
                not check_if_prerequisite(paper,
                                          semesters,
                                          year,
                                          semester-1)):
                semesters[year+1][semester].append(paper)
            else:
                semesters[year][semester].insert(0, paper)
        
        if ((tmp == paper or len(semesters[year][semester]) <= 4) or
            len([x for x in semesters[year+1][semester]
                 if int(float(x) * 1000 % 1000) / 100 == year+1]) == 0 and
            len(semesters[year][semester]) < 4):
            done = True




def check_if_prerequisite(paper, semesters, year, semester):
    for yr in range(year, -1, -1):
        for sem in range(semester, -1, -1):
            for code in semesters[yr][sem]:
                if paper in get_prerequisites(code, []):
                    return True
        
    
    return False

def check_programme(modal):
    programme = []
    [programme.extend([y.split(' ')[0] for y in x if y is not None]) for x in modal]

    #clear the list
    del missing[:]
    
    result = DEGREE.check_programme(major, programme)
    operators.reset_missing()
    #print 'passed rules =', result
    if not result:
        for x in DEGREE.rules:
            result = x.check(programme, DEGREE.schedule)
            if not result:
                missing.append((str(x), DEGREE.name + ' Degree', copy.deepcopy(operators.missing), result,))
            
            operators.reset_missing()
        for x in DEGREE.schedule[major][1]:
            result = x.check(programme, DEGREE.schedule[major][0])
            if not result:
                missing.append((str(x), major + ' Major', copy.deepcopy(operators.missing), result,))
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
                    missing.append((str(rule), code + ' Prerequisite', copy.deepcopy(operators.missing), result,))
                        
                operators.reset_missing()
    max_columns = 1
    rulestore.clear()
    missing_degrees = [x for x in missing if x[1].find('Degree') != -1]
    if len(missing_degrees) > 0:
        it = rulestore.append(('Degree requirements', None, None))
        for missed in missing_degrees:
            if len(missed[1]) > max_columns:
                max_columns = len(missed[2])
            it = rulestore.append((missed[0],missed[1], "TODO"))
        it = rulestore.append((None, None, None))
    missing_majors = [x for x in missing if x[1].find('Major') != -1]
    if len(missing_majors) > 0:
        it = rulestore.append(('Major requirements', None, None))
        for missed in missing_majors:
            if len(missed[1]) > max_columns:
                max_columns = len(missed[2])
            it = rulestore.append((missed[0],missed[1], "TODO"))
        it = rulestore.append((None, None, None))
    missing_papers = [x for x in missing if x[1].find('Prerequisite') != -1]
    if len(missing_papers) > 0:
        it = rulestore.append(('Paper requirements', None, None))
        for missed in missing_papers:
            if len(missed[1]) > max_columns:
                max_columns = len(missed[2])
            it = rulestore.append((missed[0],missed[1], "TODO"))
        it = rulestore.append((None, None, None))
    


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

    def is_valid(x):
        tmp = x.strip()
        if tmp in ['True', 'False']:
            return True
        elif 'x' in tmp:
            return True

        try:
            float(tmp)
            return True
        except:
            return False

        return False
        
    tmp = [True] + [convert(x) for x in tmp.split(',') if is_valid(x)]
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
    [programme.extend([y.split()[0] for y in x if y is not None and len(y) > 0]) for x in planstore]
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
    [programme.extend([y.split()[0] for y in x if y is not None and len(y) > 0]) for x in planstore]
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
    sigs = builder.connect_signals({'gtk_main_quit': gtk.main_quit, 
									'on_planstore_row_changed': on_planstore_row_changed, 
									'on_rule_selected': on_rule_selected, 
									'cancel_action_activate_cb': cancel_action_activate_cb, 
									'apply_action_activate_cb': apply_action_activate_cb,
									'on_possible_activated': widgets.on_possible_activated, 
									'on_plancell_edit_1': on_plancell_edit_1, 
									'on_plancell_edit_2': on_plancell_edit_2, 
									'on_plancell_edit_3': on_plancell_edit_3,
									'on_major_filter_changed': on_major_filter_changed})

    fillinplan()
    
    main_window.show()

    

    gtk.main()

    debug_file.close()
