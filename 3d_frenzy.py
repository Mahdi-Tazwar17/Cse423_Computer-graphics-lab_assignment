from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Window settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# Game settings
GRID_SIZE = 600
CELL_SIZE = 100
PLAYER_RADIUS = 40
PLAYER_HEIGHT = 100
ENEMY_COUNT = 5

# Camera settings
fovY = 120
camera_mode = 0  #0=third person,1==first person
camera_angle = 0
camera_height = 500
camera_radius = 800

#Player state
player_x = 0
player_y = 0
player_angle = 0
player_life = 5
bullets = []

# Enemies
enemies = []

# Cheat mode
cheat_mode = False
cheat_vision = False


missed_bullets = 0
score = 0
game_over = False

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.z = 50
        self.angle = angle
        self.speed = 10

    def move(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))


class Enemy:
    def __init__(self):
        self.reset()

    def reset(self):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(300, 500)
        self.x = r * math.cos(angle)
        self.y = r * math.sin(angle)
        self.scale = 1.0
        self.direction = 1

    def move_towards_player(self):
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist > 1:
            self.x += 1.5 * dx / dist
            self.y += 1.5 * dy / dist

        self.scale += 0.07 * self.direction
        if self.scale > 1.2 or self.scale < 0.8:
            self.direction *= -1


def draw_text(x, y, text):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_checkered_floor():
    for x in range(-GRID_SIZE, GRID_SIZE, CELL_SIZE):
        for y in range(-GRID_SIZE, GRID_SIZE, CELL_SIZE):
            if ((x + y) // CELL_SIZE) % 2 == 0:
                glColor3f(0.5, 0.5, 0.5)
            else:
                glColor3f(0.5, 0.2, 0.6)
            glBegin(GL_QUADS)
            glVertex3f(x, y, 0)
            glVertex3f(x + CELL_SIZE, y, 0)
            glVertex3f(x + CELL_SIZE, y + CELL_SIZE, 0)
            glVertex3f(x, y + CELL_SIZE, 0)
            glEnd()


def draw_wall():
    glColor3f(1, 1, 0)
    height = 40
    for x in [-GRID_SIZE, GRID_SIZE ]:
        for y in range(-GRID_SIZE, GRID_SIZE):
            glPushMatrix()
            glTranslatef(x, y, height / 2)
            glutSolidCube(20)
            glPopMatrix()
    for y in [-GRID_SIZE, GRID_SIZE ]:
        for x in range(-GRID_SIZE, GRID_SIZE):
            glPushMatrix()
            glTranslatef(x, y, height / 2)
            glutSolidCube(20 ) 
            glPopMatrix()



def draw_player():
    glPushMatrix()
    glTranslatef(player_x, player_y, 0)

    if game_over:
        glRotatef(90, 1, 0, 0) 

    glRotatef(player_angle, 0, 0, 1)


    # BODY
    glColor3f(1, 1, 0)  # Yellow
    glPushMatrix()
    glTranslatef(0, 0, PLAYER_HEIGHT / 2)
    gluCylinder(gluNewQuadric(), PLAYER_RADIUS, PLAYER_RADIUS, PLAYER_HEIGHT, 10, 10)
    glPopMatrix()

    #leg????
    leg_radius = PLAYER_RADIUS / 2
    leg_height = PLAYER_HEIGHT / 2
    leg_offset_x = PLAYER_RADIUS / 2
    leg_offset_y = PLAYER_RADIUS / 2
    glColor3f(0.3, 0.3, 1) 

    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * leg_offset_x, -leg_offset_y, leg_height / 2)
        gluCylinder(gluNewQuadric(), leg_radius, leg_radius, leg_height, 10, 10)
        glPopMatrix()

    # hand
    arm_radius = PLAYER_RADIUS / 4
    arm_length = PLAYER_RADIUS * 1.5
    arm_height = PLAYER_HEIGHT * 0.8
    glColor3f(1, 0.5, 0) 

    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * (PLAYER_RADIUS + arm_radius), 0, arm_height)
        glRotatef(90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), arm_radius, arm_radius, arm_length, 10, 10)
        glPopMatrix()

    # GUN 
    gun_radius = 5
    gun_length = 60
    glColor3f(0.2, 0.2, 0.2) 

    glPushMatrix()
    glTranslatef(0, PLAYER_RADIUS + 10, arm_height)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), gun_radius, gun_radius, gun_length, 10, 10)
    glPopMatrix()

    glPopMatrix()



def draw_enemies():
    for enemy in enemies:
        glPushMatrix()
        glTranslatef(enemy.x, enemy.y, 0)
        glScalef(enemy.scale, enemy.scale, enemy.scale)
        #glColor3f(1, 0, 1)
        glPushMatrix()
        glColor3f(1, 0, 1)
        glTranslatef(0, 0, 40)
        gluSphere(gluNewQuadric(), 20, 10, 10)
        glColor3f(0, 1, 0)
        glTranslatef(0, 0, -40)
        gluSphere(gluNewQuadric(), 30, 10, 10)
        glPopMatrix()
        glPopMatrix()


def draw_bullets():
    glColor3f(0, 1, 0)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet.x, bullet.y, bullet.z)
        glScalef(1, 1, 0.3)
        glutSolidCube(20)
        glPopMatrix()


def setup_camera():
    global camera_angle, camera_height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, WINDOW_WIDTH / WINDOW_HEIGHT, 1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera_mode == 0:
        eye_x = camera_radius * math.cos(math.radians(camera_angle))
        eye_y = camera_radius * math.sin(math.radians(camera_angle))
        eye_z = camera_height
        gluLookAt(eye_x, eye_y, eye_z, 0, 0, 0, 0, 0, 1)
    else:
        if cheat_mode and cheat_vision:
            eye_x = player_x  * math.cos(math.radians(player_angle))
            eye_y = player_y * math.sin(math.radians(player_angle))
            eye_z = PLAYER_HEIGHT
        else:
            eye_x = player_x - 100 * math.cos(math.radians(player_angle))
            eye_y = player_y - 100 * math.sin(math.radians(player_angle))
            eye_z = 200
        gluLookAt(eye_x, eye_y, eye_z, player_x, player_y, 0, 0, 0, 1)


def update():
    global bullets, enemies, score, missed_bullets, player_life, game_over, player_angle


    if game_over:
        glutPostRedisplay()
        return

    for bullet in bullets:
        bullet.move()

    for enemy in enemies:
        enemy.move_towards_player()

        #Bullet collision
        for bullet in bullets:
            if math.hypot(enemy.x - bullet.x, enemy.y - bullet.y) < 40:
                bullets.remove(bullet)
                enemy.reset()
                score += 1
                break

        #Enemy touching player
        if math.hypot(enemy.x -player_x, enemy.y-player_y) < 40:
            player_life -= 1
            enemy.reset()

    # Cheat Mode
    if cheat_mode and not game_over:
        for enemy in enemies:
            dx = enemy.x - player_x
            dy = enemy.y - player_y
            dist = math.hypot(dx, dy)
            angle_to_enemy = math.degrees(math.atan2(dy, dx))

           #wrange
            if dist < 600:
                if abs((player_angle - angle_to_enemy + 180) % 360 - 180) < 10:
                    bullets.append(Bullet(player_x, player_y, player_angle))

       
    #global player_angle
        player_angle += 2

    #out of bounds bullets remove
    bullets = [b for b in bullets if abs(b.x) < GRID_SIZE and abs(b.y) < GRID_SIZE]

    # Missed bullet counter
    for bullet in bullets[:]:
        if abs(bullet.x) >= GRID_SIZE or abs(bullet.y) >= GRID_SIZE:
            bullets.remove(bullet)
            missed_bullets += 1

    # Game over
    if player_life <= 0 or missed_bullets >= 10:
        game_over = True

    glutPostRedisplay()



def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    setup_camera()

    draw_checkered_floor()
    draw_wall()
    draw_player()
    draw_enemies()
    draw_bullets()

    draw_text(10, 770, f"Score: {score}  Life: {player_life}  Missed: {missed_bullets}")
    if game_over:
        draw_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, "GAME OVER - Press R to Restart")

  

    glutSwapBuffers()


def keyboard(key, x, y):
    global player_x, player_y, player_angle
    global cheat_mode, cheat_vision, player_life, bullets, missed_bullets, score, enemies, game_over

    if game_over:
        if key == b'r':
            player_life = 5
            bullets = []
            missed_bullets = 0
            score = 0
            game_over = False
            for e in enemies:
                e.reset()
        return

    if key == b'w':
        player_x += 10 * math.cos(math.radians(player_angle))
        player_y += 10 * math.sin(math.radians(player_angle))
    elif key == b's':
        player_x -= 10 * math.cos(math.radians(player_angle))
        player_y -= 10 * math.sin(math.radians(player_angle))
    elif key == b'a':
        player_angle += 10
    elif key == b'd':
        player_angle -= 10
    elif key == b'c':
        cheat_mode = not cheat_mode #?????????
    elif key == b'v':
        cheat_vision = not cheat_vision #cheat vision not working


def special(key, x, y):
    global camera_angle, camera_height
    if key == GLUT_KEY_LEFT:
        camera_angle -= 5
    elif key == GLUT_KEY_RIGHT:
        camera_angle += 5
    elif key == GLUT_KEY_UP:
        camera_height += 10
    elif key == GLUT_KEY_DOWN:
        camera_height -= 10


def mouse(button, state, x, y):
    global camera_mode
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        bullets.append(Bullet(player_x, player_y, player_angle))
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = 1 - camera_mode


def main():
    global enemies
    enemies = [Enemy() for _ in range(ENEMY_COUNT)]
    glutInit()
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow(b"Bullet Frenzy")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special)
    glutMouseFunc(mouse)
    glutIdleFunc(update)
    glutMainLoop()


if __name__ == "__main__":
    main()

