"""
this class contains general purpose methods
"""
import pygame
#    https://www.pygame.org/docs/ref/mixer.html

#need to run these commands before playing sounds (these are run automatically when this modual is imported)
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init() #turn all of pygame on.

def playSound(fileName):
    sound = pygame.mixer.Sound(fileName)
    sound.play()
    
