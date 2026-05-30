import pygame
import random
import sys

from Setting import *
from Char.Player import Player
from Char.Boss import Boss
from Object.Upgrade import Upgrade
from Cam import Camera
from Weapon.Laser import LaserWeapon
from Char.LevelUp import LevelUpSystem
from Menu import MainMenu

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Shooter Game")

font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)


def reset_game(stage_class, difficulty_multiplier):
    platforms, boxes, enemies, boss = stage_class.create_map()

    for enemy in enemies:
        enemy.set_hp(int(100 * difficulty_multiplier))

    boss.set_hp(int(5000 * difficulty_multiplier))

    player   = Player(100, 500) 
    upgrades = []
    bullets  = []
    camera   = Camera()
    levelup  = LevelUpSystem()

    return player, boss, platforms, boxes, enemies, bullets, upgrades, camera, levelup

STATE_MENU = "menu"
STATE_GAME = "game"
STATE_OVER = "over"
STATE_WIN  = "win"

state = STATE_MENU
menu  = MainMenu(screen)

player = boss = platforms = boxes = enemies = bullets = upgrades = camera = levelup = None

running = True

while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == STATE_MENU:
            result = menu.handle_event(event)
            if result == "play":
                stage      = menu.get_selected_stage()
                difficulty = menu.get_difficulty_multiplier()
                player, boss, platforms, boxes, enemies, bullets, upgrades, camera, levelup = reset_game(stage, difficulty)
                state = STATE_GAME
            elif result == "exit":
                running = False

        elif state == STATE_GAME:
            if levelup.pending_levelup:
                levelup.handle_event(event, player)
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.jump()

        elif state in (STATE_OVER, STATE_WIN):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    stage      = menu.get_selected_stage()
                    difficulty = menu.get_difficulty_multiplier()
                    player, boss, platforms, boxes, enemies, bullets, upgrades, camera, levelup = reset_game(stage, difficulty)
                    state = STATE_GAME
                if event.key == pygame.K_ESCAPE:
                    state = STATE_MENU

    if state == STATE_MENU:
        menu.draw()

    elif state == STATE_GAME:
        screen.fill((40, 40, 60))

        if not levelup.pending_levelup:
            keys          = pygame.key.get_pressed()
            mouse_pressed = pygame.mouse.get_pressed()[0]
 
            player.move(keys)
            player.apply_gravity()
            player.update_weapon()
 
            camera.update(player)
 
            mouse_pos  = pygame.mouse.get_pos()
            world_mouse = (mouse_pos[0] + camera.x, mouse_pos[1])

            if mouse_pressed:
                player.attack(bullets, world_mouse)

            for Obstacle in platforms + boxes:
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

                for enemy in enemies:
                    if enemy.get_rect().colliderect(rect):
                        if enemy._vel_y > 0 and enemy.get_rect().bottom - enemy._vel_y <= rect.top:
                            enemy.get_rect().bottom = rect.top
                            enemy._vel_y = 0
                            enemy._on_ground = True

                        elif enemy._direction == 1:
                            enemy.get_rect().right = rect.left

                        elif enemy._direction == -1:
                            enemy.get_rect().left = rect.right

            for enemy in enemies:
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

                for Obstacle in platforms + boxes:
                    if bullet.rect.colliderect(Obstacle.get_rect()):
                        if bullet.penetrate:
                                continue
                        if bullet in bullets:
                                bullets.remove(bullet)
                        break

                if bullet.owner == player:
                    effective_damage = bullet.damage + player.get_damage_bonus()

                    for enemy in enemies[:]:
                        if bullet.rect.colliderect(enemy.get_rect()):
                            enemy.take_damage(bullet.damage)

                            if not bullet.penetrate:
                                if bullet in bullets:
                                    bullets.remove(bullet)

                            if enemy.is_dead():
                                if random.random() < 0.4:
                                    upgrades.append(Upgrade(enemy.get_rect().x, enemy.get_rect().y))

                                enemies.remove(enemy)
                                levelup.register_kill()

                            break

                    if bullet.rect.colliderect(boss.get_rect()):
                        boss.take_damage(bullet.damage)

                        if not bullet.penetrate:
                            if bullet in bullets:
                                bullets.remove(bullet)
                                continue

                    for box in boxes[:]:
                        if bullet.rect.colliderect(box.get_rect()):
                            box.take_damage(bullet.damage)

                            if not bullet.penetrate:
                                if bullet in bullets:
                                    bullets.remove(bullet)
                                    continue

                            if box.is_destroyed():
                                boxes.remove(box)

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
                state = STATE_OVER

            if boss.is_dead():
                state = STATE_WIN

        for platform in platforms:
            platform.draw(screen, camera.x)

        for box in boxes:
            box.draw(screen, camera.x)

        for enemy in enemies:
            enemy.draw(screen, camera.x)

        for bullet in bullets:
            bullet.draw(screen, camera.x)

        for upgrade in upgrades:
            upgrade.draw(screen, camera.x)

        boss.draw(screen, camera.x)
        player.draw(screen, camera.x)

        lv_text = small_font.render(
                f"Lv.{levelup.level}  Kill: {levelup.kills} / {levelup.kills_per_level * levelup.level}",
                True, WHITE
            )
        screen.blit(lv_text, (20, 50))

        levelup.draw(screen)

    elif state == STATE_OVER:
        screen.fill((40, 40, 60))
        text  = font.render("GAME OVER", True, RED)
        text2 = small_font.render("R - Restart    ESC - Main Menu", True, WHITE)
        screen.blit(text,  (WIDTH // 2 - text.get_width() // 2,  250))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 350))

    elif state == STATE_WIN:
        screen.fill((40, 40, 60))
        text  = font.render("VICTORY!", True, GREEN)
        text2 = small_font.render("R - Restart    ESC - Main Menu", True, WHITE)
        screen.blit(text,  (WIDTH // 2 - text.get_width() // 2,  250))
        screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 350))

    pygame.display.update()

pygame.quit()
sys.exit()

