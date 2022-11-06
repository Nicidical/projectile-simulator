"""
Imports
"""
import inputvariables as invar
import pygame
import sys
import text as tex
from math import sin,cos,floor,radians



"""
Initialization
"""
# Intializing
pygame.init()
X = 1280
Y = 720
display = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Basic Projectile Simulator')

#Initializing Core Variables
#Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gcolor = (100, 100, 100)

#Images of background and ufo
bg = pygame.image.load('images/bg.png')
ufo = pygame.image.load('images/ufo.png')

#Variables
center = (X // 2, Y // 2)
state = [-1,0,0]
font = pygame.font.Font('freesansbold.ttf', 36)
font2 = pygame.font.Font('freesansbold.ttf', 180)
FPS = 60 # Frames per second
fpsClock = pygame.time.Clock()
traveltime = 0 #Frames that the projectile travels for
timer = FPS #Used for the countdown beforehand
changestate1 = False
state2setup = True

#Changing all of the input variables and storing them inside an array
inputvars = []
inputvars.append(list(invar.g))
inputvars.append(list(invar.iv))
inputvars.append(list(invar.ih))
inputvars.append(list(invar.a))
newinputvars = {}
newinputvars["gravity"] = ""
newinputvars["initialvelo"] = ""
newinputvars["initialh"] = ""
newinputvars["angle"] = ""
inputkeys = newinputvars.keys()
inputkeys = list(inputkeys)

#Text Intialization
text = []
texts = []
textrect = []
textrects = []
for entry in tex.alltext:
    for t in entry:
        temptext = font.render(t, True, white)
        text.append(temptext)
        temprect = temptext.get_rect()
        temprect.center = (center[0], center[1] // (5/3))
        textrect.append(temprect)
    texts.append(text)
    textrects.append(textrect)
    textrect = []
    text = []

#The text displayed to continue
ctext = font.render('Press enter to continue.', True, white)
crect = ctext.get_rect()
crect.center = (center[0], int(center[1] * (4/3)))

#The text displayed at the start
stext = font.render('Press 1, 2, 3, 4, or 5 (if avaliable) to increase the corresponding digits.', True, white)
srect = stext.get_rect()
srect.center = (center[0], center[1] // (5/3))

#The period displayed between digits in the input phase
period = font.render('.', True, white)
prect = period.get_rect()
prect.center = (center[0], center[1] * (4/3))

#The variables used for when the ufo begins traveling
initialy = 0
currenty = 0
currentx = 0
prevy = 0
ally = set()
allvy = set()



"""
Functions
"""
def safe_pop(arr,index):
    temparr = arr.copy()
    return temparr.pop(index)

# The Main Loop
if __name__ == "__main__":
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or newinputvars["gravity"] == "00.00":
                pygame.quit()
                sys.exit()
            
            temp1 = safe_pop(state,1)
            temp2 = safe_pop(state,2)
            
            #Keyboard Events
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                if event.key == pygame.K_RETURN:
                    if state[0] == -1:
                        state[0] = 0
                    if state[0] == 0:
                        if texts[temp1][temp2] != texts[temp1][-1]:
                            state[2] += 1
                        elif texts[temp1][temp2] == texts[temp1][-1]:
                            state[2] = 0
                            tempcount = 0
                            for char in inputvars[temp1]:
                                newinputvars[inputkeys[temp1]] = newinputvars[inputkeys[temp1]] + char
                                if len(newinputvars[inputkeys[temp1]]) == len(inputvars[temp1]) - 2:
                                    newinputvars[inputkeys[temp1]] = newinputvars[inputkeys[temp1]] + "."                
                            if state[1] == len(texts) - 1:
                                state[1] = 0
                                state[0] += 1
                                changestate1 = True
                            state[1] += 1
                if texts[temp1][temp2] == texts[temp1][-1]:
                    if event.key == pygame.K_1:
                        tempnum = int(inputvars[temp1][0])
                        if tempnum == 9:
                            tempnum = 0
                        else:
                            tempnum += 1
                        inputvars[temp1][0] = str(tempnum)
                    elif event.key == pygame.K_2:
                        tempnum = int(inputvars[temp1][1])
                        if tempnum == 9:
                            tempnum = 0
                        else:
                            tempnum += 1
                        inputvars[temp1][1] = str(tempnum)
                    elif event.key == pygame.K_3:
                        tempnum = int(inputvars[temp1][2])
                        if tempnum == 9:
                            tempnum = 0
                        else:
                            tempnum += 1
                        inputvars[temp1][2] = str(tempnum)
                    elif event.key == pygame.K_4:
                        tempnum = int(inputvars[temp1][3])
                        if tempnum == 9:
                            tempnum = 0
                        else:
                            tempnum += 1
                        inputvars[temp1][3] = str(tempnum)
                    elif event.key == pygame.K_5 and len(inputvars[temp1]) >= 5:
                        tempnum = int(inputvars[temp1][4])
                        if tempnum == 9:
                            tempnum = 0
                        else:
                            tempnum += 1
                        inputvars[temp1][4] = str(tempnum)
        
        #Text Display Events        
        if state[0] == -1:
            display.fill(black)
            display.blit(bg,(0,0))
            display.blit(stext,srect)
            display.blit(ctext,crect)
            
        elif state[0] == 0:
            display.fill(black)
            display.blit(bg,(0,0))
            display.blit(texts[temp1][temp2], textrects[temp1][temp2])
            if texts[temp1][temp2] != texts[temp1][-1]:
                display.blit(ctext,crect)
            else:
                unit = len(inputvars[temp1])
                halfunit = int(floor(unit / 2))
                space = 20
                count = 0
                for digit in inputvars[temp1]:
                    tempvar = font.render(digit, True, white)
                    temprect = tempvar.get_rect()
                    if len(inputvars[temp1]) % 2 != 0:
                        temprect.center = (center[0] - ((halfunit - count) * space), center[1] * (4/3))                    
                        if halfunit - count == 0:
                            prect.center = (center[0] + space, center[1] * (4/3))
                            display.blit(period,prect)
                            count += 1
                    else:
                        temprect.center = (center[0] - ((halfunit - count) * space), center[1] * (4/3))
                        if halfunit - count == 1:
                            prect.center = (center[0], center[1] * (4/3))
                            display.blit(period,prect)
                            count += 1
                    
                    display.blit(tempvar,temprect)
                    count += 1
                    
        elif state[0] == 1:
            if changestate1:
                state[1] -= 1
            changestate1 = False
            if state[1] == 0:
                display.fill(black)
                message = font2.render("Get Ready!", True, white)
                messagerect = message.get_rect()
                messagerect.center = (center)
            elif state[1] == 1:
                display.fill(white)
                message = font2.render("3!", True, black)
                messagerect = message.get_rect()
                messagerect.center = (center)
            elif state[1] == 2:
                display.fill(red)
                message = font2.render("2!", True, black)
                messagerect = message.get_rect()
                messagerect.center = (center)
            elif state[1] == 3:
                display.fill(blue)
                message = font2.render("1!", True, black)
                messagerect = message.get_rect()
                messagerect.center = (center)
            elif state[1] == 4:
                display.fill(green)
                message = font2.render("GO!", True, black)
                messagerect = message.get_rect()
                messagerect.center = (center)
            elif state[1] == 5:
                display.fill(black)
                display.blit(bg,(0,0))
                initialy = initialh = float(newinputvars['initialh'])
                display.blit(ufo,(0,Y-initialy-113))
            if state[1] != 5:
                display.blit(message,messagerect)
            timer -= 1
            if timer == 0:
                if state[1] < 5:
                    state[1] += 1
                    timer = FPS
                else:
                    state[0] = 2
                    state[1] = 0
                    
        elif state[0] == 2:
            #Calculation
            if state2setup:
                gravity = float(newinputvars['gravity'])
                initialvelo = float(newinputvars['initialvelo'])        
                initialh = float(newinputvars['initialh'])
                angle = min(float(newinputvars['angle']),90)
                yvelo = initialvelo*sin(radians(angle))
                xvelo = initialvelo*cos(radians(angle))
                currenty += (yvelo/FPS + initialh)
                state2setup = False
            else:
                yvelo -= gravity/FPS
                currenty += yvelo/FPS
            currentx += xvelo/FPS

            ally.add(currenty)
            allvy.add(abs(yvelo))
            
            #Drawing Everything
            display.fill(black)
            display.blit(bg,(0,0))
            display.blit(ufo,(min(currentx,X/2),max(Y - currenty - 113,Y/2)))
            xmessage = font.render("X: {0:.2f}m".format(currentx), True, white)
            ymessage = font.render("Y: {0:.2f}m".format(currenty), True, white)
            xvmessage = font.render("X Vel: {0:.2f}m/s".format(xvelo), True, white)
            yvmessage = font.render("Y Vel: {0:.2f}m/s".format(yvelo), True, white)
            gmessage  = font.render("Grav: {0:.2f}m/(s*s)".format(gravity), True, white)
            amessage = font.render("Angle: {0:.2f} degrees".format(angle), True, white)
            tmessage = font.render("Total Time: {0:.2f}s".format(traveltime / 60), True, white)

            display.blit(xmessage,(0,0))
            display.blit(ymessage,(0,35))
            display.blit(xvmessage,(0,70))
            display.blit(yvmessage,(0,105))
            display.blit(gmessage,(0,140))
            display.blit(amessage,(0,175))
            display.blit(tmessage,(0,210))
            
            traveltime += 1
            if currenty <= 0:
                state[0] = 3
        
        elif state[0] == 3:
           display.fill(black)
           display.blit(bg,(0,0))
           display.blit(ufo,(min(currentx,X/2),max(Y - currenty - 113,Y/2)))
           endmessage1 = font.render("And that's a wrap!", True, white)
           endmessage2 = font.render("Final Results:", True, white)
           finaldist = font.render("Horizontal Distance Traveled: {0:.2f} meters".format(currentx), True, white)
           maxheight = font.render("Maximum Height: {0:.2f} meters".format(max(ally)), True, white)
           maxvelo = font.render("Maximum Y Velocity: {0:.2f} meters per second".format(max(allvy)), True, white)
           timetraveled = font.render("Total Time: {0:.2f} seconds".format(traveltime / 60), True, white)
           endmessage3 = font.render("Thanks a bunch for playing!", True, white)
           endmessage4 = font.render("Designed and coded for Hack RPI 2022 by: Ryan Tedaldi", True, white)
           
           messagerect = endmessage1.get_rect()
           messagerect.center = (center[0],17)
           display.blit(endmessage1,messagerect)
           
           messagerect = endmessage2.get_rect()
           messagerect.center = (center[0],52)
           display.blit(endmessage2,messagerect)
           
           messagerect = finaldist.get_rect()
           messagerect.center = (center[0],Y // 2 - 52)
           display.blit(finaldist,messagerect)
           
           messagerect = maxheight.get_rect()
           messagerect.center = (center[0],Y // 2 - 17)
           display.blit(maxheight,messagerect)
           
           messagerect = maxvelo.get_rect()
           messagerect.center = (center[0],Y // 2 + 17)
           display.blit(maxvelo,messagerect)
           
           messagerect = timetraveled.get_rect()
           messagerect.center = (center[0],Y // 2 + 52)
           display.blit(timetraveled,messagerect)
           
           messagerect = endmessage3.get_rect()
           messagerect.center = (center[0],Y - 70)
           display.blit(endmessage3,messagerect)
           
           messagerect = endmessage4.get_rect()
           messagerect.center = (center[0],Y - 35)
           display.blit(endmessage4,messagerect)
           
            
        pygame.display.flip()
        fpsClock.tick(FPS)