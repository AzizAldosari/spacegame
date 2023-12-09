import pygame
from .player import Player
from .Bullet import Bullet
from .boss import Boss
from .enemy1 import Enemy1
from .Laser import Laser
from pause_menu import pause_menu
import os
import random
from auto_save import auto_save


def run_world1(screen, player_data=None, level=1, score=0, kills=0, skills=None):
    pygame.init()
    # for the game over screen and winning screen and load and continue
    player_level = level
    player_score = score
    player_kills = 0
    player_skills = skills if skills is not None else []
    # the world1 screen
    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Game")
    # to fix the auto save and make it not save for inifnite number of time until the kill num increases
    auto_saved = False
    # Load images for player, bullets, boss, enemies, etc.
    base_path = os.path.dirname(__file__)  # using os path due to the game main loop being in the parent file
    player_images = os.path.join(base_path, 'assets_world1', 'spaceship1.png')
    bullet_images = os.path.join(base_path, 'assets_world1', 'fire.png')
    boss_image_path = os.path.join(base_path, 'assets_world1', 'boss_attack.png')
    enemy_image_path = os.path.join(base_path, 'assets_world1', 'enemy1.png')
    laser_image_path = os.path.join(base_path, 'assets_world1', 'fire.png')
    map_image_path = os.path.join(base_path, 'assets_world1', 'space.jpg')

    # Load images
    map_image = pygame.image.load(map_image_path)
    map_image = pygame.transform.scale(map_image, (screen_width, screen_height))  # Scale the image, to fix an issue
    # with the map dark spots.
    boss_image = pygame.image.load(boss_image_path)
    player_images = {'normal': pygame.image.load(player_images)}
    bullet_images = {'normal': pygame.image.load(bullet_images)}
    skill_image = {
        'speed_boost': 'world1/assets_world1/speed.png',
        'power_shot': 'world1/assets_world1/power.png',
        'extra_hp': 'world1/assets_world1/shield.png',
        'elemental_power': 'world1/assets_world1/ice.png'
    }
    # music
    music_path = os.path.join(os.path.dirname(__file__), 'assets_world1', 'game.mp3')
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)
    # to control the boss spawn
    boss_spawned = False
    boss = None
    # to add a number of enemies needed before the boss can come
    ENEMY_Num = 15  # small number for testing
    # Create game objects, and player data
    if isinstance(player_data, dict):
        start_speed = player_data.get('speed', 5)
        player_hp = player_data.get('hp', 100)
        player_level = player_data.get('level', 1)
    else:
        start_speed = 5
        player_hp = 100
        player_level = level

    if player_data:
        player = Player(player_images, bullet_images, start_speed, skill_image)
        player.hp = player_hp
        player.level = player_level
    else:
        player = Player(player_images, bullet_images, start_speed, skill_image)

    # boss = Boss((400, 300), 100, boss_image_path, laser_image_path)
    enemies = [Enemy1((200, 200), 2, enemy_image_path)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False, False
            elif event.type == pygame.USEREVENT + 1:
                player.reset_speed()
            elif event.type == pygame.USEREVENT + 2 and boss_spawned:
                boss.reset_shape()  # Reset boss shape when the event is triggered
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu(screen, player_score, player_kills, player.level, player.skills)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()
        if keys[pygame.K_UP]:
            player.move_up()
        if keys[pygame.K_DOWN]:
            player.move_down()
        if keys[pygame.K_SPACE]:
            player.shoot()

        screen.fill((0, 0, 0))
        screen.blit(map_image, (0, 0))
        player.draw(screen)

        for enemy in enemies:
            enemy.draw(screen)

        for bullet in player.bullets[:]:  # Iterate over a copy of the list
            bullet.update()
            bullet.draw(screen)

            # Remove bullet if it goes off-screen
            if bullet.position.y < 0:
                player.bullets.remove(bullet)

        for enemy in enemies[:]:  # iterate over a copy of the list
            if player.rect.colliderect(enemy.rect):
                player.hp -= 10  # or however much damage an enemy does
                enemies.remove(enemy)  # remove the enemy that collided with the player
                player_kills += 1
                player_score += 10
                player.experience += 10  # increase player's experience
            # Check for collision of bullets with enemies
        for bullet in player.bullets[:]:  # iterate over a copy of the list
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    player.bullets.remove(bullet)  # remove the bullet
                    enemies.remove(enemy)  # remove the enemy
                    player_kills += 1
                    player_score += 10
                    player.experience += 10  # increase player's experience
                    break  # break out of the inner loop to avoid multiple collisions for the same bullet

                    # the max number of enemies at the same time is 10
        if len(enemies) < min(10, 1 + player_kills // 5):  # increase enemies count
            spawn_position = (random.randint(0, screen_width), random.randint(0, screen_height))
            enemies.append(Enemy1(spawn_position, 2, enemy_image_path))  # Spawn new enemy

        # auto save trigger.
        if (player_kills + 1) % 5 == 0 and not auto_saved:  # to prevent auto save from happening when the game just
            # started.
            auto_save(player_level, player_score, player_kills, player_skills)
            print(f"Auto-saved at {player_kills} kills.")
            auto_saved = True
        elif (player_kills + 1) % 5 != 0:
            auto_saved = False

            # Level up system
        if player.experience >= 100:  # assuming 100 exp needed to level up
            player.experience -= 100  # reset the experience
            player.level_up()  # call the level up method
        if player.hp <= 0:
            pygame.mixer.music.stop()
            return False, player_score, player.level, player_kills

        if not boss_spawned and player_kills >= ENEMY_Num:
            boss = Boss((400, 300), 300, boss_image_path, laser_image_path)
            boss_spawned = True
            # boss coding spawn
        if boss_spawned:
            boss.update(player, screen, player.bullets)
            # calling the utility based ai system
            boss.decide_action(player, player.bullets)
            boss.draw(screen)

            for laser in boss.lasers[:]:  # Iterate over a copy of the list
                laser.update()
                laser.draw(screen)
                if player.rect.colliderect(laser.rect):
                    player.hp -= 10  # Reduced laser damage for testing
                    boss.lasers.remove(laser)  # Remove the laser after hitting the player
                # bullet damage and disappears after hitting the boss.
            for bullet in player.bullets[:]:
                if boss.rect.colliderect(bullet.rect):
                    player.bullets.remove(bullet)
                    boss.hp -= 10  # damage the bullet does
                    # Check for collision with boss
            if player.rect.colliderect(boss.rect):
                player.hp -= 50  # damage the boss does

            if boss.hp <= 0:
                pygame.mixer.music.stop()
                player_score += 100
                return True, player_score, player.level, player_kills

        for enemy in enemies:
            enemy.update(player.position, player.bullets)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return False, False
