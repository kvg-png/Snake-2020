import math
import random
import pygame
from pygame.math import Vector2
import sys
from pygame import mixer

class Snake:
    def __init__(self):
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.direction = Vector2(1,0)
        self.newblock = False
        
    def drawSnake(self):
      for block in self.body:
        # Create rectangle for the body of snake
          x_position = block.x * blockSize
          y_position = block.y * blockSize
          snake_rect = pygame.Rect(x_position, y_position, blockSize, blockSize) 
        # Draws rectangles for the body of snake
          pygame.draw.rect(screen,(0,255,0), snake_rect)

    def moveSnake(self):
      # Checks if the snake has eaten a new block and does what it says: 
      if self.newblock == True:
        # Copies the whole body
          body_copy = self.body[:] 
        # First element of previous list
          body_copy.insert(0, body_copy[0] + self.direction) 
          self.body = body_copy[:]
          self.newblock = False
        
      else:
        # Copies whole body, removing last item
          body_copy = self.body[:-1] 
        # Adds first element of previous list 
          body_copy.insert(0, body_copy[0] + self.direction) 
          self.body = body_copy[:]            
    
    # Method that checks if the snake eats a virus:
    def addBlock(self):
      self.newblock = True

    def game_logic(self):
      global blockSize, blockNumber
      over_sound = mixer.Sound('Game Over.mp3')
        
      x = """
              ________    _____      _____  ___________     ____________   _________________________._.
             /  _____/   /  _  \    /     \ \_   _____/     \_____  \   \ /   /\_   _____/\______   \ |
            /   \  ___  /  /_\  \  /  \ /  \ |    __)_       /   |   \   Y   /  |    __)_  |       _/ |
            \    \_\  \/    |    \/    Y    \|        \     /    |    \     /   |        \ |    |   \\|
             \______  /\____|__  /\____|__  /_______  /     \_______  /\___/   /_______  / |____|_  /__
                    \/         \/         \/        \/              \/                 \/         \/ \/
            """        
    # Detects when x-coordiante of snake is negative OR bigger than width of screen/when the snake hits the LEFT or RIGHT border 
      if (self.body[0][0] <= -1) or (self.body[0][0] >= blockNumber):
        over_sound.play()
        pygame.time.delay(1500)
        pygame.quit()
        print(x)
        sys.exit()

        
    # Detects when y-coordiante of snake is negative OR bigger than length of screen/when the snake hits the TOP or BOTTOM border
      if (self.body[0][1] <= -1) or (self.body[0][1] >= blockNumber):
          over_sound.play()
          pygame.time.delay(1500)
          pygame.quit()
          print(x)
          sys.exit()

    # Checks if the snake's head hits itself or any section of its own body    
      for block in self.body[1:]:
        if block == self.body[0]:
            over_sound.play()
            pygame.time.delay(1500)
            pygame.quit()
            print(x)
            sys.exit()

class Virus:
    def __init__(self):
      # Creates x and y position
        self.randomize()

    def drawVirus(self):
      # Creates virus
        virus = pygame.image.load('coronavirus.png').convert()
        virus = pygame.transform.scale(virus, (blockSize, blockSize))
      # Draws virus onto screen
        screen.blit(virus, (self.position.x*blockSize, self.position.y*blockSize))

    def randomize(self):
      # Spawns the virus in any place on the game screen
        self.x = random.randint(0, blockNumber-1)
        self.y = random.randint(0, blockNumber-1)
        self.position = Vector2(self.x, self.y)


def main():
  # Makes sure we can call variables throughout code
    global blockSize, blockNumber, screen, score 
  # Initializes pygame and title
    pygame.init()
    pygame.display.set_caption("Snake")
    score = 0

  # Creates screen, also makes board flexible 
    blockSize = 40  # Helps with the size of each block
    blockNumber = 20 # Gives the number of blocks there are
    screen = pygame.display.set_mode((blockSize*blockNumber, blockSize*blockNumber))

  # Controls FPS & makes it so that the snake doesn't go at maximum speed.
    clock = pygame.time.Clock()

  # Updates screen 
    screenUpdate = pygame.USEREVENT
    pygame.time.set_timer(screenUpdate, 300) # Will be triggered every 300 milliseconds

    virus = Virus()
    snake = Snake()

  # Plays the music on a loop
    mixer.music.load('Pixelland.mp3')
    mixer.music.play(-1)

  # Game Loop:
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
          pygame.quit()
          sys.exit()   

      # Updates the screen
        if event.type == screenUpdate:
          snake.moveSnake()
          snake.game_logic()
          
        # Snake and Virus collision:
          if virus.position == snake.body[0]:
        # Chomp sound everytime snake eats
            chomp = mixer.Sound('Cartoon Chomp.mp3')
            chomp.play()
            
            score += 1
          # Repositions virus
            virus.randomize()
            
          # Adds another block to snake
            snake.addBlock()
            
      # Checks if the user presses the keys and moves the snake accordingly
        if event.type == pygame.KEYDOWN:
          
          if event.key == pygame.K_UP:
            snake.direction = Vector2(0, -1)
          
          if event.key == pygame.K_DOWN:
            snake.direction = Vector2(0, 1)                
          if event.key == pygame.K_LEFT:
            snake.direction = Vector2(-1, 0)
          
          if event.key == pygame.K_RIGHT:
            snake.direction = Vector2(1, 0)


      # Sets the color of window
        screen.fill((133, 45, 186))
        
      # Keeps track of score and displays it on screen
        font = pygame.font.SysFont(None, 60)
        img = font.render('Score: ' + str(score) , True, (255,255,255))
        screen.blit(img, (20, 20))

      # Draws the aspects of the game 
        snake.drawSnake()
        virus.drawVirus() 

      # Controls frames per second
        clock.tick(60) # Keeps the clock the frames per second consistent and slower
        pygame.display.update()
        

main()
