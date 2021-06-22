import pygame, sys, random
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()

class Files:
    """
    Class to maintain file names and read-in Instructions.txt file.
    You will need to update this code if you change the file names or use different images.

    Attributes:
        skier_dict: dictionary with skier image file names based on speed or type
        bg_image: background image file name
        font: tuple containing font name and size
        instructions: string containing game instructions
    """

    def __init__(self):
        self.skier_dict = { -2:'skier_left2.png', -1:'skier_left1.png', 0: 'skier_down.png', 1:'skier_right1.png', 2:'skier_right2.png', 'crash':'skier_crash.png', 'tree':'skier_tree.png', 'flag':'skier_flag.png', 'snowball':'skier_snowball.png' }
        self.bg_image = 'background.jpg'
        self.font = pygame.font.SysFont(("bauhaus93"),35)
        self.smallfont = pygame.font.SysFont(("bauhaus93"),25)
        self.instructions = ''
        self.welcome_image = 'instructions.png'

        with open('instructions.txt') as my_file:
            self.instructions = my_file.read()
    
    def playmusic(self):
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(-1)
    
    def __repr__(self):
        """Returns names of all files in File class"""
        return (str(self.bg_image) + 
                str(self.font) + 
                str(self.skier_dict) +
                str(self.instructions)
                )

class Display(pygame.sprite.Sprite):
    """
    Class to import and scroll background image.
    Could be used to create other image rectangles.

    Attributes:
        surface: loads image *arg onto pygame surface
        rect: places a rectangle around the surface
        speed: default speed is -1 pixel
        first_pos: default position is 0 [this is used for pos of first background image]
        second_pos: default position is y_dim [this is used for pos of second background image]

    """

    def __init__(self, image_file):
        super().__init__()
        self.surface = pygame.image.load(image_file).convert_alpha()
        self.rect = self.surface.get_rect()
        self.speed = -1
        self.first_pos = 0
        self.second_pos = Y_DIM 
        self.display_width = X_DIM
        self.display_height = Y_DIM
    
    def draw_floor(self):
        """Displays game title and scrolls background image"""
        pygame.display.set_caption("AVALANCHE EXTREME!   Move left and right with < and > keys.")
        SCREEN.blit(self.surface, (0, self.first_pos + self.speed))
        SCREEN.blit(self.surface, (0, self.second_pos + self.speed))
        self.first_pos -= 1
        self.second_pos -= 1

        if self.first_pos < -Y_DIM:
            self.first_pos = 0
        if self.second_pos < -Y_DIM:
            self.second_pos = 0

    def welcome_screen(self):
        global SCREEN
        """Displays welcome screen for ~30 seconds"""
        self.surface = self.surface
        self.surface = pygame.transform.scale(self.surface, (int(X_DIM), int(Y_DIM*1.3)))
        self.rect = self.surface.get_rect()
        SCREEN.blit(self.surface,(0,0))
        pygame.display.update()
        pygame.time.delay(20000)
        SCREEN = pygame.display.set_mode((X_DIM, Y_DIM))
        pygame.display.update()
        
    def __repr__(self):
        print("This object is used to manage the background image")

class Player(pygame.sprite.Sprite):
    """This class is used to create a skier.
        
        Attributes:
            surface: this loads the downhill image onto Pygame surface
            rect: places a Pygame rect around the surface
            rect.center: x,y coodinates of skier
            self.angle: this is speed along x-axis, which can range from -2 to +2 (left to right)
            self.health: default is 100
            self.flag_score: number of flags collected
            self.high_score: highest flag score on record
            self.status: bool; controls game loop; if True, game runs
            self.games_played: tracks number of games played
        
        Methods:

    """
    def __init__(self, image_file):
        super().__init__()
        self.surface = pygame.image.load(image_file).convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect.center = [X_DIM/2, Y_DIM*0.35]
        self.angle = 0
        self.health_score = 100
        self.flag_score = 0
        self.high_score = 0
        self.status = True     #this sets the game loop
        self.games_played = 1
    
    def __repr__(self):
        return ("This object represents the player")

    def turn(self, direction):
        """Loads new image when skier turns and returns angle value"""
        pos = self.rect.center
        self.angle = self.angle + direction
        if self.angle < -2:
            self.angle = -2
        if self.angle > 2:
            self.angle = 2
        self.surface = pygame.image.load(files.skier_dict[self.angle]).convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect.center = pos
        return self.angle

    def move(self, angle):
        """Move the skier left and right based on turn method's return value"""
        self.rect.centerx = self.rect.centerx + angle
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centerx > X_DIM:
            self.rect.centerx = X_DIM 
    
    def collision(self, obstacle):
        """Checks for collision with trees and snowballs and update health score"""
        col = pygame.sprite.spritecollide(self, obstacle, False)
        if self.health_score == 0:
            return False
        elif not col:
            return False
        elif col and self.health_score > 1:
            col[0].kill()
            self.health_score -= 10
            self.angle = 0
            print("Collision with obstacle!")
            return True
    
    def crash(self, collide):
        """ Updates photo if collision method returns True"""
        global SCREEN
        global files

        if collide == True:
            self.surface = pygame.image.load(files.skier_dict['crash']).convert_alpha()
            SCREEN.blit(self.surface, self.rect)
            pygame.display.flip()
            pygame.time.delay(500)    
  
    def score(self, flags):
        """Updates flag score"""
        col = pygame.sprite.spritecollide(self, flags, False)
        if col and self.health_score >1:
            col[0].kill()
            self.flag_score += 1
            print("Caught a flag!")
    
    def checkstatus(self):
        """Checks player's health status.
            If health score reaches 0, skier status set to False.
        """
        if self.health_score <= 0:
             skier.status = False
     
    def score_display(self):
        """ Displays health score and flag score"""
        health_score_surface = files.font.render(f'HEALTH SCORE: {int(self.health_score)}', True, (0,0,0))
        health_score_rect = health_score_surface.get_rect(center = (X_DIM/2, Y_DIM*0.05))
        SCREEN.blit(health_score_surface, health_score_rect)
        flag_score_surface = files.font.render(f'FLAG SCORE: {int(self.flag_score)}', True, (0,0,0))
        flag_score_rect = flag_score_surface.get_rect(center = (X_DIM/2, Y_DIM*0.1))
        SCREEN.blit(flag_score_surface, flag_score_rect)
    
    def final_score_display(self):
        """ Displays score and message when game ends """
        if self.flag_score == 0:
            bad_score_surface = files.font.render(f'YOU SCORED NO FLAGS. TRY AGAIN!', True, (0,0,0))
            bad_score_rect = bad_score_surface.get_rect(center = (X_DIM/2, Y_DIM/2))
            SCREEN.blit(bad_score_surface, bad_score_rect)
            print("Flag score is: ", self.flag_score)
            print("High score is: ", self.high_score)
            print("Total games played is: ", self.games_played)
            pygame.display.flip()
            pygame.time.delay(3000)
        
        elif self.flag_score == 1:
            bad_score_surface = files.font.render(f'YOU SCORED 1 FLAG. KEEP TRYING!', True, (0,0,0))
            bad_score_rect = bad_score_surface.get_rect(center = (X_DIM/2, Y_DIM/2))
            SCREEN.blit(bad_score_surface, bad_score_rect)
            print("Flag score is: ", self.flag_score)
            print("High score is: ", self.high_score)
            print("Total games played is: ", self.games_played)
            pygame.display.flip()
            pygame.time.delay(3000)

        elif self.flag_score <= self.high_score:
            good_score_surface = files.font.render(f'YOU SCORED {int(self.flag_score)} FLAGS!', True, (0,0,0))
            good_score_rect = good_score_surface.get_rect(center = (X_DIM/2, Y_DIM/2))
            SCREEN.blit(good_score_surface, good_score_rect)
            print("Flag score is: ", self.flag_score)
            print("High score is: ", self.high_score)
            print("Total games played is: ", self.games_played)
            pygame.display.flip()
            pygame.time.delay(3000)

        elif self.flag_score > self.high_score and self.high_score > 1:
            good_score_surface = files.font.render(f'YOU SCORED {int(self.flag_score)} FLAGS!', True, (0,0,0))
            good_score_rect = good_score_surface.get_rect(center = (X_DIM/2, Y_DIM*0.2))
            SCREEN.blit(good_score_surface, good_score_rect)
            high_score_surface = files.smallfont.render(f"THAT'S {(int(self.flag_score)) - (int(self.high_score))} MORE THAN YOUR PRIOR RECORD!", True, (0,0,0))
            high_score_rect = high_score_surface.get_rect(center = (X_DIM/2, Y_DIM/2))
            SCREEN.blit(high_score_surface, high_score_rect)
            print("Flag score is: ", self.flag_score)
            print("High score is: ", self.high_score)
            print("Total games played is: ", self.games_played)
            pygame.display.flip()
            pygame.time.delay(3000)

        elif self.flag_score > self.high_score and self.high_score == 0:
            good_score_surface = files.font.render(f'YOU SCORED {int(self.flag_score)} FLAGS!', True, (0,0,0))
            good_score_rect = good_score_surface.get_rect(center = (X_DIM/2, Y_DIM*0.2))
            SCREEN.blit(good_score_surface, good_score_rect)
            get_score_surface = files.smallfont.render("LET'S GET MORE!", True, (0,0,0))
            get_score_rect = get_score_surface.get_rect(center = (X_DIM/2, Y_DIM/2))
            SCREEN.blit(get_score_surface, get_score_rect)
            print("Flag score is: ", self.flag_score)
            print("High score is: ", self.high_score)
            print("Total games played is: ", self.games_played)
            pygame.display.flip()
            pygame.time.delay(3000)

    def reset(self):
        """ Resets player's position, angle, health score and flag score. Sets skier status to True. """
        if self.flag_score > self.high_score:
            self.high_score = self.flag_score
        self.surface = pygame.image.load(files.skier_dict[0]).convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect.center = [X_DIM/2, Y_DIM*0.35]
        self.angle = 0
        self.health_score = 100
        self.flag_score = 0
        self.status = True

class Obstacles(pygame.sprite.Sprite):
    """ This class is used to create trees and flags"""
    def __init__(self, image_file):
        super().__init__()
        self.surface = pygame.image.load(image_file).convert_alpha()
        self.rect = self.surface.get_rect()
        self.rect.center = (random.choice(list(range(0, X_DIM+1, 40))), Y_DIM+10)

    def update(self):
        """ Updates position of trees and flags"""
        self.rect.centery -= 1
        SCREEN.blit(self.surface, self.rect)
        if self.rect.centery < 0:
            self.kill()
    
    def __repr__(self):
        return ("This object represents an instance of a tree or flag")

class Snowball(Obstacles):
    """ THe Snowball class is a child of the Obstacle class and is used to create snowballs.
        The update method has been overridden to move snowballs from top to bottom of screen.
    """
    def __init__(self, image_file):
        super().__init__(image_file)
        self.rect.center = (random.choice(list(range(0, X_DIM))), 0)
    
    def update(self):
        """Moves snowballs diagonally from top to bottom of screen"""
        self.rect.centery += 1
        self.rect.centerx += 1
        SCREEN.blit(self.surface, self.rect)
        if self.rect.centery > Y_DIM:
            self.kill()
    
    def __repr__(self):
        return ("This object represents an instance of a snowball, which inherits attributes from Obstacles parent class")

class Engine:
    """ The Engine class runs the game by calling the 'playgame' method."""

    def __init__(self):
        print("Game created")

    def playgame(self):
        global SCREEN

        # Set background and clock variables       
        bg = Display(files.bg_image)
        files.playmusic()   

        ### Declare sprite container groups
        tree_and_flag_group = pygame.sprite.Group() 
        obstacle_group = pygame.sprite.Group() 
        snowball_group = pygame.sprite.Group() 
        tree_group = pygame.sprite.Group() 
        flag_group = pygame.sprite.Group() 

        def sprite_reset(self):
            """This function clears sprite groups if game ends"""
            for x in obstacle_group:
                x.kill()
            for x in tree_and_flag_group:
                x.kill()
            for x in tree_group:
                x.kill()
            for x in flag_group:
                x.kill()
            for x in snowball_group:
                x.kill()

        ### Define Pygame userevents to make trees, flags and snowballs at specified time intervals 
        CREATETREE = pygame.USEREVENT
        pygame.time.set_timer(CREATETREE, 400)
        CREATEFLAG = pygame.USEREVENT+1
        pygame.time.set_timer(CREATEFLAG, 1000)
        CREATESNOWBALL = pygame.USEREVENT+2
        pygame.time.set_timer(CREATESNOWBALL, 2000)

        while True:
            bg.draw_floor()
            SCREEN.blit(skier.surface, skier.rect)
            clock.tick(120)          
            
            # Monitor user-input and create trees/flags/snowballs
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:                  
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # checks if a key is pressed
                    if event.key == pygame.K_LEFT:
                        skier.angle = skier.turn(-1)
                    elif event.key == pygame.K_RIGHT:
                        skier.angle = skier.turn(1)
                    elif event.key == pygame.K_h:
                        welcome.welcome_screen()
                    elif event.key == pygame.K_RETURN:
                        game.playgame()
                if event.type == CREATETREE:
                    tree_group.add(Obstacles(files.skier_dict['tree']))
                if event.type == CREATEFLAG:
                    flag_group.add(Obstacles(files.skier_dict['flag']))
                if event.type == CREATESNOWBALL:
                    snowball_group.add(Snowball(files.skier_dict['snowball']))
                
                # Update sprite groups
                tree_and_flag_group.add(tree_group)
                tree_and_flag_group.add(flag_group)
                obstacle_group.add(tree_group)
                obstacle_group.add(snowball_group)
            
            # Game loop
            if skier.status == True:
                
                skier.score_display()

                # Update location of objects
                skier.move(skier.angle)
                tree_and_flag_group.update()
                snowball_group.update()

                # Check for collisions & flags
                skier.crash(skier.collision(obstacle_group))
                skier.score(flag_group)
                skier.checkstatus()

            elif skier.status == False:
                skier.final_score_display()
                skier.reset()
                skier.games_played += 1
                sprite_reset(self)
                SCREEN = pygame.display.set_mode((X_DIM, Y_DIM))
                SCREEN.blit(skier.surface, skier.rect)
                pygame.display.flip()

            pygame.display.update()
            
# CONSTANT GAME VARIABLES
X_DIM = 600
Y_DIM = 500
SCREEN = pygame.display.set_mode((int(X_DIM), int(Y_DIM*1.3)))

# START GAME
files = Files()
skier = Player(files.skier_dict[0])    
game = Engine()
clock = pygame.time.Clock()
welcome = Display(files.welcome_image)
welcome.welcome_screen()
game.playgame()