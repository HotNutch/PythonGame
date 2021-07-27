# Joshua Hutchinson, 4/27/20, CS 1110 game project

import pygame
import gamebox
import random
import webbrowser

"""
Game idea: Coin collecting game with enemies that follow the player and power ups, game is beaten after level 10
is completed
Optional requirements: Enemies that follow the player, timer for power up spawning, collectible coins for score, 
power ups for speed boosts, levels with increasing difficulty (more coins to collect and more and faster enemies)
"""

"""
Disclaimer: Images/graphics used under Fair Use. 
Image sources:
Title Screen Background: http://getwallpapers.com/wallpaper/full/4/6/4/496050.jpg
Background: https://wallpaperplay.com/walls/full/c/a/1/195993.jpg
Background 1: https://i.pinimg.com/originals/cf/ef/27/cfef2749daad1d46f8a2848d0c42f3d6.jpg
Background 2: https://www.itl.cat/pngfile/big/144-1442403_sci-fi-wallpaper-1920-hd.jpg
Game Beaten Background: https://images.hdqwalls.com/download/scifi-astronaut-space-mars-is-1920x1200.jpg
Player 0 (default): https://opengameart.org/sites/default/files/lighter.gif
Player 1: https://media2.giphy.com/media/FsAFQWr5uq1by/source.gif
Player 2: https://i.pinimg.com/originals/3b/03/94/3b0394153492f7a2e31e80bb9e4c4fb5.gif
Player 3: https://i.ya-webdesign.com/images/transparent-laser-spaceship-7.gif
Player 4: https://media.giphy.com/media/CLqIaSJrDOa0o/giphy.gif
Coin: https://media.giphy.com/media/XzeRWmW7f5K4kZnrgB/giphy.gif
Enemy: https://thumbs.gfycat.com/TeemingGrizzledHammerkop-size_restricted.gif
Power Up: https://vignette.wikia.nocookie.net/doom/images/9/94/Invulnerability_anim.gif/revision/latest/top-crop/width/
          360/height/360?cb=20190112081955
"""

# movement speeds, acceleration, other variables, etc.
time = 0
score = 0
level = 0
player_speed = 14
enemy_speed = 0
level_time = 0  # for use with grace periods for each level
player_orientation = 90  # player orientation, for rotating character based on direction of movement
power_up_time = 5  # default spawn time for power up (for first level 1 of game being run)
teleport_uses = 1  # uses of teleport ability left
game_on = False
title_screen = True
game_paused = False
character_selected = False
powered_up = False
game_beaten = False
selected_character = "Brown"

# camera, gameboxes, images, etc.
camera = gamebox.Camera(800, 600)  # camera window
title_screen_background = gamebox.from_image(400, 300, "game_title_screen_background.jpg")
title_screen_background.scale_by(.8)
background = gamebox.from_image(400, 300, "game_background.jpg")
player = gamebox.from_image(400, 300, "game_player.gif")  # player in center of screen
player.scale_by(.3)

# walls of playable area
walls = [
    gamebox.from_color(825, 300, "black", 50, 1000),
    gamebox.from_color(-25, 300, "black", 50, 1000),
    gamebox.from_color(400, 625, "black", 1000, 50),
    gamebox.from_color(400, -25, "black", 1000, 50),
]

# collectible coins
coins = []

# enemies
enemies = []

# power ups
power_ups = [
    gamebox.from_image(random.randint(0, 800), random.randint(0, 600), "game_power_up.gif")
]
for power_up in power_ups:
    power_up.scale_by(.1)


def tick(keys):
    """
    Called in gamebox.timer() every frame, draws gameboxes, checks keys, etc.
    :param keys: keys pressed
    :return: None
    """

    # global variables
    global background
    global time
    global level_time
    global score
    global game_on
    global title_screen
    global game_paused
    global player
    global character_selected
    global selected_character
    global level
    global enemy_speed
    global player_speed
    global coins
    global enemies
    global power_ups
    global player_orientation
    global power_up_time
    global powered_up
    global teleport_uses
    global background
    global game_beaten

    # clear last frame
    camera.clear("black")  # fills the screen with black

    # title screen
    if title_screen:
        camera.draw(title_screen_background)
        camera.draw("Made by: Joshua Hutchinson (jnh4m)", 20, "white", 670, 585)
        camera.draw("Super Spectacular Space Chase", 40, "white", 400, 230)
        camera.draw("--------------------------------------------------------------------------", 20, "white", 400, 252)
        camera.draw("Move with WASD. Press SPACE for an emergency teleport. Press TAB to pause.", 20, "white", 400, 270)
        camera.draw("Collect all of the coins while avoiding the enemies to advance to the next level.", 20, "white",
                    400, 290)
        camera.draw("Power Ups spawn once each level and remain available for five seconds.", 20,
                    "white", 400, 310)
        camera.draw("Collect them to increase your speed and gain another teleport use.", 20, "white", 400, 330)
        camera.draw("--------------------------------------------------------------------------", 20, "white", 400, 350)
        camera.draw("Press a number to select your character:", 20, "white", 400, 370)
        camera.draw("1. Red 2. Blue 3. Teal 4. Yellow", 20, "white", 400, 390)
        camera.draw("Press SPACE to start or press ESC to quit.", 20, "white", 400, 430)

        # player select
        if pygame.K_1 in keys:
            player = gamebox.from_image(camera.x, camera.y, "game_player1.gif")
            player.scale_by(.2)
            character_selected = True
            selected_character = "Red"
        if pygame.K_2 in keys:
            player = gamebox.from_image(camera.x, camera.y, "game_player2.gif")
            player.scale_by(.2)
            character_selected = True
            selected_character = "Blue"
        if pygame.K_3 in keys:
            player = gamebox.from_image(camera.x, camera.y, "game_player3.gif")
            player.scale_by(.1)
            character_selected = True
            selected_character = "Teal"
        if pygame.K_4 in keys:
            player = gamebox.from_image(camera.x, camera.y, "game_player4.gif")
            player.scale_by(.08)
            character_selected = True
            selected_character = "Yellow"
        if character_selected:
            camera.draw(selected_character + " selected.", 20, "white", 400, 410)
        if pygame.K_SPACE in keys:
            title_screen = False
            game_on = True
            keys.clear()

    # level
    if len(coins) == 0:
        level += 1
        player_speed += 1  # increase player speed as level increases
        enemy_speed += 1  # increase enemy speed as level increases
        level_time = 0
        if level == 1:  # only reset orientation on new game
            rotation = 90 - player_orientation  # calculate rotation needed for orientation to be "up"
            player.rotate(rotation)  # rotate player to be facing "up"
            player_orientation += rotation  # update player orientation after rotation

        # add more coins
        for num in range(0, level + 4):  # add one more coin each level
            coins.append(gamebox.from_image(random.randint(0, 800), random.randint(0, 600), "game_coin.gif"))
        if len(coins) == level + 4:  # scale coins
            for coin_b in coins:
                coin_b.scale_by(.1)

        # add more enemies
        enemies = []  # reset list of enemies so more can be added
        for num in range(0, level + 2):  # add one more enemy each level
            enemies.append(gamebox.from_image(random.randint(0, 800), random.randint(0, 600), "game_enemy.gif"))
        if len(enemies) == level + 2:  # scale enemies
            for enemy_b in enemies:
                enemy_b.scale_by(.2)

        # reset power ups and powered up status
        power_ups = []  # reset list of power ups
        powered_up = False  # reset power up indicator

    # background change based on level, slight lag on first changes of program run
    if level < 4:  # default background for levels 1 to 3
        background = gamebox.from_image(400, 300, "game_background.jpg")
        background.scale_by(.6)
    elif 4 <= level < 7:  # change background for levels 4 to 6
        background = gamebox.from_image(400, 300, "game_background1.jpg")
        background.scale_by(.6)
    elif 7 <= level < 11:  # change background for levels 7 to 10
        background = gamebox.from_image(400, 300, "game_background2.jpg")
        background.scale_by(.5)

    # game beaten
    if level == 11:  # change background for game beaten screen
        game_beaten = True
        background = gamebox.from_image(400, 300, "game_beaten_background.jpg")  # change background
        background.scale_by(.6)

    # draw background behind everything else
    if not title_screen:
        camera.draw(background)

    # game on
    if game_on:  # player and camera do not move when paused, etc.

        # show character during game play
        camera.draw(player)

        # time
        time += 1 / fps
        if level == 1:
            level_time = time
        elif level != 1:
            level_time += 1 / fps

        # player movement
        if pygame.K_w in keys:
            player.y -= player_speed
        if pygame.K_s in keys:
            player.y += player_speed
        if pygame.K_d in keys:
            player.x += player_speed
        if pygame.K_a in keys:
            player.x -= player_speed

        # emergency teleport, randomly teleports player (may teleport player into enemies, part of the risk of use)
        if pygame.K_SPACE in keys and teleport_uses != 0:  # can use once per run but power up adds another use
            teleport_x, teleport_y = 0, 0
            # moves player to opposite side of playable area
            if player.x >= 400:
                teleport_x = random.randint(0, 400)
            elif player.x < 400:
                teleport_x = random.randint(400, 800)
            if player.y >= 300:
                teleport_y = random.randint(0, 300)
            elif player.y < 300:
                teleport_y = random.randint(300, 600)
            player.x, player.y = teleport_x, teleport_y
            teleport_uses -= 1
            keys.clear()

        # player rotation
        # two directions (diagonal)
        if pygame.K_w in keys and pygame.K_d in keys:
            rotation = 45 - player_orientation
            player.rotate(rotation)
            player_orientation += rotation
        elif pygame.K_w in keys and pygame.K_a in keys:
            rotation = 135 - player_orientation
            player.rotate(rotation)
            player_orientation += rotation
        elif pygame.K_s in keys and pygame.K_a in keys:
            rotation = 225 - player_orientation
            player.rotate(rotation)
            player_orientation += rotation
        elif pygame.K_s in keys and pygame.K_d in keys:
            rotation = 315 - player_orientation
            player.rotate(rotation)
            player_orientation += rotation

        # one direction
        elif pygame.K_w in keys:
            rotation = 90 - player_orientation  # calculate rotation needed for orientation to be "up"
            player.rotate(rotation)  # rotate player to be facing "up"
            player_orientation += rotation  # keep track of changes in orientation
        elif pygame.K_s in keys:
            rotation = 270 - player_orientation
            player.rotate(rotation)
            player_orientation += rotation
        elif pygame.K_d in keys:
            rotation = 360 - player_orientation
            player.rotate(rotation)
            player_orientation += rotation
        elif pygame.K_a in keys:
            rotation = 180 - player_orientation
            player.rotate(rotation)
            player_orientation += rotation

        # enemy movement (follow player)
        for enemy_c in enemies:
            if enemy_c.x < player.x:
                enemy_c.x += enemy_speed
            if enemy_c.x > player.x:
                enemy_c.x -= enemy_speed
            if enemy_c.y < player.y:
                enemy_c.y += enemy_speed
            if enemy_c.y > player.y:
                enemy_c.y -= enemy_speed

        # pause game
        if pygame.K_TAB in keys:
            game_paused = True
            game_on = False

    # player interaction with walls
    for wall in walls:
        if not title_screen and not game_beaten:
            camera.draw(wall)
        if player.touches(wall):
            player.move_to_stop_overlapping(wall)

    # player interaction with coins
    for coin_a in coins:  # named "coin_a" to not mirror "coin" in outer scope
        if not title_screen and not game_beaten:
            camera.draw(coin_a)
        if player.touches(coin_a):
            score += 1
            coins.remove(coin_a)

    # power up spawning and despawning
    if 5 <= round(level_time) <= 10 and game_on:
        if len(power_ups) == 0 and not powered_up:  # only add power up if none added already and none collected
            for num in range(1, 2):  # one power up each level
                power_ups.append(gamebox.from_image(random.randint(0, 800), random.randint(0, 600),
                                                    "game_power_up.gif"))
                for power_up_b in power_ups:
                    power_up_b.scale_by(.1)  # scale power ups after appending
    if round(level_time) > 10:
        power_ups = []  # power up is not collectible even after it is no longer visible

    # player interaction with power ups
    for power_up_a in power_ups:
        if not title_screen and not game_beaten:
            camera.draw(power_up_a)
        if player.touches(power_up_a):
            player_speed += 2  # speed up player for rest of game (until death) not just for round
            power_ups.remove(power_up_a)
            teleport_uses += 1  # add another teleport use, teleport uses are stackable and carry over to next level
            powered_up = True  # power up collected

    # player interaction with enemies
    for enemy_a in enemies:  # named "enemy_a" to not mirror "enemy" in outer scope
        if not title_screen and not game_beaten:
            camera.draw(enemy_a)
        if player.touches(enemy_a) and level_time > 1:  # one second grace period to prevent death upon spawning
            game_on = False

    # glitch fix for if player speed is too high (player_speed > 43)and player gets outside of playable area
    if player.x > 800:
        player.x = 400
    if player.x < 0:
        player.x = 400
    if player.y > 600:
        player.y = 300
    if player.y < 0:
        player.y = 300

    # draw time, score, etc. on top of everything else
    if not title_screen and not game_beaten:
        if round(time) == 1:  # "second" non plural
            camera.draw("Time: " + str(round(time)).zfill(3) + " second", 20, "white", 64, 15)  # timer
        if round(time) != 1:  # "seconds plural
            camera.draw("Time: " + str(round(time)).zfill(3) + " seconds", 20, "white", 68, 15)  # timer
        camera.draw("Score: " + str(round(score)).zfill(3) + " points", 20, "white", 65, 35)  # score board
        camera.draw("Level: " + str(level), 20, "white", 400, 15)
        if teleport_uses != 0:
            camera.draw("Teleport Available", 20, "white", 67, 55)  # indicates teleport use is available
        if powered_up:
            camera.draw("Power Up Collected", 20, "white", 71, 75)  # indicate power up has been collected

    # game paused
    if game_paused:
        camera.draw(player)  # keep player shown during pause
        camera.draw("Game paused.", 30, "white", 400, 230)
        camera.draw("Press SPACE to resume or press BACKSPACE to return to the title screen.", 20, "white", 400, 260)
        if pygame.K_SPACE in keys:  # resume game
            game_paused = False
            game_on = True
            keys.clear()

    # game over
    if not game_on and not title_screen and not game_paused and not game_beaten:
        camera.draw("Game Over.", 30, "white", 400, 230)
        camera.draw("---------------------", 20, "white", 400, 246)
        if score == 1:  # "point" non plural
            camera.draw("Your score was " + str(round(score)) + " point.", 20, "white", 400, 260)
        elif score != 1:  # "points" plural
            camera.draw("Your score was " + str(round(score)) + " points.", 20, "white", 400, 260)
        camera.draw("Press SPACE to try again or press BACKSPACE to return to the title screen.", 20, "white", 400, 280)
        player.x, player.y = 400, 300  # reset player location
        if pygame.K_SPACE in keys:  # resets game
            score = 0
            time = 0
            level = 0
            player_speed = 14
            enemy_speed = 0
            teleport_uses = 1  # reset number of uses for new game
            coins = []
            enemies = []
            game_on = True
            keys.clear()  # prevents movement at start of new game

    # game beaten
    if game_beaten:
        game_on = False
        camera.draw("Congratulations! You win!", 30, "white", 400, 230)
        camera.draw("-----------------------------------------", 20, "white", 400, 246)
        camera.draw("Thanks for playing!", 20, "white", 400, 260)
        camera.draw("Your score was " + str(round(score)) + " points.", 20, "white", 400, 280)
        camera.draw("Press SPACE to play again or press BACKSPACE to return to the title screen.", 20, "white",
                    400, 300)
        camera.draw("Press R to claim your reward.", 20, "white", 400, 320)
        player.x, player.y = 400, 300  # reset player location
        if pygame.K_SPACE in keys:  # resets game, keeps level
            score = 0
            time = 0
            level = 0
            player_speed = 15
            enemy_speed = 1
            teleport_uses = 1  # reset number of uses for new game
            coins = []
            enemies = []
            game_beaten = False
            game_on = True
            keys.clear()  # prevents movement at start of new game
        if pygame.K_r in keys:
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            keys.clear()

    # return to title screen and reset game
    if game_paused or game_beaten or not game_on:
        if pygame.K_BACKSPACE in keys:
            time = 0
            score = 0
            level = 0
            player_speed = 14
            enemy_speed = 0
            level_time = 0
            player.x, player.y = 400, 300
            rotation = 90 - player_orientation
            player.rotate(rotation)
            player_orientation += rotation
            power_up_time = 5
            teleport_uses = 1
            game_on = False
            title_screen = True
            game_paused = False
            character_selected = False
            powered_up = False
            game_beaten = False
            selected_character = "Brown"
            coins = []
            enemies = []
            keys.clear()

    camera.display()  # makes what is drawn visible


fps = 30  # frames per second
gamebox.timer_loop(fps, tick)
