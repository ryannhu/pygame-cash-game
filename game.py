import pygame
import random

pygame.init()

#assign variable for colours

BLACK = (0 , 0 , 0)
WHITE = (255, 255, 255)
GREEN = (   0, 255,   0)
RED = ( 255,   0,   0)
BLUE  = (   0,   0, 255)


size = (700 , 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Ryan\'s Game')


player = pygame.image.load('player1.png')
def draw_player(x,y):
    screen.blit(player, (x,y))


cash = pygame.image.load('cash1.png')
cash_pos = []
def draw_cash(x,y):
    screen.blit(cash, (x,y))


bear = pygame.image.load('bear1.png')
bear_pos = []
def draw_bear(x,y):
    screen.blit(bear, (x,y))

#background images
background = pygame.image.load('background.png')
death_background = pygame.image.load('death_background.png')
shop_background = pygame.image.load('shop.png')
death_image = pygame.image.load('lmao.png')

#shop images
heart = pygame.image.load('heart.png')
coke = pygame.image.load('coke.png')
printer = pygame.image.load('printer.png')

    
clock = pygame.time.Clock()
done = False

#define fonts
font = pygame.font.SysFont('Calibri', 35, True, False)
death_font = pygame.font.SysFont('Comic Sans MS', 48, True, False)
shop_font = pygame.font.SysFont('Comic Sans MS', 24, True, False)

#defining in game variables
x = 300
y = 200
x_speed = 6
y_speed = 0
jump_counter = 0
lives = 3
score = 0
true_score = 0
cash_spawn_rate = 50
bear_spawn_rate = 15
cash_mod = 1
printer_cost = 20
in_shop = False


while not done: #main event loop
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit the loop if game is closed
            done = True

        if event.type == pygame.KEYDOWN: #jump if the space key or up button is bressed
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and jump_counter < 2:
                y_speed = -20
                jump_counter += 1
            if event.key == pygame.K_s:
                in_shop = True
            
    keys = pygame.key.get_pressed() #movement of the player on the x axis based on keyboard input
    if keys[pygame.K_LEFT] == True:
        x -= x_speed
    if keys[pygame.K_RIGHT] == True :
        x += x_speed

    y += y_speed

    if lives < 1: #if lives are less than 0, go to death screen loop
        while lives < 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #quit the loop if game is closed
                    done = True
                    lives = 3

                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r or event.key == pygame.K_SPACE: #if player presses respawn, reset the values and send them out of death loop
                        lives = 3
                        score = 0
                        true_score = 0
                        cash_pos = []
                        bear_pos = []
                        cash_mod = 1
                        x_speed = 6
                        printer_cost = 20
                    
            screen.fill(WHITE) #death screen images + text
            screen.blit(death_background , (-100,-150))
            death_text = death_font.render('LMFAOOOOOO you died' , True, RED)
            respawn_text = death_font.render('Press Space or R to replay', True, RED)
            final_score = death_font.render('Your score was: $' + str(score) , True, RED)
            
            screen.blit(death_text, (50,100))
            screen.blit(respawn_text, (50, 200))
            screen.blit(final_score, (50,400))
            screen.blit(death_image, (200, 300))
            pygame.display.flip()
            
            clock.tick(60)   

    if in_shop: # if the player clicks on the shop key, enter shop
        while in_shop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #quit the loop if game is closed
                    done = True
                    in_shop = False

                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_s: #if player presses respawn, reset the values and send them out of loop
                        in_shop = False
                    if event.key == pygame.K_l and score >= 8:
                        lives += 1
                        score -= 8
                    if event.key == pygame.K_c and score >= 7:
                        x_speed *= 1.15
                        score -= 7
                    if (event.key == pygame.K_q and score >= printer_cost) or (event.key == pygame.K_q and score == 9):
                        cash_mod *= 2
                        score -= round(printer_cost)
                        printer_cost *= 1.5
                    
            #shop iamge/text        
            screen.fill(WHITE)
            screen.blit(shop_background , (-100,-150))
            welcome_text = death_font.render('Welcome to the Shop!' , True, WHITE)
            extraLife_text = shop_font.render('Press L for extra life: Cost $8', True, BLACK)
            speedBoost_text = shop_font.render('Press C for speed boost: Cost $7', True, BLACK)
            printer_text = shop_font.render('Press Q to double money picked up: Cost $' + str(round(printer_cost)), True, BLACK)
            leave_shop = shop_font.render('Press S or ESC to leave the shop' , True, WHITE)
            score_text = shop_font.render('Score: $' + str(score) , True, WHITE)

            #displaying text
            screen.blit(welcome_text, (100,10))
            screen.blit(extraLife_text, (20, 80))
            screen.blit(speedBoost_text, (20, 240))
            screen.blit(printer_text, (20, 400))
            screen.blit(leave_shop, (200,670))
            screen.blit(score_text, (50, 640))

            screen.blit(heart, (150, 130))
            screen.blit(coke, (150, 280))
            screen.blit(printer, (150, 460))

            
            pygame.display.flip()

            clock.tick(60) 

    
    if y < 600: #gravity for the player
        y_speed += 1
    else:
        y_speed = 0
        y = 600
        jump_counter = 0


    if x < -20: #bounds the player inside the window
        x = -20
    elif x > 650:
        x = 650
    
    if random.randint(1,10000) < cash_spawn_rate + true_score * 3: #random number gen to generate cash randomly, the longer the game goes on, the faster the spawning
        cash_pos.append([random.randint(1,650) , -100])

    if random.randint(1,10000) < bear_spawn_rate + true_score * 0.8: #random number gen to generate bears randomly
        bear_pos.append([random.randint(1,650) , -100])

    

    for i in range(len(bear_pos)):
        bear_pos[i][1] += 4 #gravity for bear object
        
        if(abs(bear_pos[i][0] - x -20) < 45) and (abs(bear_pos[i][1] - y - 35) < 45):
            lives -= 1 #if the player touches the bear, remove one life
            bear_pos[i][1] = 2000
            bear_pos[i][0] = 2000

    for i in range(len(cash_pos)):
        cash_pos[i][1] += 4  #gravity for the cash

        
        if (800 < cash_pos[i][1]) and (cash_pos[i][0] < 900): #check if the cash falls below the screen, remove 1 life if it happens
            lives -= 1
            cash_pos[i][1] = 2000
            cash_pos[i][0] = 2000


        if (abs(cash_pos[i][0] - x -20) < 45) and (abs(cash_pos[i][1] - y - 35) < 45): #checks if the player touches the cash
            score += (1 * cash_mod)
            true_score += 1
            cash_pos[i][1] = 2000
            cash_pos[i][0] = 2000

    

    

    
    screen.fill(WHITE)
    screen.blit(background, (0,0))

    
    for pos in cash_pos: #draw the cash on screen
        draw_cash(pos[0],pos[1])
    for pos in bear_pos: #draw the bears on screen
        draw_bear(pos[0],pos[1])
        
    draw_player(x,y)

    score_text = font.render('Score: $' + str(score) , True, GREEN)
    lives_text = font.render('Lives: ' + str(lives) , True, GREEN)
    shop_text = font.render('Press S to go to shop' , True, GREEN)
    screen.blit(score_text, (20,80))
    screen.blit(lives_text, (20,130))
    screen.blit(shop_text, (20,200))
    
    pygame.display.flip()

    clock.tick(60)


    
pygame.quit()
