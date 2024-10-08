import time
from psychopy import monitors, visual, event, core
import random

monitor = monitors.Monitor("myMonitor", width=62.0, distance=67.0)
monitor.setSizePix([1920, 1080])
win = visual.Window([1920, 1080], monitor=monitor, units="deg", screen=0, fullscr=True)
circle = visual.Circle(win, units="pix", edges=32, radius=8, fillColor='yellow')

max = (960, 540)
i = 1
while not event.getKeys('q'):
    # x = random.randint(-max[0], max[0])
    # y = random.randint(-max[1], max[1])
    if i % 2 == 0:
        circle.pos = (max[0]-100,max[1]-100)
    else:
        circle.pos = (-max[0]+100,-max[1]+100)
    circle.draw()
    win.flip(clearBuffer=True)
    time.sleep(2)
    i += 1
    #send info to video recorder

win.close()
core.quit()