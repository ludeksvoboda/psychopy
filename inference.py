import pygame

pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video1", (640, 480))
cam.start()
while True:
    img = pygame.surfarray.array3d(cam.get_image()).swapaxes(0,1)