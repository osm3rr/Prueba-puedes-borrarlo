import pygame,random

pygame.init()

width=800
height=600

display_surface=pygame.display.set_mode((width,height))
pygame.display.set_caption("Feed the Dragon")

#set FPS and Clock
FPS=60
clock=pygame.time.Clock()

#Set game values
Player_lives=1
Player_velocity=10
Coin_velocity=5
Coin_aceleration = 0.5
screen_distance = 100 #distancia antes de entrar a la pantalla

coin_place= width+screen_distance

#Para reiniciar el contador
score=0
#Estas dos lineas me parecen un poco innecesario pero si borro esto, debo modificar los nombre a lo largo del codigo :(
players_lives = Player_lives
player_velocity=Player_velocity


#Set colors
Black=(0,0,0)
Green=(0,255,0)
white=(255,255,255)
DarkGreen=(10,50,10) 

#Set Fonts
Custom_font=pygame.font.Font('AttackGraffiti.ttf',32)

#Set text

score_text = Custom_font.render("Score: "+str(score), True, Green, DarkGreen)
score_rect=score_text.get_rect()
score_rect.topleft = (10,10)

title_text=Custom_font.render("Feed the dragon: ", True, Green, DarkGreen)
title_rect=title_text.get_rect()
title_rect.center =((width/2), 30)

lives_text=Custom_font.render("Vidas: "+str(players_lives), True, Green, DarkGreen)
lives_rect=lives_text.get_rect()
lives_rect.topright=(width-10,10) #Si no colocas ese width, lo va a colocar a la misma distancia que el rect de score

game_over_text=Custom_font.render("GAME OVER", True, Green, DarkGreen)
game_over_rect=game_over_text.get_rect()
game_over_rect.center =(width/2,height/2)

play_again_text=Custom_font.render("Play Again", True, Green, DarkGreen)
play_again_rect=play_again_text.get_rect()
play_again_rect.center=(width/2,height/2 +32)

#Set sounds and music
coin_sound=pygame.mixer.Sound("coin_sound.wav")
miss_sound=pygame.mixer.Sound("miss_sound.wav")
pygame.mixer.music.load('ftd_background_music.wav')

#Set image
dragon_image=pygame.image.load("dragon_right.png")
dragon_rect=dragon_image.get_rect()
dragon_rect.topleft=(32,height/2)

coin_image=pygame.image.load("coin.png")
coin_rect=coin_image.get_rect()
coin_rect.x=coin_place
coin_rect.y=random.randint(64, height-32)#entender las posiciones*****

#Set background
castle_image=pygame.image.load("castle.png")
castle_image = pygame.transform.scale(castle_image, (width, height))



pygame.mixer.music.play(-1,0)#-1 es para que siempre se reproduzca


running=True

while running:

    #Move the dragon

    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP] and dragon_rect.top>64:
        dragon_rect.y -= Player_velocity

    if keys[pygame.K_DOWN] and dragon_rect.bottom<height:
        dragon_rect.y += Player_velocity

    #Move the coin
    if coin_rect.x < 0:
        players_lives -=1
        miss_sound.play()
        #reposicionar
        coin_rect.x = coin_place
        coin_rect.y = random.randint(64, height-32)
    else:
        #Move the coin
        coin_rect.x -= Coin_velocity

    #check for collision
        if dragon_rect.colliderect(coin_rect):
            score = score + 1
            coin_sound.play()
            print("score: "+str(score))
            Coin_velocity = Coin_velocity + Coin_aceleration
            #Subimos la velocidad cada dos collisiones porque no podemos subir 0.5 pixeles
            #reposicionar
            coin_rect.x = coin_place
            coin_rect.y = random.randint(64, height-32)
        #Actualizar el texto ya renderizado
        score_text = Custom_font.render("Score: "+str(score), True, Green, DarkGreen)
        lives_text = Custom_font.render("Vidas: "+str(players_lives), True, Green, DarkGreen)

        #Check for game over
        if players_lives == 0:
            #copiar en pantalla los rectagulos definidos para game over y continuar
            display_surface.blit(game_over_text,game_over_rect)
            display_surface.blit(play_again_text,play_again_rect)
            pygame.display.update()

            #pause the game until player presses a key, the reset the game
            pygame.mixer.music.stop()
            paused = True
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        score=0
                        players_lives=1
                        Coin_velocity=5
                        dragon_rect.y = height/2
                        pygame.mixer.music.play()
                        paused=False

                    #Salir del juego
                    if event.type==pygame.QUIT:
                        paused=False
                        running=False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    display_surface.blit(castle_image,(0,0))

    #ASSETS
    display_surface.blit(dragon_image,dragon_rect)
    display_surface.blit(coin_image,coin_rect)
    #text
    display_surface.blit(score_text,score_rect)
    display_surface.blit(title_text,title_rect)
    display_surface.blit(lives_text,lives_rect)

    #Line
    pygame.draw.line(display_surface,(255,255,255),(0,64),(width,64),2)




    pygame.display.update()
    clock.tick(FPS)
