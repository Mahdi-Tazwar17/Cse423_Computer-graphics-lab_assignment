# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random


# droplet_collection = []
# sky_color = [0.0, 0.0, 0.0]  
# rain_shift = 0  

# def render_pixel(x, y):
#     glPointSize(5)  
#     glBegin(GL_POINTS)
#     glVertex2f(x, y) 
#     glEnd()


# def configure_view():
#     glViewport(0, 0, 700, 600)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0, 700, 0.0, 600, 0.0, 1.0)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()

# def display_scene():
#     global sky_color
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     configure_view()
#     r, g, b = sky_color
#     glClearColor(r, g, b, 1.0) 
#     draw_objects()
#     render_rain()
#     glutSwapBuffers()

# def draw_objects():
#     glBegin(GL_TRIANGLES)
#     glColor3f(0.0, 1.0, 0.0)
#     glVertex2f(100, 300)
#     glVertex2f(300, 450)
#     glVertex2f(500, 300)
#     glEnd()

#     glColor3f(0.0, 1.0, 0.0)
#     glLineWidth(5)
#     glBegin(GL_LINES)
#     glVertex2d(150, 300)
#     glVertex2d(150, 100)
#     glVertex2d(450, 300)
#     glVertex2d(450, 100)
#     glVertex2d(150, 100)
#     glVertex2d(450, 100)

#     glVertex2d(190, 100)
#     glVertex2d(190, 250)

#     glVertex2d(260, 100)
#     glVertex2d(260, 250)

#     glVertex2d(190, 250)
#     glVertex2d(260, 250)

#     glVertex2d(320, 270)
#     glVertex2d(400, 270)

#     glVertex2d(320, 210)
#     glVertex2d(400, 210)

#     glVertex2d(320, 270)
#     glVertex2d(320, 210)

#     glVertex2d(400, 270)
#     glVertex2d(400, 210)

#     glVertex2d(360, 270)
#     glVertex2d(360, 210)

#     glVertex2d(320, 240)
#     glVertex2d(400, 240)
#     glEnd()

#     glColor3f(0.0, 1.0, 0.0)
#     render_pixel(245, 175)


# def generate_rain():
#     droplet_count = 200  
#     for i in range(droplet_count):
#         x_pos = random.randint(0, 700)  
#         y_pos = random.randint(400, 600) 
#         droplet_collection.append([x_pos, y_pos])

# def move_rain():
#     global rain_shift
#     new_droplets = 10  
#     for droplet in droplet_collection:
#         x_pos, y_pos = droplet
#         if y_pos <= 18:
#             droplet_collection.remove(droplet)  
#         else:
#             droplet[1] -= random.randint(2, 4)
#     for i in range(new_droplets):
#         x_pos = random.randint(0, 700)
#         y_pos = random.randint(500, 600)
#         droplet_collection.append([x_pos, y_pos]) 

# def render_rain():
#     glColor3f(0.0, 0.0, 1.0)  
#     for droplet in droplet_collection:
#         x_pos, y_pos = droplet
#         render_droplet(x_pos, x_pos + rain_shift, y_pos, y_pos - 18)

# def render_droplet(x1, x2, y1, y2):
#     glLineWidth(1)
#     glBegin(GL_LINES)
#     glVertex2d(x1, y1)
#     glVertex2d(x2, y2)
#     glEnd()

# def key_event_listener(key, x, y):
#     global rain_shift
#     if key == b'n':  
#         switch_to_night()
#     elif key == b'd':  
#         switch_to_day()
#     elif key == GLUT_KEY_LEFT:  
#         rain_shift -= 1  
#     elif key == GLUT_KEY_RIGHT: 
#         rain_shift += 1  
#     glutPostRedisplay()

# def switch_to_day():
#     global sky_color
#     if sky_color[0] < 1.0:  
#         sky_color[0] += 0.1
#     if sky_color[1] < 1.0:  
#         sky_color[1] += 0.1
#     if sky_color[2] < 1.0: 
#         sky_color[2] += 0.1

# def switch_to_night():
#     global sky_color
#     if sky_color[0] > 0.0:  
#         sky_color[0] -= 0.1
#     if sky_color[1] > 0.0:  
#         sky_color[1] -= 0.1
#     if sky_color[2] > 0.0: 
#         sky_color[2] -= 0.1

# def animation():
#     move_rain()  
#     glutPostRedisplay()  

# glutInit()
# glutInitDisplayMode(GLUT_RGBA)
# glutInitWindowSize(700, 600) 
# glutInitWindowPosition(0, 0)
# window = glutCreateWindow(b"House in rain")  

# generate_rain()
# glutDisplayFunc(display_scene)
# glutIdleFunc(animation)
# glutSpecialFunc(key_event_listener)  
# glutKeyboardFunc(key_event_listener)  

# glutMainLoop()




# --------------------------Task2----------------------------




from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Initialize global variables
dot_list = [] 
directions = [(-1, 1), (-1, -1), (1, 1), (1, -1)]  
pace = 1
halt = False 
flicker = False 
flicker_time = 400 
is_flickering = False 
flicker_phase = 0  
flicker_flag = 0


def plot_dot(x, y, r, g, b):
    glPointSize(10)
    glColor3f(r, g, b)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def setup_view():
    glViewport(0, 0, 700, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 700, 0.0, 600, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_view()
    draw_dots()
    glutSwapBuffers()


def draw_dots():
    for dot in dot_list:
        x, y, dx, dy, r, g, b, orig_r, orig_g, orig_b = dot
        plot_dot(x, y, r, g, b)


def shift_dots():
    global dot_list, pace

    for i, dot in enumerate(dot_list):
        x, y, dx, dy, r, g, b, orig_r, orig_g, orig_b = dot

        if not halt:
            x += dx * pace
            y += dy * pace

            if x <= 0 or x >= 700:
                dx = -dx
            if y <= 0 or y >= 600:
                dy = -dy

            dot_list[i] = [x, y, dx, dy, r, g, b, orig_r, orig_g, orig_b]


def flicker_handler(value):
    global dot_list, is_flickering, flicker_phase

    if is_flickering and not halt:
        if flicker_phase == 0:
            for i, dot in enumerate(dot_list):
                dot_list[i][4], dot_list[i][5], dot_list[i][6] = 0.0, 0.0, 0.0
            flicker_phase = 1
        else:
            for i, dot in enumerate(dot_list):
                orig_r, orig_g, orig_b = dot[7], dot[8], dot[9]
                dot_list[i][4], dot_list[i][5], dot_list[i][6] = orig_r, orig_g, orig_b
            flicker_phase = 0

        glutTimerFunc(flicker_time, flicker_handler, 0)
    
    glutPostRedisplay()


def mouse_input(button, state, x, y):
    global dot_list, flicker, is_flickering, flicker_phase

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not halt:
        y = 600 - y
        move_dir = random.choice(directions)
        dx, dy = move_dir
        r, g, b = random.random(), random.random(), random.random()
        dot_list.append([x, y, dx, dy, r, g, b, r, g, b])

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if not is_flickering:
            is_flickering = True
            flicker_phase = 0
            print("Flicker started")
            glutTimerFunc(0, flicker_handler, 0)
        else:
            is_flickering = False
            for i, dot in enumerate(dot_list):
                orig_r, orig_g, orig_b = dot[7], dot[8], dot[9]
                dot_list[i][4], dot_list[i][5], dot_list[i][6] = orig_r, orig_g, orig_b
            print("Flicker stopped and colors restored")

    glutPostRedisplay()


def key_input(key, x, y):
    global pace, halt, flicker_flag, is_flickering

    if key == b' ':
        if not halt:
            halt = True
            for i, dot in enumerate(dot_list):
                orig_r, orig_g, orig_b = dot[7], dot[8], dot[9]
                dot_list[i][4], dot_list[i][5], dot_list[i][6] = orig_r, orig_g, orig_b
            if is_flickering:
                flicker_flag = 1
                is_flickering = False
        else:
            halt = False
            if flicker_flag == 1:
                is_flickering = True
                flicker_flag = 0
                glutTimerFunc(0, flicker_handler, 0)

    elif key == GLUT_KEY_UP:
        pace += 0.1
        for i, dot in enumerate(dot_list):
            dx, dy = dot[2], dot[3]
            dx *= pace
            dy *= pace
            dot_list[i][2], dot_list[i][3] = dx, dy

    elif key == GLUT_KEY_DOWN:
        pace -= 0.1
        for i, dot in enumerate(dot_list):
            dx, dy = dot[2], dot[3]
            dx *= pace
            dy *= pace
            dot_list[i][2], dot_list[i][3] = dx, dy

    glutPostRedisplay()


def run_animation():
    if not halt:
        shift_dots()
    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(700, 600)
glutInitWindowPosition(0, 0)
window = glutCreateWindow(b"Flickering Dots")

glClearColor(0.0, 0.0, 0.0, 1.0)
glEnable(GL_DEPTH_TEST)

glutDisplayFunc(render)
glutMouseFunc(mouse_input)
glutKeyboardFunc(key_input)
glutSpecialFunc(key_input)
glutIdleFunc(run_animation)

glutMainLoop()
