
import pygame
import os
from time import sleep

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Baagh Chal") #set game title
icon = pygame.image.load("images/icon.png") #set game icon
pygame.display.set_icon(icon) #display the game icon

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50) #display game window at top left of the screen
 
#define some colors
BLACK = (0, 0, 0)
CREAM = (255,248,220)
GOLD = (222,184,135)
GRAY = (90, 90, 90)
WHITE = (255, 255, 255)
DARK_GREY = (30,30,30)

def game_reset():
    #start game variables
    global coords, tiger_coords, goat_coords, non_empty_coords, empty_coords, pos_moves, temp_tiger, temp_goat, adj, gkill, gdanger, trapped, odd_coords
    coords = [] #list for all coords
    for i in range(60, 660, 120):
        for j in range(60, 660, 120):
            coords.append([i, j])
    tiger_coords = [[60, 60], [540, 540], [60, 540], [540, 60]] #list for tiger coords
    goat_coords = [] #list for goat coords
    non_empty_coords = tiger_coords + goat_coords #list for non empty positions
    empty_coords = [] #list for empty positions
    for i in coords:
        if i not in non_empty_coords:
            empty_coords.append(i)
    pos_moves = [] #list for possible moves
    temp_tiger = [] #temporary list for selected tiger coords
    temp_goat = [] #temporary list for selected goat coords
    adj = [] #list for adjacent positions
    gkill = [] #goat kill list
    gdanger = [] #goats in danger list
    trapped = [] #trapped tiger list
    odd_coords = [[60, 180], [60, 420], [540, 180], [540, 420], [180, 60], [420, 60], [180, 540], [420, 540], [300, 180], [180, 300], [420, 300], [300, 420]] #list for all coords in which characters can't make diagonal moves
#end game variables

class Board:
    def draw(self, screen):
        # Load a wood texture image for the board background
        wood_texture = pygame.image.load('/Users/ankurgyawali/Downloads/game-main/images/wood.png')
        wood_texture = pygame.transform.scale(wood_texture, (570, 570))  # Assuming the board size
        screen.blit(wood_texture, (50, 50))

        # Set color and width for the lines
        line_color = (0, 0, 0)  # Black lines
        line_width = 4
        
        # Draw the outer square
        # pygame.draw.rect(screen, line_color, [60, 60, 540, 540], line_width)
        color = GRAY
        
        """ #reference grid for getting the coordinates of the squares placed on intersections
        for i in range(10):
            for j in range(1):
                pygame.draw.rect(screen, BLACK, [60*j, 60*i, 60, 60], 1)
        for i in range(1):
            for j in range(10):
                pygame.draw.rect(screen, BLACK, [60*j, 60*i, 60, 60], 1)
        for i in range(10):
            for j in range(4,5):
                pygame.draw.rect(screen, BLACK, [60*j, 60*i, 60, 60], 1)
        for i in range(4,7):
            for j in range(10):
                pygame.draw.rect(screen, BLACK, [60*j, 60*i, 60, 60], 1)
        for i in range(1,10):
            for j in range(1, 10):
                pygame.draw.rect(screen, BLACK, [60*j, 60*i, 60, 60], 1)
        """
        for row in range(1,5):
            for column in range(1,5):
                pygame.draw.line(screen, color, [90, 90], [570,570], 6)
                pygame.draw.line(screen, color, [90, 570], [570,90], 6)
                pygame.draw.line(screen, color, [330, 570], [570,330], 6)
                pygame.draw.line(screen, color, [90, 330], [330,570], 6)
                pygame.draw.line(screen, color, [330, 90], [570,330], 6)
                pygame.draw.line(screen, color, [90, 330], [330,90], 6)
                pygame.draw.rect(screen, color,[((120)*column-30), ((120)*row-30), 120, 120],4)

    # adding new method to draw the music button
    def draw_music_button(self, screen, music_playing):
        if music_playing:
            music_btn = pygame.image.load('/Users/ankurgyawali/Downloads/game-main/images/icons8-speaker-50.png')  # Load the music on image
        else:
            music_btn = pygame.image.load('/Users/ankurgyawali/Downloads/game-main/images/icons8-mute-50.png')  # Load the music off image
        
    

                
    def draw_tiger(self, screen):
        #draw tiger
        tiger = pygame.image.load('images/tiger.png') #load tiger image
        for c in tiger_coords:
            screen.blit(tiger, c) #draw tiger on all coordinates on tiger list

    def draw_goat(self, screen):
        #draw goat
        goat = pygame.image.load('images/goat.png') #load goat image
        for c in goat_coords:
            screen.blit(goat, c) #draw goat on all coordinates on goat list

    def place_goat(self, screen, c):
        #place goat on the board
        goat = pygame.image.load('images/goat.png')
        screen.blit(goat, c)

    def draw_pos(self, screen):
        #draw black square on all empty positions
        black_square = pygame.image.load('images/bsquare.png')
        for c in empty_coords:
            screen.blit(black_square, c)

    def get_adj(self, column, row):
	    #get adjacent goat coordinates for selected tiger
        for j in goat_coords:
            if [column+120, row] == j:
                adj.append([column+120, row])
            if [column-120, row] == j:
                adj.append([column-120, row])
            if [column, row+120] == j:
                adj.append([column, row+120])
            if [column, row-120] == j:
                adj.append([column, row-120])
            if [column, row] not in odd_coords:
                if [column+120, row+120] == j:
                    adj.append([column+120, row+120])
                if [column-120, row-120] == j:
                    adj.append([column-120, row-120])
                if [column+120, row-120] == j:
                    adj.append([column+120, row-120])
                if [column-120, row+120] == j:
                    adj.append([column-120, row+120])
	
    def poss_moves(self, column, row):
		#find the possible moves for selected tiger or goat
        for i in empty_coords: #if adjacent coords are empty, append to pos_moves list
            if [column+120, row] == i:
                pos_moves.append([column+120, row])
            if [column-120, row] == i:
                pos_moves.append([column-120, row])
            if [column, row+120] == i:
                pos_moves.append([column, row+120])
            if [column, row-120] == i:
                pos_moves.append([column, row-120])
            if [column, row] not in odd_coords:
                if [column+120, row+120] == i :
                    pos_moves.append([column+120, row+120])
                if [column-120, row-120] == i:
                    pos_moves.append([column-120, row-120])
                if [column+120, row-120] == i:
                    pos_moves.append([column+120, row-120])
                if [column-120, row+120] == i:
                    pos_moves.append([column-120, row+120])
        if [column, row] in tiger_coords: #for tiger, if adjacent coords of goat coords adjacent to the selected tiger are empty, append to pos_moves
            self.get_adj(column, row)
            for j in adj:
                if [j[0]+120, j[1]] in empty_coords and [j[0]-120, j[1]] == [column, row]:
                    pos_moves.append([j[0]+120, j[1]])
                if [j[0]-120, j[1]] in empty_coords and [j[0]+120, j[1]] == [column, row]:
                    pos_moves.append([j[0]-120, j[1]])
                if [j[0], j[1]+120] in empty_coords and [j[0], j[1]-120] == [column, row]:
                    pos_moves.append([j[0], j[1]+120])
                if [j[0], j[1]-120] in empty_coords and [j[0], j[1]+120] == [column, row]:
                    pos_moves.append([j[0], j[1]-120])
                if [j[0]+120, j[1]+120] in empty_coords and [j[0]-120, j[1]-120] == [column, row] :
                    pos_moves.append([j[0]+120, j[1]+120])
                if [j[0]-120, j[1]-120] in empty_coords and [j[0]+120, j[1]+120] == [column, row]:
                    pos_moves.append([j[0]-120, j[1]-120])
                if [j[0]+120, j[1]-120] in empty_coords and [j[0]-120, j[1]+120] == [column, row]:
                    pos_moves.append([j[0]+120, j[1]-120])
                if [j[0]-120, j[1]+120] in empty_coords and [j[0]+120, j[1]-120] == [column, row]:
                    pos_moves.append([j[0]-120, j[1]+120])		
    def trap_adj(self, column, row):
	    #get adjacent goat coordinates for all tigers
        ad = []
        for j in goat_coords:
            if [column+120, row] == j:
                ad.append([column+120, row])
            if [column-120, row] == j:
                ad.append([column-120, row])
            if [column, row+120] == j:
                ad.append([column, row+120])
            if [column, row-120] == j:
                ad.append([column, row-120])
            if [column, row] not in odd_coords:
                if [column+120, row+120] == j:
                    ad.append([column+120, row+120])
                if [column-120, row-120] == j:
                    ad.append([column-120, row-120])
                if [column+120, row-120] == j:
                    ad.append([column+120, row-120])
                if [column-120, row+120] == j:
                    ad.append([column-120, row+120])
        return ad
    
    
    def trap_moves(self, column, row):
		#find the possible moves for all tigers
        pos_move = []
        for i in empty_coords: #if adjacent coords are empty, append to pos_move list
            if [column+120, row] == i:
                pos_move.append([column+120, row])
            if [column-120, row] == i:
                pos_move.append([column-120, row])
            if [column, row+120] == i:
                pos_move.append([column, row+120])
            if [column, row-120] == i:
                pos_move.append([column, row-120])
            if [column, row] in odd_coords:
                if [column+120, row+120] == i :
                    pos_move.append([column+120, row+120])
                if [column-120, row-120] == i:
                    pos_move.append([column-120, row-120])
                if [column+120, row-120] == i:
                    pos_move.append([column+120, row-120])
                if [column-120, row+120] == i:
                    pos_move.append([column-120, row+120])
        if [column, row] in tiger_coords: #if adjacent coords of goat coords adjacent to tigers are empty, append to pos_move
            ad = self.trap_adj(column, row)
            for j in ad:
                if [j[0]+120, j[1]] in empty_coords and [j[0]-120, j[1]] == [column, row]:
                    pos_move.append([j[0]+120, j[1]])
                if [j[0]-120, j[1]] in empty_coords and [j[0]+120, j[1]] == [column, row]:
                    pos_move.append([j[0]-120, j[1]])
                if [j[0], j[1]+120] in empty_coords and [j[0], j[1]-120] == [column, row]:
                    pos_move.append([j[0], j[1]+120])
                if [j[0], j[1]-120] in empty_coords and [j[0], j[1]+120] == [column, row]:
                    pos_move.append([j[0], j[1]-120])
                if [j[0]+120, j[1]+120] in empty_coords and [j[0]-120, j[1]-120] == [column, row] :
                    pos_move.append([j[0]+120, j[1]+120])
                if [j[0]-120, j[1]-120] in empty_coords and [j[0]+120, j[1]+120] == [column, row]:
                    pos_move.append([j[0]-120, j[1]-120])
                if [j[0]+120, j[1]-120] in empty_coords and [j[0]-120, j[1]+120] == [column, row]:
                    pos_move.append([j[0]+120, j[1]-120])
                if [j[0]-120, j[1]+120] in empty_coords and [j[0]+120, j[1]-120] == [column, row]:
                    pos_move.append([j[0]-120, j[1]+120])
        return pos_move

    def get_trapped(self):
        #get list of trapped tiger coordinates
        for m in tiger_coords:
            t = self.trap_moves(m[0], m[1])
            if len(t) == 0:
                trapped.append(m)

    def draw_moves(self, screen):
        #draw blue squares on all positions with possible move for selected piece
        blue_square = pygame.image.load('images/square.png')
        for c in pos_moves:
            screen.blit(blue_square, c)

    def draw_atiger(self, screen):
        #draw selected tiger
        active_tiger = pygame.image.load('/Users/ankurgyawali/Downloads/game-main/images/tiger.png')
        if temp_tiger:
            screen.blit(active_tiger, temp_tiger[0])

    def draw_agoat(self, screen):
	    #draw selected goat
        active_goat = pygame.image.load('/Users/ankurgyawali/Downloads/game-main/images/goat.png')
        if temp_goat:
            screen.blit(active_goat, temp_goat[0])
			
    def draw_dgoat(self, screen):
        #draw goat in danger
        dgoat = pygame.image.load('images/dgoat.png')
        for c in gdanger:
            screen.blit(dgoat, c)
			
    def draw_dtiger(self, screen):
        #draw trapped tiger
        self.get_trapped()
        dtiger = pygame.image.load('/Users/ankurgyawali/Downloads/game-main/images/tiger.png')
        for c in trapped:
            screen.blit(dtiger, c)
			
    def draw_res(self, screen):
        #draw restart button
        res = pygame.image.load('/Users/ankurgyawali/Downloads/game-main/images/icons8-restart-48.png')
        screen.blit(res, [640, 60])

    def draw_start(self, screen):
        #draw start button
        start = pygame.image.load('/Users/ankurgyawali/Downloads/game-main/images/icons8-start-48.png')
        screen.blit(start, [640, 60])
		
    def draw_quit(self, screen):
        #draw quit button
        qui = pygame.image.load('/Users/ankurgyawali/Downloads/game-main/images/icons8-quit-48.png')
        screen.blit(qui, [810, 60])
    
    def draw_help(self, screen):
	    #draw help button
        help = pygame.image.load('/Users/ankurgyawali/Downloads/game-main/images/icons8-help-64.png')
        screen.blit(help, [810, 500])
		
    def draw_help_screen(self, screen):
        #draw help screen
        helps = pygame.image.load('images/help_screen.png')
        screen.blit(helps, [15, 10])
        close = pygame.image.load('images/back.png')
        screen.blit(close, [835, 10])

    def play_move(self):
        #play sound on every move
        # Load sound effects
        move_sound_effect = pygame.mixer.Sound('/Users/ankurgyawali/Downloads/game-main/sounds/move.mp3')
        # To play a sound effect
        move_sound_effect.play()
        sleep(0.2)

    def goat_killed(self):
        #play sound on every move
        # Load sound effects
        goat_killed_sound = pygame.mixer.Sound('/Users/ankurgyawali/Downloads/game-main/sounds/goat_scream.mp3')
        # To play a sound effect
        goat_killed_sound.play()
        sleep(0.2)

    def play_nomove(self):
        #play sound when selected piece has no possible moves
        pygame.mixer.music.load(open('sounds/nomove.wav', 'rb'))
        pygame.mixer.music.play()
        sleep(0.2)
		
    def play_win(self):
        #play win sound
        pygame.mixer.music.load(open('sounds/win.wav', 'rb'))
        pygame.mixer.music.play()
        sleep(0.2)
		
    def play_menu(self):
        #play sound on menu button clicks
        pygame.mixer.music.load(open('sounds/menu.wav', 'rb'))
        pygame.mixer.music.play()
        sleep(0.2)

def toggle_music():
    if pygame.mixer.music.get_busy():  # Check if music is playing
        pygame.mixer.music.pause()  # Pause the music
    else:
        pygame.mixer.music.unpause()  # Unpause the music


def main():

    # screen_info = pygame.display.Info()
    # WINDOW_SIZE = (screen_info.current_w, screen_info.current_h)
    # # Create a fullscreen window
    # screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
    # At the start of your main() function, load the music
    music_playing = True  
    pygame.mixer.music.load('/Users/ankurgyawali/Downloads/game-main/sounds/morphed-metal-discharged-cinematic-trailer-sound-effects-124763.mp3')
    pygame.mixer.music.play(-1)  # The -1 makes the music play indefinitely in a loop

    

    # start_sound = pygame.mixer.Sound('/Users/ankurgyawali/Downloads/game-main/sounds/morphed-metal-discharged-cinematic-trailer-sound-effects-124763.mp3')
    # start_sound.play()


    WINDOW_SIZE = [1280,720] #set the HEIGHT and WIDTH of the screen
    screen = pygame.display.set_mode(WINDOW_SIZE) #screen to display
    clock = pygame.time.Clock() #used to manage how fast the screen updates
    board = Board()
    turn = 1 #players' turn flag
    gcount = 0 #count goats placed on board
    selected = 0 #flag to know a piece is selected, 1 when piece is selected, otherwise 0
    refresh = True #flag to refresh the display screen, refresh the display when True
    fmsg = '' #win message
    msg = '' #gameplay messages
    game_end = False #flag to decide game has ended, False when game is running, True when game is over
    start = False #flag to decide game is running, False when game is not started, True when game is running
    game_help = False #flag for help screen, True when help screen is on display, false otherwise
    done = False #flag to close the game, close the game when True
    reset = True #flag to reset the game variables when game is restarted

     # Load music button images
    music_on_img = pygame.image.load('/Users/ankurgyawali/Downloads/game-main/images/icons8-speaker-50.png')
    music_off_img = pygame.image.load('/Users/ankurgyawali/Downloads/game-main/images/icons8-mute-50.png')

    # Scaling images to a suitable size (if needed)
    music_on_img = pygame.transform.scale(music_on_img, (50, 50))
    music_off_img = pygame.transform.scale(music_off_img, (50, 50))

	
    def displayvars():
        #display variables on the screen
        font = pygame.font.Font('fonts/ErasBoldITC.ttf', 25)
        if turn == 1 and start == True and game_end == False:  #Conditions to display text on screen
            text1 = "Goat's Turn."
        elif turn == 2 and start == True and game_end == False:
            text1 = "Tiger's Turn."
        elif game_end == True:
            text1 = "Game Over."
        else:
            text1 = ""
        text2="Goats in hand: "+str(20-gcount)
        text3="Goats captured: "+str(len(gkill))
        text4="Goats on board: "+str(gcount-len(gkill))
        text5= msg
        text6= fmsg
        tt = []
        for kk in trapped:
            if kk not in tt:
                tt.append(kk)
        text="Tigers trapped: "+str(len(tt))     
        textSurf = font.render(text5, True, WHITE)
        screen.blit(textSurf,(60,15))
        textSurf = font.render(text2, True, WHITE)
        screen.blit(textSurf,(1020,200))
        textSurf = font.render(text4, True, WHITE)
        screen.blit(textSurf,(1020,250))
        textSurf = font.render(text3, True, WHITE)
        screen.blit(textSurf,(1020,300))
        textSurf = font.render(text, True, WHITE)
        screen.blit(textSurf,(1020,350))
        textSurf = font.render(text1, True, WHITE)
        screen.blit(textSurf,(760,15))
        textSurf = font.render(text6, True, WHITE)
        if len(gkill) == 5 or len(tt) == 4:
            pygame.draw.rect(screen, GOLD, [50, 270, 560, 100])
            screen.blit(textSurf,(150,305))

    while not done:            # -------- Main Program Loop -----------

        
        if reset == True:
            game_reset()
            turn = 1
            gcount = 0
            selected = 0
            reset = False
        
        if len(gkill) == 5:                #checks goats kills to know if tiger wins
            fmsg = 'GAME OVER! TIGER WON!'   
            reset = True
            game_end = True
            board.play_win()
            
        tt = []
        for kk in trapped:                 #for loop to get trapped tigers without duplicates
            if kk not in tt:
                tt.append(kk)
        
        if len(tt) == 4:                   #checks tiger trapped to know if goats wins
            fmsg = 'GAME OVER! GOAT WON!'
            reset = True
            game_end = True
            refresh = True
            board.play_win()
        
                
        if refresh == True:
            screen.fill(DARK_GREY) #set the screen background

             # Decide which music button image to display
            music_btn = music_on_img if music_playing else music_off_img
            screen.blit(music_btn, (760, 500))  # Adjust coordinates as needed

            pygame.display.flip()
            refresh = False
            if game_help == True:
                board.draw_help_screen(screen) #draw help screen when help is True
            
            elif game_help == False: #draw game screen when help is false
                board.draw(screen) #draw screen
                board.draw_tiger(screen) #draw tiger pieces
                # board.draw_pos(screen) #draw all empty positions
                board.draw_goat(screen) #draw goats
                board.draw_moves(screen) #draw all possible moves
                board.draw_atiger(screen) #draw selected tiger
                board.draw_agoat(screen) #draw selected goat
                board.draw_dgoat(screen) #draw goat in danger
                board.draw_dtiger(screen) #draw trapped tiger
                board.draw_help(screen) #draw help button
                board.draw_music_button(screen, music_playing)

                
                if start == True: #when start is True
                    board.draw_res(screen) #draw restart button
                    displayvars() #and display variables
                
                if start == False: #when start is false
                    board.draw_start(screen) #draw start button in place of restart button
                board.draw_quit(screen) #draw quit button
            
            refresh = False #reset refresh flag to False
            msg = '' #reset msg to ''
            fmsg = '' #reset fmsg to ''
            
        for event in pygame.event.get():
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column, row = pos

                # Assume music_btn is the correct image based on the current state
                music_btn = music_on_img if music_playing else music_off_img

                # Now you can check if the click was within the bounds of the music button
                if 760 <= column <= 760 + music_btn.get_width() and 500 <= row <= 500 + music_btn.get_height():
                    toggle_music()
                    music_playing = not music_playing
                    refresh = True


            if event.type == pygame.MOUSEBUTTONDOWN and start == False and game_help == False: #start the game when user clicks start button when start is False, help is False
                pos = pygame.mouse.get_pos()
                column,row = pos
                
                if column >= 640 and column <=790 and row >=60 and row <=100:
                
                    start = True
                    refresh = True
                    msg = 'Game started.'
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("/Users/ankurgyawali/Downloads/game-main/sounds/horror-chase-music-loop-67634.mp3")
                    pygame.mixer.music.play(-1)
                    continue
            if event.type == pygame.MOUSEBUTTONDOWN and game_help == False: # gets the help menu if user clicks help button and when help is False. 
                pos = pygame.mouse.get_pos()
                column = pos[0]
                row = pos[1]
                
                if column >= 810 and column <=910 and row >=500 and row <=540:
                    refresh = True
                    game_help = True
                    board.play_menu()

            if event.type == pygame.MOUSEBUTTONDOWN and game_help == True: # exits the help menu if user clicks exit button in help menu and when help is True.
                pos = pygame.mouse.get_pos()
                column = pos[0]
                row = pos[1]
                
                if column >= 840 and column <=940 and row >=10 and row <=50:
                    refresh = True
                    game_help = False
                    board.play_menu()
					
            if event.type == pygame.MOUSEBUTTONDOWN and game_end == True and start == True and game_help == False: #reset the game after game is over and if restart button is clicked
                    pos = pygame.mouse.get_pos()
                    column = pos[0]
                    row = pos[1]
                    
                    if column >= 640 and column <=790 and row >=60 and row <=100:
                        reset = True
                        refresh = True
                        game_end = False
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("/Users/ankurgyawali/Downloads/game-main/sounds/horror-chase-music-loop-67634.mp3")
                        pygame.mixer.music.play(-1)
                        msg = 'Game restarted.'

            if event.type == pygame.MOUSEBUTTONDOWN and game_end == True and start == True and game_help == False: #quit if quit button is clicked
                    pos = pygame.mouse.get_pos()
                    column = pos[0]
                    row = pos[1]
                    
                    if column >= 810 and column <=910 and row >=60 and row <=100:
                        done = True
                        board.play_menu()

            if event.type == pygame.MOUSEBUTTONDOWN and game_end == False and start == False and game_help == False: #quit if quit button is clicked
                    pos = pygame.mouse.get_pos()
                    column = pos[0]
                    row = pos[1]
                    
                    if column >= 810 and column <=910 and row >=60 and row <=100:
                        done = True
                        board.play_menu()
						
            if event.type == pygame.QUIT:  # If user clicked close
                done = True        # Flag that we are done so we exit this loop

            elif game_end == False and start == True and game_help == False: #when game is started but not over
                if event.type == pygame.MOUSEBUTTONDOWN: #reset the game if restart button is clicked
                    pos = pygame.mouse.get_pos()
                    column = pos[0]
                    row = pos[1]
                    
                    if column >= 640 and column <=790 and row >=60 and row <=100:
                        reset = True
                        refresh = True
                        msg = 'Click any empty black square to place a goat.'

                if event.type == pygame.MOUSEBUTTONDOWN: #quit if quit button is clicked
                    pos = pygame.mouse.get_pos()
                    column = pos[0]
                    row = pos[1]
                    
                    if column >= 810 and column <=910 and row >=60 and row <=100:
                        done = True
                        board.play_menu()

                if event.type == pygame.MOUSEBUTTONDOWN and turn == 1 and gcount < 20: #first place 20 goats on the board
                    pos = pygame.mouse.get_pos()
                    column = 60*(pos[0] // 60)
                    row = 60*(pos[1] // 60)
                    
                    if [column, row] in empty_coords:
                        board.place_goat(screen, [column, row])
                        empty_coords.remove([column, row])
                        goat_coords.append([column, row])
                        gcount += 1
                        turn = 2
                        refresh = True
                        board.play_move()

                elif event.type == pygame.MOUSEBUTTONDOWN and turn == 1 and gcount == 20 and selected == 0: #select goat after 20 goats have been placed
                    pos = pygame.mouse.get_pos()
                    column = 60*(pos[0] // 60)
                    row = 60*(pos[1] // 60)
                    
                    if [column, row] in goat_coords: #select the goat
                        board.poss_moves(column, row)
                        
                        if len(pos_moves) == 0: #if selected goat has no moves
                            msg = "Goat can't move. Select a different goat."
                            del pos_moves[:]
                            refresh = True
                            board.play_nomove()
                            continue
                        
                        temp_goat.append([column, row])
                        goat_coords.remove(temp_goat[0])
                        selected = 1
                        refresh = True

                elif event.type == pygame.MOUSEBUTTONDOWN and turn == 1 and gcount == 20 and selected == 1: #move the goat
                    pos = pygame.mouse.get_pos()
                    column = 60*(pos[0] // 60)
                    row = 60*(pos[1] // 60)
                    
                    if [column, row] in temp_goat: #if goat is deselected
                        goat_coords.append([column, row])
                        selected = 0
                        del pos_moves[:]
                        del temp_goat[:]
                        refresh = True
                    
                    if [column, row] in pos_moves: #if goat is moved
                        goat_coords.append([column, row])
                        empty_coords.append(temp_goat[0])
                        empty_coords.remove([column, row])
                        board.play_move()
                        del temp_goat[:]
                        del pos_moves[:]
                        del trapped[:]
                        selected = 0
                        turn = 2
                        refresh = True

                elif event.type == pygame.MOUSEBUTTONDOWN and turn == 2 and selected == 0: #select the tiger
                    pos = pygame.mouse.get_pos()
                    column = 60*(pos[0] // 60)
                    row = 60*(pos[1] // 60)
                    
                    if [column, row] in tiger_coords: #select the tiger
                        board.poss_moves(column, row)
                        
                        if len(pos_moves) == 0: #if selected tiger is trapped
                            msg = 'Tiger is trapped. Select a different tiger.'
                            refresh = True
                            del pos_moves[:]
                            board.play_nomove()
                            continue
                        
                        temp_tiger.append([column, row])
                        tiger_coords.remove(temp_tiger[0])
                        
                        for i in pos_moves:
                            tgx = (i[0]+temp_tiger[0][0])/2
                            tgy = (i[1]+temp_tiger[0][1])/2
                            
                            if [tgx, tgy] in goat_coords:
                                gdanger.append([tgx, tgy])
                        
                        selected = 1
                        refresh = True
                        
                elif event.type == pygame.MOUSEBUTTONDOWN and turn == 2 and selected == 1: #move the tiger
                    pos = pygame.mouse.get_pos()
                    column = 60*(pos[0] // 60)
                    row = 60*(pos[1] // 60)
                    
                    if [column, row] in temp_tiger: #if tiger is deselected
                        tiger_coords.append([column, row])
                        selected = 0
                        del pos_moves[:]
                        del temp_tiger[:]
                        del adj[:]
                        del gdanger[:]
                        refresh = True
                    
                    if [column, row] in pos_moves: #if tiger is moved
                        tiger_coords.append([column, row])
                        empty_coords.append(temp_tiger[0])
                        selected = 0
                        empty_coords.remove([column, row])
                        tgx = (column + temp_tiger[0][0])/2
                        tgy = (row + temp_tiger[0][1])/2
                        if [tgx, tgy] in goat_coords:
                            board.goat_killed()
                            gkill.append([tgx, tgy])
                            goat_coords.remove([tgx, tgy])
                            empty_coords.append([tgx, tgy])
                        else:
                            board.play_move()
                        del pos_moves[:]
                        del temp_tiger[:]
                        del adj[:]
                        del gdanger[:]
                        del trapped[:]
                        turn = 1
                        refresh = True

        pygame.display.flip()
main()
