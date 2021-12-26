import numpy as np

def remove_outliers(X:np.ndarray,Y:np.ndarray):

    assert len(X.shape) == len(Y.shape) == 1
    assert X.size == Y.size

    EPSILON_X = 0.02   
    EPSILON_Y = 0.04

    groups : dict= {0:{0}}

    block = [(0,X[0],Y[0],0)]

    for i,(x,y) in enumerate(zip(X[1:],Y[1:]),1):
        while block and abs(block[0][1]-x)>EPSILON_X:
            block.pop(0)
        seen_groups =set()
        for _,_,y_,g_ in block:
            if abs(y_-y)>EPSILON_Y:
                continue
            seen_groups.add(g_)

        if len(seen_groups)>1:  # combines groups 
            new = set()
            for group in seen_groups:
                new |= groups[group]
                del groups[group]
            new.add(i)
            groups[min(seen_groups)] = new
            block = [(ind,i,j,min(seen_groups) if ind in new else k) for ind,i,j,k in block]
            tfgroup = min(seen_groups)
        elif len(seen_groups) == 1:     # adds a to an existing group
            tfgroup = min(seen_groups)
            groups[tfgroup].add(i)
        else:   # creates a new group
            tfgroup = max(groups.keys())+1
            groups[tfgroup] = set([i])

        block.append((i,x,x,tfgroup))
        
    inliers = []
    top = [[0,0],[0,0],[0,0]]
    for group,ind in groups.items():
        if len(ind) > top[0][1]:
            top = [[0,0],top[0],top[1]]
            top[0] = [group,len(ind)]
            continue
        elif len(ind) > top[1][1]:
            top = [top[0],[0,0],top[1]]
            top[1] = [group,len(ind)]
        elif len(ind) > top[2][1]:
            top[2] = [group,len(ind)]
    if top[2][1] > 0.2*top[1][1]:
        inliers = [ind  for i,_ in top for ind in groups[i]]
    else: 
        allowed = [top[0][0],top[1][0]]
        inliers = [ind for i in allowed for ind in groups[i]]
        
    inliers = np.sort(np.array(inliers))

    return inliers