from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math


bubble_list = []
bullet_list = []
shooter_x = 0 ; shooter_y = -273 ; shooter_r = 25
shooter_cl = [.7,.6,0]
create = 500 ; p_time = 0
score = 0 ; missed_shot = 0 ; missed_bubble = 0 ; speed = .02
game_over= False ; freeze = False


def draw_pixel(x,y,clr):
    glColor3d(clr[0],clr[1],clr[2])
    # glColor3d(1.0,1.0,0)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def find_zone(x1,y1,x2,y2):
    dx = x2-x1
    dy = y2-y1
    # print("dy", dy , "dx", dx)

    if abs(dx) >= abs(dy):
        # print("entered")
        # print("dy", dy , "dx", dx)
        if dx >= 0 and dy >= 0:
            return 0
        if dx >= 0 and dy <= 0:
            return 7
        if dx <= 0 and dy >= 0:
            return 3
        if dx <= 0 and dy <= 0:
            return 4
    if abs(dx) < abs(dy):
        if dx >= 0 and dy >= 0:
            return 1
        if dx >= 0 and dy <= 0:
            return 6
        if dx <= 0 and dy >= 0:
            return 2
        if dx <= 0 and dy <= 0:
            return 5
        
def conv_Z0(a,b,z):
    if z == 0:
        x = a ; y = b
    if z == 1:
        x = b ; y = a
    if z == 2:
        x = b ; y = -a
    if z == 3:
        x = -a ; y = b
    if z == 4:
        x = -a ; y = -b
    if z == 5:
        x = -b ; y = -a
    if z == 6:
        x = -b ; y = a
    if z == 7:
        x = a ; y = -b
    return (x,y)

def conv_realZ(a,b,z):
    if z == 0:
        x = a ; y = b
    if z == 1:
        x = b ; y = a
    if z == 2:
        x = -b ; y = a
    if z == 3:
        x = -a ; y = b
    if z == 4:
        x = -a ; y = -b
    if z == 5:
        x = -b ; y = -a
    if z == 6:
        x = b ; y = -a
    if z == 7:
        x = a ; y = -b

    return (x,y)

def mid_point_algo(x1,y1,x2,y2,clr):

    zone = find_zone(x1,y1,x2,y2)
    # print(zone)
    nx1,ny1 = conv_Z0(x1,y1,zone)
    nx2,ny2 = conv_Z0(x2,y2,zone)

    dx = nx2-nx1
    dy = ny2-ny1

    d = 2*dy - dx
    dE = 2*dy
    dNE = 2*dy - 2*dx

    x = nx1 
    y = ny1

    while (x <= nx2):

        x_ , y_ = conv_realZ(x,y,zone)
        draw_pixel(x_,y_,clr)

        if d > 0:
            y +=1
            d += dNE

        else:
            d+= dE

        x+=1 


class circle:
    def __init__(self,x,y,r,cl):

        self.x = x
        self.y = y
        self.r = r
        self.clr = cl


def use_octant(x,y,cx,cy,clr):

    draw_pixel(x + cx, y + cy,clr)
    draw_pixel(y + cx, x + cy,clr)
    draw_pixel(y + cx, -x + cy,clr)
    draw_pixel(x + cx, -y + cy,clr)
    draw_pixel(-x + cx, -y + cy,clr)
    draw_pixel(-y + cx, -x + cy,clr)
    draw_pixel(-y + cx, x + cy,clr)
    draw_pixel(-x + cx, y + cy,clr)


def mid_point_circ_algo(cx,cy,r,clr):

    d = 1 - r
    x = 0 ; y = r

    while (x <= y):

        use_octant(x,y,cx,cy,clr)
        
        if d < 0:
            d = d + 2*x + 3
            x += 1
        else:
            d = d + 2*x -2*y + 5
            x += 1
            y -= 1


def bubble_falling():

    global bubble_list, missed_bubble,speed

    if missed_bubble >= 3:
        GameOver()

    for i in bubble_list:
        i.y -= speed
        if i.y + i.r <= -300:
            bubble_list.remove(i)
            missed_bubble += 1
            create_new_bubble()
            print(f"{missed_bubble} bubble missed")


def shot_bullet():

    global bullet_list,bubble_list,score, missed_shot,speed

    for i in bullet_list:

        i.y += 15
        if i.y + i.r >= 300:

            bullet_list.remove(i)
            missed_shot += 1
            print(f"You missed the shot! only {3-missed_shot} lives remaining")
            if missed_shot == 3:
                GameOver()
                return
        else:
            for j in bubble_list:

                target = i.r + j.r
                dist = math.sqrt((i.x - j.x) ** 2 + (i.y - j.y) ** 2)

                if dist <= target :
                    score += 1
                    speed += 0.005
                    bullet_list.remove(i)
                    bubble_list.remove(j)
                    create_new_bubble()
                    print(f"Score {score}")

def check_overlap(obj):

    global bubble_list

    for i in bubble_list:
        target = i.r + obj.r
        dist = math.sqrt((i.x - obj.x) ** 2 + (i.y - obj.y) ** 2)
        if dist <= target :
            return True
    return False      

def create_new_bubble():

    global bubble_list, game_over , freeze , create , p_time

    c_time = glutGet(GLUT_ELAPSED_TIME)
    if len(bubble_list) < 6 and game_over == False and freeze == False and (c_time - p_time) > create:
        r = random.randrange(15,50)
        x = random.randrange(-400+r,400-r)
        y = 300-(r+30)
        new_bubble = circle(x,y,r,[1.0,1.0,0.0])
        if check_overlap(new_bubble) == False:
            bubble_list.append(new_bubble)
            p_time = c_time
        else:
            create_new_bubble()
            



def draw_bubble():

    global bubble_list,shooter_x,shooter_y,shooter_r

    for i in bubble_list:
        target = i.r + shooter_r
        dist = math.sqrt((i.x - shooter_x) ** 2 + (i.y - shooter_y) ** 2)
        if dist <= target:
            GameOver()
            break
        mid_point_circ_algo(i.x,i.y,i.r,i.clr)

def draw_bullet():

    global bullet_list

    for i in bullet_list:

        mid_point_circ_algo(i.x,i.y,i.r,i.clr)


def GameOver():

    global game_over,bubble_list,bullet_list

    game_over = True
    print(f"Game_over! Final Score {score}")
    bubble_list = []
    bullet_list = []

def start_newGame():

    global bubble_list,bullet_list,shooter_x,shooter_y,shooter_r,shooter_cl,score,missed_shot,missed_bubble,game_over

    bubble_list = []
    bullet_list = []
    shooter_x = 0 ; shooter_y = -275 ; shooter_r = 25
    shooter_cl = [.7,.6,0]
    score = 0 ; missed_shot = 0 ; missed_bubble = 0 
    game_over= False ; freeze = False ; speed = 0.02
    p_time = 0




def keyboardListener(key, x, y):

    global shooter_x,shooter_y,shooter_r,bullet_list,freeze,game_over

    if game_over == False and freeze == False:
        if key == b'a':
            var = shooter_x - shooter_r
            if var - 15 >= -400:
                shooter_x -= 15

        if key == b'd':
            var = shooter_x+shooter_r
            if var + 15 <= 400:
                shooter_x += 15

        if key == b' ':

            shot = circle(shooter_x,shooter_y,5,[1,0,0])
            bullet_list.append(shot)


def mouseListener(button, state, x, y):

    # print(x,y)
    global freeze, score
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 0 <= x <= 45 and 0 <= y <= 30 :
            print("Starting Over")
            start_newGame()

        if 385 <= x <= 415 and 0 <= y <= 30 :
            if freeze == False:
                freeze = True
            elif freeze == True:
                freeze = False
                
        if 770 <= x <= 800 and 0 <= y <= 30 :
                print(f"Goodbye! Score: {score}")
                glutLeaveMainLoop()
    glutPostRedisplay()




def iterate():
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-400, 400, -300, 300, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    global shooter_x,shooter_y,shooter_r,shooter_cl
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    #draw shooter
    mid_point_circ_algo(shooter_x,shooter_y,shooter_r,shooter_cl)

    create_new_bubble()
    draw_bubble()
    draw_bullet()

    # reset button

    co1 = [0.0,0.67,0.65] 
    mid_point_algo(-395,285,-378,296, co1)
    mid_point_algo(-395,285,-378, 275, co1)
    mid_point_algo(-395,285,-360,285, co1)

    # cancel button

    co2 = [1.0,0.0,0.0]
    mid_point_algo(375,295,395,278, co2)
    mid_point_algo(375,278,395,295, co2)

    # play pause button
    co3 = [1.0,0.4,0.0]
    
    if freeze == False:

        mid_point_algo(-15,295,-15,275, co3)
        mid_point_algo(15,295,15,275, co3)
    
    elif freeze == True:

        mid_point_algo(-10,295,-10,275, co3)
        mid_point_algo(-10,295,10,285, co3)
        mid_point_algo(-10,275,10,285, co3)

    glutSwapBuffers()

def animate():

    global game_over, freeze

    if game_over == False and freeze == False:

        bubble_falling()
        shot_bullet()

    glutPostRedisplay()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(800, 600) #window size
glutInitWindowPosition(500,20)
wind = glutCreateWindow(b"Mansura Task1 Assignment3") #window name
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)

glutMainLoop()

    