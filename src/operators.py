
#for applying rules to degree schedules
inschedule = None
points = None
missing = list()


def reset_missing():
    global missing
    missing = list()
    

def orcheck(papers, programme):
    results = list()
    for paper in papers:
        if isinstance(paper, tuple):
            if paper[0] == 'and':
                results.append(andcheck(paper[1:], programme))
            elif paper[0] == 'any':
                results.append(anycheck(paper[1:], programme))
        else:
            results.append(code(paper, programme))



    return any(results)


def andcheck(papers, programme):
    results = list()
    for paper in papers:
        if isinstance(paper, tuple):
            if paper[0] == 'or':
                results.append(orcheck(paper[1:], programme))
            elif paper[0] == 'any':
                results.append(anycheck(paper[1:], programme))
        else:
            results.append(code(paper, programme))

    return all(results) and len(results) > 0

def code(code, programme):
    ret = code in programme or ('x' in code and len([x for x in programme if int(float(code.replace('x', ''))*10) == int(float(x)*10)]) > 0)
    if not ret:
        missing.append(code)

    return ret


def oneof(papers, programme):
    results = list()
    for paper in papers:
        if isinstance(paper, tuple):
            if paper[0] == 'any':
                results.append(anycheck(paper[1:], programme))
        else:
            results.append(code(paper, programme))

    return any(results)


def anycheck(levels, programme):
    results = list()
    for level in levels:
        results.append(int(level) in [int(float(x)*1000%1000) for x in programme])

    return any(results)

def check(papers, programme, schedule=None):
    results = list()
    if inschedule != None and inschedule == True:
        if points != None:
            pass
        else:
            if schedule != None and isinstance(schedule, dict):
                tmp = [x[0] for x in schedule.values()]

                tmp2 = list()
                for paper in tmp:
                    tmp2.extend(paper)
                tmp2.sort()

                tmp3 = [int(float(x)) for x in tmp2]

                inschedule_papers = set([x for x in programme if int(float(x)) in tmp3])

                return len(inschedule_papers) >= int(papers[0])
    else:
        if isinstance(papers, list) and len(papers) > 0 and not isinstance(papers[0], tuple):
            for paper in papers:
                results.append(code(paper, programme))
        elif len(papers) > 0:
            for paper in papers[0]:
                if isinstance(paper, tuple):
                    if paper[0] == 'and':
                        results.append(andcheck(paper[1:], programme))
                    elif paper[0] == 'any':
                        results.append(anycheck(paper[1:], programme))
                    elif paper[0] == 'oneof':
                        results.append(oneof(paper[1:], programme))
                    elif paper[0] == 'or':
                        results.append(orcheck(paper[1:], programme))

                else:

                    results.append(code(paper, programme))


    return all(results) and len(results) > 0


def set_inschedule(status):
    global inschedule
    inschedule = status
