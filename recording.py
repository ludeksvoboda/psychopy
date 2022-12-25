#test if images correspond to the point by making it skip between two points far left and far right

from multiprocessing import Process, Pipe
import time
from psychopy import monitors, visual, event, core
import random
import pygame
import pygame.camera
import mysql.connector
import config
import numpy as np

mydb = mysql.connector.connect(
            host="10.0.0.114",
            user="ludek",
            passwd=config.db_pwd
        )

mycursor = mydb.cursor()

def screen(child_conn):
    monitor = monitors.Monitor("myMonitor", width=62.0, distance=67.0)
    monitor.setSizePix([1920, 1080])
    win = visual.Window([1920, 1080], monitor=monitor, units="deg", screen=0, fullscr=True)
    circle = visual.Circle(win, units="pix", edges=32, radius=8, fillColor='yellow')
    max = (960, 540)
    i = 1

    while not event.getKeys('q'):
        x = random.randint(-max[0], max[0])
        y = random.randint(-max[1], max[1])
        circle.pos = (x,y)
        circle.draw()
        win.flip(clearBuffer=True)
        time.sleep(1.5)
        if i > 1:
            query = "INSERT INTO eye_click_psychopy.data(x , y) " \
                    "VALUES (%(x)s, %(y)s)"
            mycursor.execute(query, {"x": x, "y": y})
            mydb.commit()
            child_conn.send([x, y, mycursor.lastrowid, i])
        else:
            child_conn.send([0, 0, 0, i])
        i += 1

    win.close()
    core.quit()
    
def video(parent_conn):
    pygame.init()
    pygame.camera.init()
    cam = pygame.camera.Camera("/dev/video1", (640, 480))
    cam.start()
    dir_name = '/home/lu/MLData/psychopyEyeClick/'
    images = []

    while(True):
        images.append(pygame.surfarray.array3d(cam.get_image()).swapaxes(0,1))
        if parent_conn.poll():
                save_info = parent_conn.recv()
                if save_info[3] > 1:
                    np.save(dir_name +'/images' + str(save_info[2]) + '.npy', images, allow_pickle=True)
                images = [] 

if __name__ == '__main__':
    p,q = Pipe()
    p1 = Process(target=screen, args=(q,))
    p2 = Process(target=video, args=(p,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()