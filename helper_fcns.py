#reminder!!!!
#check that the code from Fuzhan is also revaling the multiples in the plots
import itertools as it
import numpy as np
n_comp = 4
n_elem = 6


def make_comps_ffoms(n_comp = n_comp,n_elem = n_elem):
    #setup a test array cointaining all the compositions of a 6 choose 4 plate

    quadcs = [i for i in it.product([j/10. for j in range (11)],repeat=n_comp) if sum(i)==1.]
    systems = [i for i in it.combinations([q for q in range(n_elem)],r=4)]
    compl = [] #this is the list of all compositions
    for system in systems:
        for quadc in quadcs:
            quadc = list(quadc)
            compl.append([quadc.pop(0) if i in system else 0 for i in range(n_elem)])
    #we only want the unique compositions
    comp = np.unique(compl,axis=0)
    foms = np.random.rand(len(comp))#some random numbers for foms
    return comp,foms

def split_comp_foms(comp,foms):
    #now we need to develop a way of telling which composition is part of which quaternary
    #the idea is to make a dict that has the quaternary identifier as key and the contents are comps and foms
    systems = {j:i for j,i in enumerate(it.combinations([q for q in range(n_elem)],r=n_comp))} #copied from above
    sysd = {i:{'comp':[],'fom':[]} for i in systems.keys()}
    for cix,c in enumerate(comp):
        #find out in which system we are
        memberships = []
        for j,v in systems.items():
            #inside = set([k for k, v in enumerate(c) if k > 0]).intersection(v)
            outside = set([k for k, v in enumerate(c) if v > 0]).difference(v)
            if len(outside)==0:
                memberships.append(j)
        for m in memberships:
            sysd[m]['comp'].append(c)
            sysd[m]['fom'].append(foms[cix])

    #this is to check if all quaternaries have the same length after they are repopulated
    #print([len(v['fom']) for k,v in sysd.items()])
    return sysd,systems

def chk_plot2update(c,systems):
    #this recieves a composition and returns the systems to be updated
    memberships = []
    for j, v in systems.items():
        # inside = set([k for k, v in enumerate(c) if k > 0]).intersection(v)
        outside = set([k for k, v in enumerate(c) if v > 0]).difference(v)
        if len(outside) == 0:
            memberships.append(j)
    return memberships

def import_data():
    import pickle
    data = pickle.load(open('tri_data_share.pck', 'rb'))
    foms = data['4098']['fom']
    comp = data['4098']['comp']
    compuni, ind = np.unique(comp, axis=0, return_index=True)
    fomsuni = foms[ind]
    sysd, systems = split_comp_foms(compuni, fomsuni)
    return sysd,systems



