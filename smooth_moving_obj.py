#each cycle move circle in random direction by small increment, so the movement is smooth
#make sure that circle is always on the screen

from psychopy import monitors, visual, event, core
import random   
import time

monitor = monitors.Monitor("myMonitor", width=62.0, distance=67.0)
monitor.setSizePix([1920, 1080])
win = visual.Window([1920, 1080], monitor=monitor, units="deg", screen=0, fullscr=True)
circle = visual.Circle(win, units="pix", edges=32, radius=8, fillColor='yellow')

max = (960, 540)
x = random.randint(-max[0], max[0])
y = random.randint(-max[1], max[1])
while not event.getKeys('q'):
    circle.pos = (x,y)
    circle.draw()
    win.flip(clearBuffer=True)
    x_incr = random.randint(-10, 10)
    y_incr = random.randint(-10, 10)
    if x + x_incr > max[0] or x + x_incr < -max[0]:
        x = x - x_incr
    else:
        x = x + x_incr
    if y + y_incr > max[1] or y + y_incr < -max[1]:
        y = y - y_incr
    else:
        y = y + y_incr
    time.sleep(0.1)

win.close()
core.quit()