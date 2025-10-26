from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

# Game state variables
bowl_coords = [100, 500, 2600, 500]     # (x0, y0, x1, y1)
gem_coords = [5100, 8000, 5400, 8400]    # (a0, b0, a1, b1)
bx0, by0, bx1, by1 = bowl_coords
gx0, gy0, gx1, gy1 = gem_coords

icon_pause = [0, 0, 0, 0]
icon_exit = [0, 0, 0, 0]
icon_resume = [0, 0, 0, 0]
icon_restart = [0, 0, 0, 0]

paused = False
points = 0
game_done = False
move_left = 0
move_right = 0
fall_speed = 100

color_palette = [
    (1.0, 0.0, 0.0),  # Red
    (0.0, 1.0, 0.0),  # Green
    (0.0, 0.0, 1.0),  # Blue
    (1.0, 1.0, 0.0),  # Yellow
    (1.0, 0.0, 1.0),  # Magenta
    (0.0, 1.0, 1.0),  # Cyan
    (1.0, 0.5, 0.0),  # Orange
    (1.0, 0.75, 0.8), # Pink
]
active_color = random.choice(color_palette)

def getZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) < abs(dy):
        if dx > 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6
    else:
        if dx > 0 and dy > 0:
            return 0
        elif dx < 0 and dy > 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7

def toZone0(zone, x, y):
    mapping = {
        0: (x, y), 1: (y, x), 2: (-y, x), 3: (-x, y),
        4: (-x, -y), 5: (-y, -x), 6: (-y, x), 7: (x, -y),
    }
    return mapping[zone]

def fromZone0(zone, x, y):
    mapping = {
        0: (x, y), 1: (y, x), 2: (y, -x), 3: (-x, y),
        4: (-x, -y), 5: (-y, -x), 6: (y, -x), 7: (x, -y),
    }
    return mapping[zone]

def plotPixel(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def drawLine(x1, y1, x2, y2):
    zone = getZone(x1, y1, x2, y2)
    x1, y1 = toZone0(zone, x1, y1)
    x2, y2 = toZone0(zone, x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    d = 2*dy - dx
    de = 2*dy
    dne = 2*(dy - dx)
    while x1 < x2:
        px, py = fromZone0(zone, x1, y1)
        plotPixel(px, py)
        if d >= 0:
            y1 += 1
            d += dne
        else:
            d += de
        x1 += 1

def drawBowl(x1, y1, x2, y2):
    global game_done, fall_speed, gy1, points
    if gy1 <= 0:
        glColor3f(1.0, 0.0, 0.0)
        if not game_done:
            game_done = True
            print(f"Game Over, Score: {points}")
            fall_speed = 35
    else:
        glColor3f(0.7, 0.7, 0.7)

    right = x2 - move_left + move_right
    left = x1 - move_left + move_right
    renderBox(left, y1, right, y2, 250, 350)

def renderBox(l, t, r, b, w, h):
    drawLine(l, t, r, t)
    drawLine(l + w, t - h, r - w, t - h)
    drawLine(l, t, l + w, t - h)
    drawLine(r - w, t - h, r, t)

def renderGem(ax1, ay1, ax2, ay2):
    global active_color
    glColor3f(*active_color)
    drawLine(ax1, ay1, ax2, ay2)
    drawLine(ax2, ay2, ax1 + 600, ay1)
    drawLine(ax1, ay1, ax2, ay2 - 800)
    drawLine(ax2, ay2 - 800, ax1 + 600, ay1)

def iconRestart():
    global icon_restart
    glColor3f(0.0, 1.0, 1.0)
    drawRestartSymbol()
    icon_restart = [1000, 1600, 9200, 9800]

def drawRestartSymbol():
    drawLine(1000, 9500, 1300, 9800)
    drawLine(1000, 9500, 1300, 9200)
    drawLine(1000, 9500, 1600, 9500)

def iconPause():
    global icon_pause
    glColor3f(1.0, 0.84, 0.0)
    drawPauseBars()
    icon_pause = [4750, 5250, 9200, 9800]

def drawPauseBars():
    drawLine(4850, 9800, 4850, 9200)
    drawLine(5150, 9800, 5150, 9200)

def iconResume():
    global icon_resume
    glColor3f(1.0, 0.84, 0.0)
    drawResumeSymbol()
    icon_resume = [4750, 5250, 9200, 9800]

def drawResumeSymbol():
    drawLine(4750, 9800, 4750, 9200)
    drawLine(4750, 9200, 5250, 9500)
    drawLine(4750, 9800, 5250, 9500)

def iconExit():
    global icon_exit
    glColor3f(1.0, 0.0, 0.0)
    drawExitX()
    icon_exit = [9000, 9600, 9200, 9800]

def drawExitX():
    drawLine(9000, 9800, 9600, 9200)
    drawLine(9000, 9200, 9600, 9800)

def togglePause():
    global paused
    paused = not paused

def handleSpecialKeys(key, x, y):
    global move_left, move_right, bx0, bx1
    step = 500
    if not paused and not game_done:
        
        if key == GLUT_KEY_LEFT and (bx0 - move_left + move_right) > 0:
            move_left += step
        elif key == GLUT_KEY_RIGHT and (bx1 - move_left + move_right) < 10000:
            move_right += step
    
   
    if bx0 - move_left + move_right < 0:
        move_left = bx0  
    if bx1 - move_left + move_right > 10000:
        move_right = 10000 - bx1  

    glutPostRedisplay()


def handleMouse(button, state, mx, my):
    global icon_exit, icon_pause, icon_resume, icon_restart
    global bx0, by0, bx1, by1, gx0, gy0, gx1, gy1
    global game_done, points, fall_speed, paused, active_color

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        my = 500 - my
        mx *= 20
        my *= 20

        if (icon_restart[0] <= mx <= icon_restart[1] and 
            icon_restart[2] <= my <= icon_restart[3]):
            print("Starting Over! Previous Score:", points)
            bx0, by0, bx1, by1 = 100, 500, 2600, 500
            gx0, gy0, gx1, gy1 = 5100, 8000, 5400, 8400
            points = 0
            fall_speed = 100
            game_done = False
            paused = False
            active_color = random.choice(color_palette)
            glutPostRedisplay()

        elif (icon_pause[0] <= mx <= icon_pause[1] and 
              icon_pause[2] <= my <= icon_pause[3]):
            togglePause()
            glutPostRedisplay()

        elif (icon_exit[0] <= mx <= icon_exit[1] and 
              icon_exit[2] <= my <= icon_exit[3]):
            print(f"Goodbye! Your score was: {points}")
            glutLeaveMainLoop()

def setupView():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 10000, 0.0, 10000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def updateAnimation():
    global gy0, gy1, bx0, bx1, by0, by1, points, fall_speed, gx0, gx1, active_color, game_done
    if not paused and not game_done:
        gy0 -= fall_speed
        gy1 -= fall_speed

        bowl_l = bx0 - move_left + move_right
        bowl_r = bx1 - move_left + move_right
        bowl_t = by0
        bowl_b = by0 - 350

        if (gx1 > bowl_l and gx0 < bowl_r and gy0 < bowl_t and gy1 > bowl_b):
            gy0, gy1 = 8000, 8400
            points += 1
            fall_speed += 15
            print(f"Score: {points}")
            gx0 = random.randint(500, 9500)
            gx1 = gx0 + 300
            active_color = random.choice(color_palette)

        if gy1 <= 0 and not game_done:
            game_done = True
            print(f"Game Over! Final Score: {points}")
    glutPostRedisplay()

def drawScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setupView()
    glColor3f(0.0, 0.0, 0.0)
    iconRestart()
    iconExit()
    iconResume() if paused else iconPause()
    renderGem(gx0, gy0, gx1, gy1)
    drawBowl(bx0, by0, bx1, by1)
    glutSwapBuffers()

def startGame():
    glutInit()
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Catch the Diamonds!")
    glutDisplayFunc(drawScene)
    glutIdleFunc(updateAnimation)
    glutSpecialFunc(handleSpecialKeys)
    glutMouseFunc(handleMouse)
    glutMainLoop()

if __name__ == "__main__":
    startGame()
