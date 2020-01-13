import numpy as np
import matplotlib.pyplot as plt
from myquaternaryutility import QuaternaryPlot
from quaternary_faces_shells import ternaryfaces_shells
import helper_fcns

sysd,systems = helper_fcns.import_data()
fake_elements = np.array(['a','b','c','d','e','f'])
# Relevant Variables
nrows = 5
ncols = 3
n_of_measurments = 10

# Helper Variables
intervs = 10
results = np.empty((0, 4))
n_click = 0



#compsint = [[b, c, (intervs - a - b - c), a] for a in np.arange(0, intervs + 1)[::-1] for b in
            #np.arange(0, intervs + 1 - a) for c in np.arange(0, intervs + 1 - a - b)][::-1]
#print(len(compsint))
#comps = np.float32(compsint) / intervs


# Declaration of the figure with the given number of columns and rows
fig, axis = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True)

# Iteration over every axis where the data is used to plot the ternary_shells
points_list = []
counter = 0
for i in range(0, nrows, 1):
    for j in range(0, ncols, 1):
        # Get the object QuaternaryPlot
        stpquat = QuaternaryPlot()
        #cols = stpquat.rgb_comp(sysd[counter]['comp'])
        tf = ternaryfaces_shells(axis[i][j], fake_elements[list(systems[counter])], nintervals=intervs)
        tf.label()
        #Saves all tthe picked data inside a list for the color changing
        #np.rand.random(len(sysd[counter]['comp']))
        points_list.append(tf.scatter(np.array(sysd[counter]['comp'])[:,systems[counter]], np.array(sysd[counter]['fom'])*0, skipinds = [0,1,2,3], s=None))
        counter += 1
        axis[i][j].set_picker(True)
# Pick event for changing color of the picked Data

selectiond = {'system': [], 'comp': [], 'fom': [], 'n_click':[]}

import matplotlib as mpl

# A Press event executed on mouse-clicks
# It takes the clicked coordinates and turns them into the comp coordinates
# Closes the program after reaching the number of measurments
def on_press(event):
    #this can tell us where we clicked
    global n_click
    global results
    #figure out the axis in that we clicked and from there get the system
    counter_sys = 0
    for i in range(0, nrows, 1):
        for j in range(0, ncols, 1):
            if axis[i][j] == event.inaxes:
                selectiond['system'].append(counter_sys)
                axs = [i,j]
            counter_sys += 1
    counter_sys = selectiond['system'][-1]
    clicked_comp = tf.toComp(event.xdata, event.ydata)


    selectiond['comp'].append(clicked_comp)
    selectiond['n_click'].append(n_click)

    #figure out the FOM
    ix = np.argmin(np.sum(np.abs(np.array(sysd[counter_sys]['comp'])[:,systems[counter_sys]]-clicked_comp),axis=1))
    selectiond['fom'].append(sysd[counter_sys]['fom'][ix])

    norm = mpl.colors.Normalize(vmin=0.39,vmax=.65)
    color = mpl.cm.hot(norm(selectiond['fom'][-1]))
    #event.artist._facecolors[event.ind, :] = color
    axis[axs[0]][axs[1]].scatter(event.xdata, event.ydata,s=200,color=color)
    fig.canvas.draw()

    if n_click < n_of_measurments:
        # Forms the results Array
        n_click += 1
        # Print Formatting
        print('Measurment: {} '.format(n_click))
    else:
        print('Coordinates of {} measurments'.format(n_of_measurments))
        # Results are saved to csv

        exit()


# The Click event
fig.canvas.mpl_connect('button_press_event', on_press)
#fig.canvas.mpl_connect('pick_event', onpick)

plt.show()
