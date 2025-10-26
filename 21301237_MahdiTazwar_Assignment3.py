from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Window settings
WIN_WIDTH = 1000
WIN_HEIGHT = 800

# Game settings
GRID_DIM = 600
CELL_DIM = 100
CHAR_RADIUS = 40
CHAR_HEIGHT = 100
NUM_ENEMIES = 5

# Camera settings
fovY_angle = 120
view_mode = 0  
view_angle = 0
view_height = 500
view_radius = 800

# Player state
char_x = 0
char_y = 0
char_orientation = 0
char_life_points = 5
projectiles = []

# Enemies
bad_guys = []

# Cheat mode
cheat_enabled = False
cheat_vision_enabled = False

missed_shots = 0
player_score = 0
is_game_over = False

class Projectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.z = 50
        self.angle = angle
        self.velocity = 10

    def move(self):
        self.x += self.velocity * math.cos(math.radians(self.angle))
        self.y += self.velocity * math.sin(math.radians(self.angle))

class Villain:
    def __init__(self):
        self.reset()

    def reset(self):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(300, 500)
        self.x = radius * math.cos(angle)
        self.y = radius * math.sin(angle)
        self.scale_factor = 1.0
        self.direction = 1

    def approach_player(self):
        dx = char_x - self.x
        dy = char_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 1:
            self.x += 1.5 * dx / distance
            self.y += 1.5 * dy / distance

        self.scale_factor += 0.07 * self.direction
        if self.scale_factor > 1.2 or self.scale_factor < 0.8:
            self.direction *= -1

def render_text(x, y, text):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_WIDTH, 0, WIN_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def render_checkered_floor():
    for x in range(-GRID_DIM, GRID_DIM, CELL_DIM):
        for y in range(-GRID_DIM, GRID_DIM, CELL_DIM):
            if ((x + y) // CELL_DIM) % 2 == 0:
                glColor3f(0.5, 0.5, 0.5)
            else:
                glColor3f(0.5, 0.2, 0.6)
            glBegin(GL_QUADS)
            glVertex3f(x, y, 0)
            glVertex3f(x + CELL_DIM, y, 0)
            glVertex3f(x + CELL_DIM, y + CELL_DIM, 0)
            glVertex3f(x, y + CELL_DIM, 0)
            glEnd()

def render_wall():
    glColor3f(1, 1, 0)
    height = 40
    for x in [-GRID_DIM, GRID_DIM]:
        for y in range(-GRID_DIM, GRID_DIM):
            glPushMatrix()
            glTranslatef(x, y, height / 2)
            glutSolidCube(20)
            glPopMatrix()
    for y in [-GRID_DIM, GRID_DIM]:
        for x in range(-GRID_DIM, GRID_DIM):
            glPushMatrix()
            glTranslatef(x, y, height / 2)
            glutSolidCube(20)
            glPopMatrix()

def render_player():
    glPushMatrix()
    glTranslatef(char_x, char_y, 0)

    if is_game_over:
        glRotatef(90, 1, 0, 0)

    glRotatef(char_orientation, 0, 0, 1)

    # BODY
    glColor3f(1, 1, 0)  # Yellow
    glPushMatrix()
    glTranslatef(0, 0, CHAR_HEIGHT / 2)
    gluCylinder(gluNewQuadric(), CHAR_RADIUS, CHAR_RADIUS, CHAR_HEIGHT, 10, 10)
    glPopMatrix()

    # Legs
    leg_radius = CHAR_RADIUS / 2
    leg_height = CHAR_HEIGHT / 2
    leg_offset_x = CHAR_RADIUS / 2
    leg_offset_y = CHAR_RADIUS / 2
    glColor3f(0.3, 0.3, 1)

    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * leg_offset_x, -leg_offset_y, leg_height / 2)
        gluCylinder(gluNewQuadric(), leg_radius, leg_radius, leg_height, 10, 10)
        glPopMatrix()

    # Arms
    arm_radius = CHAR_RADIUS / 4
    arm_length = CHAR_RADIUS * 1.5
    arm_height = CHAR_HEIGHT * 0.8
    glColor3f(1, 0.5, 0)

    for side in [-1, 1]:
        glPushMatrix()
        glTranslatef(side * (CHAR_RADIUS + arm_radius), 0, arm_height)
        glRotatef(90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), arm_radius, arm_radius, arm_length, 10, 10)
        glPopMatrix()

    # GUN
    gun_radius = 5
    gun_length = 60
    glColor3f(0.2, 0.2, 0.2)

    glPushMatrix()
    glTranslatef(0, CHAR_RADIUS + 10, arm_height)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), gun_radius, gun_radius, gun_length, 10, 10)
    glPopMatrix()

    glPopMatrix()

def render_villains():
    for villain in bad_guys:
        glPushMatrix()
        glTranslatef(villain.x, villain.y, 0)
        glScalef(villain.scale_factor, villain.scale_factor, villain.scale_factor)
        glPushMatrix()
        glColor3f(1, 0, 1)
        glTranslatef(0, 0, 40)
        gluSphere(gluNewQuadric(), 20, 10, 10)
        glColor3f(0, 1, 0)
        glTranslatef(0, 0, -40)
        gluSphere(gluNewQuadric(), 30, 10, 10)
        glPopMatrix()
        glPopMatrix()

def render_projectiles():
    glColor3f(0, 1, 0)
    for projectile in projectiles:
        glPushMatrix()
        glTranslatef(projectile.x, projectile.y, projectile.z)
        glScalef(1, 1, 0.3)
        glutSolidCube(20)
        glPopMatrix()

def setup_camera_view():
    global view_angle, view_height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY_angle, WIN_WIDTH / WIN_HEIGHT, 1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if view_mode == 0:
        eye_x = view_radius * math.cos(math.radians(view_angle))
        eye_y = view_radius * math.sin(math.radians(view_angle))
        eye_z = view_height
        gluLookAt(eye_x, eye_y, eye_z, 0, 0, 0, 0, 0, 1)
    else:
        if cheat_enabled and cheat_vision_enabled:
            eye_x = char_x + (CHAR_RADIUS + 10) * math.cos(math.radians(char_orientation))
            eye_y = char_y + (CHAR_RADIUS + 10) * math.sin(math.radians(char_orientation))
            eye_z = CHAR_HEIGHT * 0.8 
            gluLookAt(eye_x, eye_y, eye_z,
                    char_x + 100 * math.cos(math.radians(char_orientation)),
                    char_y + 100 * math.sin(math.radians(char_orientation)),
                    eye_z, 0, 0, 1)
        else:
            eye_x = char_x - 100 * math.cos(math.radians(char_orientation))
            eye_y = char_y - 100 * math.sin(math.radians(char_orientation))
            eye_z = 200
            gluLookAt(eye_x, eye_y, eye_z, 
                     char_x, char_y, 0, 0, 0, 1)

def update_game_state():
    global projectiles, bad_guys, player_score, missed_shots, char_life_points, is_game_over, char_orientation

    if is_game_over:
        glutPostRedisplay()
        return

    # Track projectiles that hit nothing and go out of bounds
    projectiles_to_remove = []
    
    for projectile in projectiles:
        projectile.move()
        
        # Check if projectile is out of bounds (only count as miss in non-cheat mode)
        if abs(projectile.x) >= GRID_DIM or abs(projectile.y) >= GRID_DIM:
            projectiles_to_remove.append(projectile)
            if not cheat_enabled:  # Only count misses in normal mode
                missed_shots += 1

    # Remove out-of-bounds projectiles
    for p in projectiles_to_remove:
        if p in projectiles:
            projectiles.remove(p)

    for villain in bad_guys:
        villain.approach_player()

        # Bullet collision
        for projectile in projectiles[:]:
            if math.hypot(villain.x - projectile.x, villain.y - projectile.y) < 40:
                if projectile in projectiles:
                    projectiles.remove(projectile)
                villain.reset()
                player_score += 1
                break

      
        if not cheat_enabled and math.hypot(villain.x - char_x, villain.y - char_y) < 40:
            char_life_points -= 1
            villain.reset()

    if cheat_enabled and not is_game_over:
        char_orientation += 2  
        
       
        target_villains = []
        for villain in bad_guys:
            dx = villain.x - char_x
            dy = villain.y - char_y
            dist = math.hypot(dx, dy)
            angle_to_villain = math.degrees(math.atan2(dy, dx))
            angle_diff = abs((char_orientation - angle_to_villain + 180) % 360 - 180)
            
            if dist < 600 and angle_diff < 20:
                target_villains.append(villain)
        
        
        if target_villains and glutGet(GLUT_ELAPSED_TIME) % 6== 0:  
            for villain in target_villains[:1]:  # Only process first target each frame
                # Calculate exact angle needed to hit this villain
                hit_angle = math.degrees(math.atan2(villain.y - char_y, villain.x - char_x))
                
                projectiles.append(Projectile(char_x, char_y, hit_angle))

    # Game over check
    if char_life_points <= 0 or (not cheat_enabled and missed_shots >= 10):
        is_game_over = True

    glutPostRedisplay()


def display_game():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, WIN_WIDTH, WIN_HEIGHT)

    setup_camera_view()

    render_checkered_floor()
    render_wall()
    
    
    if view_mode == 0 or not (cheat_enabled and cheat_vision_enabled):
        render_player()
    
    render_villains()
    render_projectiles()

    render_text(10, 770, f"Score: {player_score}  Life: {char_life_points}  Missed: {missed_shots}")
    if is_game_over:
        render_text(WIN_WIDTH // 2 - 100, WIN_HEIGHT // 2, "GAME OVER - Press R to Restart")

    glutSwapBuffers()

def keyboard_input(key, x, y):
    global char_x, char_y, char_orientation
    global cheat_enabled, cheat_vision_enabled, char_life_points, projectiles, missed_shots, player_score, bad_guys, is_game_over

    if is_game_over:
        if key == b'r':
            char_life_points = 5
            projectiles = []
            missed_shots = 0
            player_score = 0
            is_game_over = False
            for villain in bad_guys:
                villain.reset()
        return

    if key == b'w':
        new_x = char_x + 10 * math.cos(math.radians(char_orientation))
        new_y = char_y + 10 * math.sin(math.radians(char_orientation))
        if abs(new_x) < GRID_DIM and abs(new_y) < GRID_DIM:
            char_x, char_y = new_x, new_y
    elif key == b's':
        new_x = char_x - 10 * math.cos(math.radians(char_orientation))
        new_y = char_y - 10 * math.sin(math.radians(char_orientation))
        if abs(new_x) < GRID_DIM and abs(new_y) < GRID_DIM:
            char_x, char_y = new_x, new_y
    elif key == b'a':
        char_orientation += 10
    elif key == b'd':
        char_orientation -= 10
    elif key == b'c':
        cheat_enabled = not cheat_enabled
    elif key == b'v':
        cheat_vision_enabled = not cheat_vision_enabled

def special_keys(key, x, y):
    global view_angle, view_height
    if key == GLUT_KEY_LEFT:
        view_angle -= 5
    elif key == GLUT_KEY_RIGHT:
        view_angle += 5
    elif key == GLUT_KEY_UP:
        view_height += 10
    elif key == GLUT_KEY_DOWN:
        view_height -= 10

def mouse_input(button, state, x, y):
    global view_mode
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not is_game_over:
        projectiles.append(Projectile(char_x, char_y, char_orientation))
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        view_mode = 1 - view_mode

def main():
    global bad_guys
    glutInit()
    glutInitWindowSize(WIN_WIDTH, WIN_HEIGHT)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow(b"Bullet Frenzy")
    glEnable(GL_DEPTH_TEST)
    
    bad_guys = [Villain() for _ in range(NUM_ENEMIES)]
    
    glutDisplayFunc(display_game)
    glutKeyboardFunc(keyboard_input)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse_input)
    glutIdleFunc(update_game_state)
    glutMainLoop()

if __name__ == "__main__":
    main()