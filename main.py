#game star wars
import pygame
import os
pygame.mixer.init()
pygame.font.init()
#HEALTH FONT
HEALTH_FONT =pygame.font.SysFont('comicsans',40)
WINNER_FONT =pygame.font.SysFont('comicsans',100)
#sound
BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join('Assets','L.mp3'))
PLAYER_1_WIN_SOUND=pygame.mixer.Sound(os.path.join('Assets','player1.mp3'))
PLAYER_2_WIN_SOUND=pygame.mixer.Sound(os.path.join('Assets','player2.mp3'))

BACKGROUND_SOUND=pygame.mixer.Sound(os.path.join('Assets','B.mp3'))

#screen
WIDTH,HEIGHT =1000,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("my game!")
#BULLET SPEED
BULLET_VAL=7
#num of bullet
MAX_BULLET=10
#BORDER BETWEEN TO PLAYERS
BORDER = pygame.Rect(WIDTH//2-5,0,10,HEIGHT)
##event
PLAYER_1_HIT =pygame.USEREVENT +1
PLAYER_2_HIT =pygame.USEREVENT +2
#clock
FPS=60
#players size
PLAYER_WIDTH,PLAYER_HEIGHT=60,60
#uploding images
PLAYER_1_IMAGE =pygame.image.load(os.path.join('Assets','spaceship_red.png'))
PLAYER_1=pygame.transform.rotate(pygame.transform.scale
(PLAYER_1_IMAGE,(PLAYER_WIDTH,PLAYER_HEIGHT)),270)

PLAYER_2_IMAGE=pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
PLAYER_2=pygame.transform.rotate(pygame.transform.scale
(PLAYER_2_IMAGE,(PLAYER_WIDTH,PLAYER_HEIGHT)),90)

EXPLODE_IMAGE =pygame.image.load(os.path.join('Assets','explode.png'))
EXPLODE=pygame.transform.rotate(pygame.transform.scale
(EXPLODE_IMAGE,(PLAYER_WIDTH+30,PLAYER_HEIGHT+30)),90)
#background
SPACE_IMAGE =pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))


def draw_window(player_1,player_2,bullet_1,bullet_2,player_1_health,player_2_health):
    #screen
    WIN.blit(SPACE_IMAGE,(0,0))
    #Draws the border
    pygame.draw.rect(WIN, 'black', BORDER)
    #Draws the players using the coordinates of the rectangle
    WIN.blit(PLAYER_1,(player_1.x,player_1.y))
    WIN.blit(PLAYER_2,(player_2.x, player_2.y))
    #Draws  the text
    player_1_health_text =HEALTH_FONT.render("Health : "+str(player_1_health),1,'white')
    player_2_health_text = HEALTH_FONT.render("Health: " + str(player_2_health), 1, 'white')
    # player1 = HEALTH_FONT.render("player 1  "+str(player_1_health),1,'white')
    player1 = HEALTH_FONT.render("player 1  ", 1, 'white')
    player2=HEALTH_FONT.render("player 2 ", 1, 'white')

    #position of the "HEALTH"
    WIN.blit(player_1_health_text, (WIDTH - player_1_health_text.get_width() + -10, 450))
    WIN.blit(player_2_health_text, (10, 450))
    WIN.blit(player1,(WIDTH - player_1_health_text.get_width() + -10, 10))
    WIN.blit(player2, (10,10))

    #Draws the bullets
    for bullet in bullet_1:
        #     WIN.blit(heart, (100, 200))
        pygame.draw.rect(WIN,'red',bullet)
    for bullet in bullet_2:
        pygame.draw.rect(WIN,'yellow',bullet)
    pygame.display.update()


def draw_winner(text):
    draow_text= WINNER_FONT.render(text,1,'white')
    WIN.blit(draow_text,(WIDTH/2-draow_text.get_width()/2,HEIGHT/2-draow_text.get_height()/2) )
    pygame.display.update()
    #pouse
    pygame.time.delay(5000)


def keys_move(player_1,player_2):
    # player_2 =(w,a,s,d)
    # player_1 =(arrows)
    keys_pressed = pygame.key.get_pressed()
################################################
                                  # we dont want to cross the border
    if keys_pressed[pygame.K_LEFT] and player_1.x>BORDER.x: # LEFT
        player_1.x -= 5
    if keys_pressed[pygame.K_RIGHT]and player_1.x<950:  # RIGHT
        player_1.x += 5
    if keys_pressed[pygame.K_DOWN] and player_1.y + 5 < 450:  # DOWN
        player_1.y += 5
    if keys_pressed[pygame.K_UP] and player_1.y + 5 > 0:  # UP
        player_1.y -= 5
        ##########################
    if keys_pressed[pygame.K_a]and player_2.x-5>0:  # LEFT
        player_2.x -= 5
    if keys_pressed[pygame.K_d] and player_2.x+60<BORDER.x: # RIGHT
        player_2.x += 5
    if keys_pressed[pygame.K_s] and player_2.y+5 <450: # DOWN
        player_2.y += 5
    if keys_pressed[pygame.K_w]and player_2.y+5 >0:  # UP
        player_2.y-= 5


def handle_bullets(bullets_1,bullets_2,player_1,player_2):
    for bullet in bullets_1:
        bullet.x-=BULLET_VAL
        if player_2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER_2_HIT))
            bullets_1.remove(bullet)
        elif bullet.x>WIDTH:
            bullets_1.remove(bullet)

    for bullet in bullets_2:
        bullet.x+=BULLET_VAL
        if player_1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER_1_HIT))
            bullets_2.remove(bullet)
        elif bullet.x<0:
            bullets_1.remove(bullet)


#loop that quit the game
def main():
    player_1_health = 10
    player_2_health = 10
    player_1= pygame.Rect(550,150,PLAYER_WIDTH,PLAYER_HEIGHT)
    player_2 =pygame.Rect(100,150,PLAYER_WIDTH,PLAYER_HEIGHT)
    bullets_1 =[]
    bullets_2 =[]
    clock=pygame.time.Clock()
#while loop
    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                #function
            if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_LCTRL and len(bullets_2)<MAX_BULLET:
                            #bullit is rectangle
                        bullet=pygame.Rect(player_2.x+player_2.width,player_2.y+player_2.height//2-2,10,5)
                             #list of bullets
                        BULLET_FIRE_SOUND.play()
                        bullets_2.append(bullet)
                    if event.key == pygame.K_SPACE and len(bullets_1)<MAX_BULLET:
                        bullet = pygame.Rect(player_1.x , player_1.y + player_1.height // 2 - 2, 10, 5)
                        bullets_1.append(bullet)
                        BULLET_FIRE_SOUND.play()
            if event.type==PLAYER_1_HIT:
                player_1_health-=1
                BULLET_HIT_SOUND.play()

            if event.type == PLAYER_2_HIT:
                player_2_health-=1
                #loading music
                BULLET_HIT_SOUND.play()
        winner_text=""
        if player_1_health<=0:
            PLAYER_2_WIN_SOUND.play()
            pygame.time.delay(500)
            WIN.blit(EXPLODE,(player_1.x,player_1.y))
            winner_text='player 2 wins!'


        if player_2_health <=0:
            PLAYER_1_WIN_SOUND.play()
            pygame.time.delay(500)
            WIN.blit(EXPLODE, (player_2.x, player_1.y))
            winner_text = 'player 1 wins!'



        if winner_text!="":
            draw_winner(winner_text)
            break
        #print(bullets_1,bullets_2)
        draw_window(player_1,player_2,bullets_1,bullets_2,player_1_health,player_2_health)
        keys_move(player_1,player_2)
        handle_bullets(bullets_1,bullets_2,player_1,player_2)
#must
    pygame.quit()


if __name__=="__main__":
    main()



