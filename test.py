import matplotlib.pyplot as plt
from random import random

def onpick(event):
    if event.artist == plt1:
        print("Picked on top plot")
    elif event.artist == plt2:
        print("Picked on bottom plot")

first = [random()*i for i in range(10)]
second = [random()*i for i in range(10)]

fig = plt.figure(1)
plt1 = plt.subplot(211)
plt.plot(range(10), first)

plt2 = plt.subplot(212)
plt.plot(range(10), second)

plt1.set_picker(True)
plt2.set_picker(True)
fig.canvas.mpl_connect('pick_event', onpick)

plt.show()