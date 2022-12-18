#Prepare new db
#set the riht image size
#save the images

from multiprocessing import Process, Pipe
import time
from psychopy import monitors, visual, event, core
import random
import pygame
import pygame.camera
import mysql.connector
import config

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

    while not event.getKeys('q'):
        x = random.randint(-max[0], max[0])
        y = random.randint(-max[1], max[1])
        circle.pos = (x,y)
        circle.draw()
        win.flip(clearBuffer=True)
        time.sleep(2)
        coordinates = f"POINT({x} {y})"
        query = "INSERT INTO eye_click.recordings(coordinates) " \
                "VALUES (ST_PointFromText(%(coordinates)s))"
        mycursor.execute(query, {"coordinates": coordinates})
        mydb.commit()
        child_conn.send([x, y, mycursor.lastrowid])
        #send info to video recorder

    win.close()
    core.quit()
    
def video(parent_conn):
    pygame.init()
    pygame.camera.init()
    cam = pygame.camera.Camera("/dev/video1", (1024, 768))
    cam.start()
    images = []
    start = time.time()

    while(time.time() - start < 1):
        file_num = file_num + 1
        images.append(cam.get_image())

if __name__ == '__main__':
    p,q = Pipe()
    p1 = Process(target=screen, args=(q,))
    p2 = Process(target=video, args=(p,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()