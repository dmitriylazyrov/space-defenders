import pygame
import controls
from spaceship import SpaceShip
from pygame.sprite import Group
from stats import Stats
from scores import Scores

def run():


    pygame.init()
    screen = pygame.display.set_mode((700, 800))
    pygame.display.set_caption("Космічні захисники")
    bg_color = (0, 0, 0)
    spaceship = SpaceShip(screen)
    bulletts = Group()
    inos = Group()
    controls.create_array(screen, inos)
    stats = Stats()
    sc = Scores(screen, stats)

    while True:
        controls.events(screen, spaceship, bulletts)
        if stats.run_game:
            spaceship.update_spaceship()
            controls.update(bg_color, screen, stats, sc, spaceship, inos, bulletts)
            controls.update_bullets(screen, stats, sc, inos, bulletts)
            controls.update_inos(stats, screen, sc, spaceship, inos, bulletts)



run()