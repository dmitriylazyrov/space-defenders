import pygame, sys
from bullet import Bullet
from ino import Ino
import time

def events(screen, spaceship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Вправо
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                spaceship.mright = True
            # Вліво
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                spaceship.mleft = True
            elif event.key == pygame.K_SPACE:
                new_bullet = Bullet(screen, spaceship)
                bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            # Вправо
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                spaceship.mright = False
            # Вліво
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                spaceship.mleft = False

def update(bg_color, screen, stats, sc, spaceship, inos, bullets):
    screen.fill(bg_color)
    sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    spaceship.output()
    inos.draw(screen)
    pygame.display.flip()

def update_bullets(screen, stats, sc, inos, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, inos, True, True)
    if collisions:
        for inos in collisions.values():
            stats.score += 10 * len(inos)
        sc.image_score()
        check_high_score(stats, sc)
        sc.image_spaces()
    if len(inos) == 0:
        bullets.empty()
        create_array(screen, inos)


def space_kill(stats, screen, sc, spaceship, inos, bullets):
    if stats.space_left > 0:
        stats.space_left -= 1
        sc.image_spaces()
        inos.empty()
        bullets.empty()
        create_array(screen, inos)
        spaceship.create_space()
        time.sleep(1)
    else:
        stats.run_game = False
        sys.exit()

def update_inos(stats, screen, sc, spaceship, inos, bullets):
    inos.update()
    if pygame.sprite.spritecollideany(spaceship, inos):
        space_kill(stats, screen, sc,  spaceship, inos, bullets)
    inos_check(stats, screen, sc, spaceship, inos, bullets)


def inos_check(stats, screen, sc, spaceship, inos, bullets):
    screen_rect = screen.get_rect()
    for ino in inos.sprites():
        if ino.rect.bottom >= screen_rect.bottom:
            space_kill(stats, screen, sc, spaceship, inos, bullets)
            break


def create_array(screen, inos):
    ino = Ino(screen)
    ino_width = ino.rect.width
    number_ino_x = int((700 - 2 * ino_width) / ino_width)
    ino_height = ino.rect.height
    number_ino_y = int((800 - 400 - 2 * ino_height) / ino_height)

    for row_number in range(number_ino_y - 1):
        for ino_number in range(number_ino_x):
            ino = Ino(screen)
            ino.x = ino_width + (ino_width * ino_number)
            ino.y = ino_height + (ino_height * row_number)
            ino.rect.x = ino.x
            ino.rect.y = ino.rect.height + (ino.rect.height * row_number)
            inos.add(ino)

def check_high_score(stats, sc):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()
        with open('highscore.txt', 'w') as f:
            f.write(str(stats.high_score))
