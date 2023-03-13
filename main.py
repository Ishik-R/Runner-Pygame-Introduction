import pygame
from random import randint, choice
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()        
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_frame_index = 0
        self.player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()
        
        self.image = self.player_walk[self.player_frame_index]
        self.rect = self.image.get_rect(midbottom = (100,300))
        self.player_y0 = 300
        self.player_speed = 0

        self.jump_sound = pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.1)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.player_y0:
                self.player_speed = -11
                self.jump_sound.play()

    def player_gravity(self):
        self.rect.y += self.player_speed
        if not game_active:
                self.player_speed = 0
                self.rect.bottom = self.player_y0
        if self.player_y0 >= self.rect.bottom and self.player_speed == 0:
            pass
        elif self.player_y0 <= self.rect.bottom and self.player_speed > 0:
            self.player_speed = 0
            self.rect.bottom = self.player_y0
        else:
            self.player_speed += 0.4

    def animation_state(self):
        if self.rect.bottom < self.player_y0:
            self.image = self.player_jump
        else:
            self.player_frame_index += 0.05
            if self.player_frame_index >= len(self.player_walk): 
                self.player_frame_index = 0   
            self.image = self.player_walk[int(self.player_frame_index)]

    def update(self):
        self.player_input()
        self.player_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.obstacle_frames = [fly_frame_1, fly_frame_2]
            y_pos = 180 
        if type == 'snail':
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.obstacle_frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
        
        self.obstacle_frame_index = 0
        random_x = randint(900,1100)
        self.image = self.obstacle_frames[self.obstacle_frame_index]
        self.rect = self.image.get_rect(midbottom = (random_x, y_pos))

    def animation_state(self):
        self.obstacle_frame_index += 0.1
        if self.obstacle_frame_index >= len(self.obstacle_frames):
            self.obstacle_frame_index = 0
        self.image = self.obstacle_frames[int(self.obstacle_frame_index)]

    def destroy(self):
        if self.rect.right < -10:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

def collision_sprite():
    ''' 
    Checks if a sprite is colliding with any member of a group of sprites. It will return a list of all elements it is collidind.
     - if we have colllision, we will return 'False' to interrupt the active game state
     - if we don't have collision, the expression in if will return an empty list, therefore, we will have a false state in the if
    '''
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

def display_score(start_time):
    '''
    Calculates the score of the player (based on the time they can survive in game) and creates a way display to it.
    - Score calculation: the current time since the game was opened - the moment since the actual game was active (not in game over / start screen).
    -   For more information I recommend to check the 'pygame.time.get_ticks()' documentation.
    :param start_time: recieves the information about the exact moment that the current game started through 'pygame.time.get_ticks()'.
    :return: the score of the player. 
    '''
    current_time = int((pygame.time.get_ticks() - start_time) / 100)
    score_surf = font_score.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    pygame.draw.rect(screen,'#c0e8ec', (290,20,220,50))
    screen.blit(score_surf,score_rect)
    return current_time

# General elements to start the game
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Jumper")
clock = pygame.time.Clock()
font_score = pygame.font.Font('font/Pixeltype.ttf',50)
music = pygame.mixer.Sound('audio/music.wav')
music.set_volume(0.2)
music.play(loops = -1)
game_active = False
start_time = 0
score = 0

# Groups: player and obstacles
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Background elements
sky_surf = pygame.image.load('graphics/sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# Inactive game state elements
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,1.8)
player_stand_rect = player_stand.get_rect(center =(400,200))
title_surf = font_score.render('JUMPER',False,(111,196,164))
title_rect = title_surf.get_rect(center = (400,90))
instructions = font_score.render('Press SPACE to start!',False,(164,64,64))
instructions_rect = instructions.get_rect(center = (400,330))

# Timer - used to generate obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Loop of the game
while True:
    # Game events (obstacle generation, jump command, start again, quit) handlers
    for event in pygame.event.get():
        # Close game event
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Active game actions: obstacle generation / animation
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','fly','snail','snail','snail'])))
        # Not active game actions: reset the game with the press of the SPACE, and also reset the score
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.update()
                start_time = pygame.time.get_ticks()
                game_active = True

    # Game display: active state (actual game) and not active state (game over and start screen)
    if game_active:
        # Background display
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))
        score = display_score(start_time)
 
        # Classes - updates and display
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen) 
        obstacle_group.update()

        # Collision check
        game_active = collision_sprite()
    else:
        # Game inactive screen background
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        if score == 0:
            # Start screen
            screen.blit(title_surf, title_rect)
        else:
            # Game over screen
            final_score = font_score.render(f'GAME OVER - final score: {score}',False,(64,64,64))
            screen.blit(final_score, final_score.get_rect(center = (400,90)))
            instructions = font_score.render('Press SPACE to try again!',False,(164,64,64))
            instructions_rect = instructions.get_rect(center = (400,330))
        screen.blit(instructions, instructions_rect)

    # Game and frame update
    pygame.display.update()
    clock.tick(60)

#JUNKYARD - some lines of code that were used, but became obsolete. Still, there is some few tricks around so i kept them
    #for event in pygame.event.get():
    #   if event.type == pygame.MOUSEMOTION:
    #       if player_rectangle.collidepoint(event.pos): print('collision')
    #if pygame.mouse.get_pressed()[0]:
    #    print(pygame.mouse.get_pressed()[0])
        #if game_active:
    #print(f"Velocidade {player_speed} Pos {player_rect}")
    #pygame.draw.line(screen, 'Black', (0,0), pygame.mouse.get_pos(), 2)
    #score_surf = font_score.render('GAME OVER - Final score: ',False,(64,64,64))
    #score_rect = score_surf.get_rect(center = (400,50))
    #pygame.draw.rect(screen,'#c0e8ec',score_rect)
    #screen.blit(score_surf,score_rect)
        #Snail movement
    #snail_rect.x -= 5
    #if snail_rect.right <= 0: snail_rect.left = 800 
                    
    #if randint(0,2):
    #   obstacle_rect_list.append(snail_surf.get_rect(midbottom = (random_x,300)))
    #   obstacle_group.add(Obstacle('fly'))
    #else:
    #   obstacle_rect_list.append(fly_surf.get_rect(midbottom = (random_x,180)))
    #   obstacle_group.add(Obstacle('snail'))

    # OBSOLETE VARIABLES (after implementation of classes)
    # - obs: many funcions and methods became obsolete after removing those
# List to store the obstacles displayed on screen:
#obstacle_rect_list = []

# Obstacle 1: SNAIL - ground obstacle
#snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
#snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
#snail_frame_index = 0
#snail_frames = [snail_frame_1, snail_frame_2]
#snail_surf = snail_frames[snail_frame_index]

# Obstacle 2: FLY - air obstacle
#fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
#fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
#fly_frame_index = 0
#fly_frames = [fly_frame_1, fly_frame_2]
#fly_surf = fly_frames[fly_frame_index]

# Info about the player: image, walk / jump states, initial vertical position and initial vertical speed (to jump)
#player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
#player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
#player_walk = [player_walk_1, player_walk_2]
#player_frame_index = 0
#player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()

#player_surf = player_walk[player_frame_index]
#player_rect = player_surf.get_rect(midbottom = (80,300))
#player_y0 = player_rect.bottom
#player_speed = 0

# Introduction screen elements:
#player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
#player_stand = pygame.transform.rotozoom(player_stand,0,1.8)
#player_stand_rect = player_stand.get_rect(center =(400,200))
#title_surf = font_score.render('JUMPER',False,(111,196,164))
#title_rect = title_surf.get_rect(center = (400,90))
#instructions = font_score.render('Press SPACE to start!',False,(164,64,64))
#instructions_rect = instructions.get_rect(center = (400,330))

# Timer - used to generate obstacles and obstacle animations
#obstacle_timer = pygame.USEREVENT + 1
#pygame.time.set_timer(obstacle_timer, 1500)

#snail_animation_timer = pygame.USEREVENT + 2
#pygame.time.set_timer(snail_animation_timer, 400)

#fly_animation_timer = pygame.USEREVENT + 3
#pygame.time.set_timer(fly_animation_timer, 200)

    #if game_active:
        # Obstacle display and atualization
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Player display
        #player_animation()
        #screen.blit(player_surf,player_rect)

        # Player jumping and gravity logic
        #if player_y0 == player_rect.bottom and player_speed == 0:
        #    pass
        #elif player_y0 <= player_rect.bottom and player_speed > 0:
        #    player_speed = 0
        #    player_rect.bottom = player_y0
        #else:
        #    player_speed += 0.4
        #player_rect.top += player_speed
        
        # Collision detections
        #game_active = collision_check(player_rect,obstacle_rect_list)
    #else:
        #player_rect.bottom = player_y0
        #player_speed = 0
        #obstacle_rect_list = []

# OBSOLETE METHODS
"""
def obstacle_movement(obstacle_list):
    '''
    Moves all elements of existent obstacles, delete those who go off the screen and checks the appropriate image to display for the obstacle.
    :param obstacle_list: recieve a list of the elements o the screen.
    :return: a list. It will be empty if the obstacle_list is empty, otherwise, it will return an updated list with the obstacles.
    '''
    # First, this function verifes if the list is not empty.
    #  Be sure to return an empty list initially or there will be conflict because the function will return "None"
    if obstacle_list:
        for obstacle_rect in obstacle_rect_list:
            obstacle_rect.x -= 5
            # Obstacle display
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)
        # update the list, returning only the obstacles which right limit are still on screen
        #   - OBS: the function used to remove this element when it was excecuting the previous 'for', but it caused the obstacles to flicker
        #   - My personal solution for this issue was to excecute the exibition and the update of the 'obstacle_list' separately, as you can see
        obstacle_list = [element for element in obstacle_list if obstacle_rect.right  > 0]
        return obstacle_list
    else:
        return []
"""
"""
def collision_check(player_rect, obstacle_list):
    '''
    Checks for collision between all obstacles in the list and the player.
     If the player collide with something, this function return False to the game_active variable.
    :param player_rect: information about the rectangle of the player image.
    :param obstacle_list: list containing all obstacles present on the screen.
    :return: boolean type. True if the player is not colliding with anything, or False if it is colliding.
    '''
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player_rect.colliderect(obstacle_rect): return False
    return True
"""

"""    
def player_animation():
    '''
    Display walk animation if the player is on the floor. Otherwise, if the player is jumping, display the jumping animation
    '''
    global player_surf, player_frame_index

    if player_rect.bottom < player_y0:
        player_surf = player_jump
    else:
        player_frame_index += 0.05
        if player_frame_index >= len(player_walk): player_frame_index = 0   
        player_surf = player_walk[int(player_frame_index)]
"""