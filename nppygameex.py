# https://realpython.com/pygame-a-primer/
# https://www.pygame.org/docs/ref/surface.html#pygame.Surface.convert
# https://stackoverflow.com/questions/41168396/how-to-create-a-pygame-surface-from-a-numpy-array-of-float32

# https://stackoverflow.com/questions/54246668/how-do-i-delete-the-hello-from-the-pygame-community-console-alert-while-using
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import numpy as np
from pygame import surfarray

from timeit import default_timer as timer

from pygame.locals import (KEYDOWN, K_ESCAPE, K_q, QUIT)

pygame.init()

w = 1000
h = 800

display = pygame.display.set_mode((w, h))

img = np.zeros((w,h,3),dtype=np.uint8)


init_time = timer()
frames_displayed = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q):
            running = False
        if event.type == pygame.QUIT:
            running = False

    # updating the image
    for i in range(100):
        img[np.random.randint(w),np.random.randint(h)] = np.random.randint(255,size=3,dtype=np.uint8)

    surfarray.blit_array(display, img)
    pygame.display.flip()

    frames_displayed+=1


print("average frame rate:", frames_displayed/(timer()-init_time), "fps")

pygame.quit()
