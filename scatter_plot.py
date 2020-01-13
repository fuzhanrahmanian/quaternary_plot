import numpy as np
import matplotlib.pyplot as plt
from myquaternaryutility import QuaternaryPlot
from quaternary_faces_shells import ternaryfaces_shells
import random
import helper_functions as help

# Relevant Variables
nrows = 5
ncols = 3
n_of_measurments = 20
ellabels = ['Au', 'Mg', 'Si', 'Na', 'Cr', 'Mn']
grouping = 4



# Helper Variables
intervs = 10
results = np.empty((0, 4))
color = np.empty((nrows, ncols), dtype=object)
n_click = 0
# Random color for picking
for i in range(nrows):
    for j in range(ncols):
        list = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1]
        color[i][j] = list
subplot_pick_color = 0
elements_of_subplot = 0



# Data for uniform Point-Distribution
compsint = [[b, c, (intervs - a - b - c), a] for a in np.arange(0, intervs + 1)[::-1] for b in
            np.arange(0, intervs + 1 - a) for c in np.arange(0, intervs + 1 - a - b)][::-1]
print(len(compsint))
comps = np.float32(compsint) / intervs



# Declaration of the figure with the given number of columns and rows
fig, axis = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True)

# Map elements in groups of 4
elemnt_groups = help.map_elemnts(ellabels, grouping, nrows, ncols)

# Iteration over every axis where the data is used to plot the ternary_shells
points_list = []
subplot_list = []
for i in range(0, nrows, 1):
    for j in range(0, ncols, 1):
        # Get the object QuaternaryPlot
        # color[i][j] = np.random.choice(range(256))
        stpquat = QuaternaryPlot()
        cols = stpquat.rgb_comp(comps)
        tf = ternaryfaces_shells(axis[i][j], elemnt_groups[i][j], nintervals=intervs)
        tf.label()
        # Saves all tthe picked data inside a list for the color changing
        points_list.append(tf.scatter(comps, cols * 0, skipinds=[0, 1, 2, 3], s=None))
        # subplot_list.append(tf)




# Pick event for changing color of the picked Data
def onpick(event):
    global subplot_pick_color
    event.artist._facecolors[event.ind, :] = subplot_pick_color
    fig.canvas.draw()


# A Press event executed on mouse-clicks
# It takes the clicked coordinates and turns them into the comp coordinates
# Closes the program after reaching the number of measurments
def on_press(event):
    global n_click
    global results
    global elements_of_subplot

    clicked_comp = tf.toComp(event.xdata, event.ydata)
    fig.canvas.draw()
    if n_click < n_of_measurments:
        # Forms the results Array
        results = np.vstack([results, [clicked_comp]])
        n_click += 1

        # Print Formatting
        print('Measurment: {} '.format(n_click))
        for elements in range(len(elements_of_subplot)):
            print('{}: {}'.format(elements_of_subplot[elements], clicked_comp[elements]))
            # Look in the dictionary for the value of elemnts_of_subplots
            # In the Key put the single elements value the are stored in clicked_comp[elemnts]

        print ('\n')
    else:
        print('Coordinates of {} measurments'.format(n_of_measurments))
        print(results)
        # Results are saved to csv
        np.savetxt('results.csv', results, delimiter=",")

        exit()


def enter_axes(event):
    global elements_of_subplot
    global subplot_pick_color
    elements_of_subplot = 0
    print('enter_axes', event.inaxes)
    for i in range(0, nrows, 1):
        for j in range(0, ncols, 1):
            if axis[i][j] == event.inaxes:
                elements_of_subplot = elemnt_groups[i][j]
                subplot_pick_color = color[i][j]


# The Click event
fig.canvas.mpl_connect('axes_enter_event', enter_axes)
fig.canvas.mpl_connect('pick_event', onpick)
fig.canvas.mpl_connect('button_press_event', on_press)
plt.show()
