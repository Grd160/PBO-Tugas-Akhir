import pygame
import random
import sys

from Setting import *
from Char.Player import Player
from Char.Boss import Boss
from Object.Map import GameMap
from Object.Upgrade import Upgrade
from Cam import Camera
from Weapon.Laser import LaserWeapon

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)


def reset_game():
    player = Player(100, 500)
    boss = Boss(4300, 120)
    game_map = GameMap()
    bullets = []
    upgrades = []
    camera = Camera()

    return player, boss, game_map, bullets, upgrades, camera


player, boss, game_map, bullets, upgrades, camera = reset_game()

running = True
game_over = False
victory = False

while running:
    dt = clock.tick(FPS)

    screen.fill((40, 40, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

            if game_over or victory:
                if event.key == pygame.K_r:
                    player, boss, game_map, bullets, upgrades, camera = reset_game()
                    game_over = False
                    victory = False

                if event.key == pygame.K_ESCAPE:
                    running = False

    if not game_over and not victory:

        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        player.move(keys)
        player.apply_gravity()
        player.update_weapon()

        camera.update(player)

        mouse_pos = pygame.mouse.get_pos()
        world_mouse = (mouse_pos[0] + camera.x, mouse_pos[1])

        if mouse_pressed:
            player.attack(bullets, world_mouse)

        for Obstacle in game_map.platforms + game_map.boxes:
            rect = Obstacle.get_rect()

            if player.get_rect().colliderect(rect):
                if player._vel_y > 0 and player.get_rect().bottom - player._vel_y <= rect.top:
                    player.get_rect().bottom = rect.top
                    player._vel_y = 0
                    player._on_ground = True
                elif player._direction == 1:
                        player.get_rect().right = rect.left
                elif player._direction == -1:
                        player.get_rect().left = rect.right

            for enemy in game_map.enemies:
                if enemy.get_rect().colliderect(rect):
                    if enemy._vel_y > 0 and enemy.get_rect().bottom - enemy._vel_y <= rect.top:
                        enemy.get_rect().bottom = rect.top
                        enemy._vel_y = 0
                        enemy._on_ground = True
                    elif enemy._direction == 1:
                        enemy.get_rect().right = rect.left
                    elif enemy._direction == -1:
                        enemy.get_rect().left = rect.right

        for enemy in game_map.enemies:
            enemy.apply_gravity()
            enemy.move(player)
            enemy.attack(bullets, player)

        boss.move(player)
        boss.attack(bullets)

        for bullet in bullets[:]:
            bullet.update()

            if bullet.exceeded_distance():
                if bullet in bullets:
                    bullets.remove(bullet)
                    continue

            for Obstacle in game_map.platforms + game_map.boxes:
                if bullet.rect.colliderect(Obstacle.get_rect()):
                    if bullet.penetrate:
                            continue
                    if bullet in bullets:
                            bullets.remove(bullet)
                    break

            if bullet.owner == player:

                for enemy in game_map.enemies[:]:
                    if bullet.rect.colliderect(enemy.get_rect()):
                        enemy.take_damage(bullet.damage)

                        if not bullet.penetrate:
                            if bullet in bullets:
                                bullets.remove(bullet)

                        if enemy.is_dead():
                            if random.random() < 0.4:
                                upgrades.append(Upgrade(enemy.get_rect().x, enemy.get_rect().y))

                            game_map.enemies.remove(enemy)

                        break

                if bullet.rect.colliderect(boss.get_rect()):
                    boss.take_damage(bullet.damage)

                    if not bullet.penetrate:
                        if bullet in bullets:
                            bullets.remove(bullet)
                            continue

                for box in game_map.boxes[:]:
                    if bullet.rect.colliderect(box.get_rect()):
                        box.take_damage(bullet.damage)

                        if not bullet.penetrate:
                            if bullet in bullets:
                                bullets.remove(bullet)
                                continue

                        if box.is_destroyed():
                            game_map.boxes.remove(box)

            else:
                if bullet.rect.colliderect(player.get_rect()):
                    player.take_damage(bullet.damage)

                    if bullet in bullets:
                        if bullet in bullets:
                            bullets.remove(bullet)
                            continue

        for upgrade in upgrades[:]:
            if player.get_rect().colliderect(upgrade.rect):
                player.set_weapon(upgrade.get_weapon())
                upgrades.remove(upgrade)

        if player.is_dead():
            game_over = True

        if boss.is_dead():
            victory = True

    for platform in game_map.platforms:
        platform.draw(screen, camera.x)

    for box in game_map.boxes:
        box.draw(screen, camera.x)

    for enemy in game_map.enemies:
        enemy.draw(screen, camera.x)

    for bullet in bullets:
        bullet.draw(screen, camera.x)

    for upgrade in upgrades:
        upgrade.draw(screen, camera.x)

    boss.draw(screen, camera.x)
    player.draw(screen, camera.x)

    if game_over:
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (420, 250))

        text2 = small_font.render("Press R to Restart or ESC to Exit", True, WHITE)
        screen.blit(text2, (420, 350))

    if victory:
        text = font.render("VICTORY", True, GREEN)
        screen.blit(text, (480, 250))

        text2 = small_font.render("Press R to Restart or ESC to Exit", True, WHITE)
        screen.blit(text2, (420, 350))

    pygame.display.update()

pygame.quit()
sys.exit()

