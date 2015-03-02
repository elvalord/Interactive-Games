# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
SHIP_SIZE=[90, 90]
SHIP_CENTER=[SHIP_SIZE[0]/2, SHIP_SIZE[1]/2] 
SHIP_AVEL_D=0.1
ship_angle_vel=0


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
ship_info_1 = ImageInfo([45+SHIP_SIZE[0], 45], [90, 90], 35)
ship_image_1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def angle_vel_inc():
    global ship_angle_vel
    if rotate_ori=="left":
        ship_angle_vel-=SHIP_AVEL_D
    elif rotate_ori=="right":
        ship_angle_vel+=SHIP_AVEL_D
timer_r = simplegui.create_timer(500, angle_vel_inc)

# Ship class
class Ship:
    
    def __init__(self, pos, vel, angle, image, info):
        global ship_angle_vel
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = ship_angle_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_center_1 = (self.image_center[0] + 90, self.image_center[1])
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust==True:
            center=self.image_center_1
        else:
            center=self.image_center
        canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        if self.vel[0]!=0:
            self.vel[0]*=0.99
        if self.vel[1]!=0:
            self.vel[1]*=0.99            
        #update position of the ship
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        #wrap the screen
        self.pos[0]=self.pos[0]%WIDTH
        self.pos[1]=self.pos[1]%HEIGHT
        #update the angle of the ship
        self.angle+=ship_angle_vel
        #update the orientation of the ship
        forward_vec=angle_to_vector(self.angle)
        if self.thrust==True:           
            self.vel=[self.vel[0]+0.1*forward_vec[0], self.vel[1]+0.1*forward_vec[1]]
       
    def modify_angle_vel(self, key):
        global rotate_ori, ship_angle_vel
        if key == simplegui.KEY_MAP["left"]:
            ship_angle_vel-=SHIP_AVEL_D 
#            rotate_ori="left"
#            timer_r.start()            
        elif key == simplegui.KEY_MAP["right"]:
            ship_angle_vel+=SHIP_AVEL_D
#            rotate_ori="right"
#            timer_r.start()                
            
    def stop_rotate(self, key):
        global ship_angle_vel 
#        timer_r.stop()
        ship_angle_vel=0
        
    def thrust_change(self, flag):
        if flag==1:
            self.thrust=True
            ship_thrust_sound.play()
        else:
            self.thrust=False
            ship_thrust_sound.rewind()

    def shoot(self):
        global a_missile
        forward_vec=angle_to_vector(self.angle)
        pos=[self.pos[0]+self.radius*forward_vec[0], self.pos[1]+self.radius*forward_vec[1]]
        vel=[self.vel[0]+5*forward_vec[0], self.vel[1]+5*forward_vec[1]]
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        self.pos[0]=self.pos[0]%WIDTH
        self.pos[1]=self.pos[1]%HEIGHT
        self.angle+=self.angle_vel
           
def draw(canvas):
    global time, score, lives
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # draw score and lives remaining
    canvas.draw_text("Score: "+ str(score), [650, 50], 30, "White", "sans-serif")
    canvas.draw_text("Lives: "+ str(lives), [50, 50], 30, "White",  "monospace")
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    vel=[0.8,0.8]
    # random position
    pos=[random.random()*WIDTH, random.random()*HEIGHT]
    # random velocity
    if random.random()>=0.5:
        vel[0]=-vel[0]
#        vel[0]=1.2*random.random()
#    else:
#        vel[0]=-1.2*random.random()
    if random.random()>=0.5:
        vel[1]=-vel[1]
#        vel[1]=1.2*random.random()
#    else:
#        vel[1]=-1.2*random.random()
    # random angle_vel
    angle_vel=0.05*random.random()
    a_rock = Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info)

def keydown(key):
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        my_ship.modify_angle_vel(key)
#    elif key == simplegui.KEY_MAP["down"]:
#        paddle2_vel= vel
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_change(1)  
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        my_ship.stop_rotate(key)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_change(0) 


    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)


# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], -1.57, ship_image, ship_info)
a_rock = Sprite([WIDTH / 4, HEIGHT / 4], [1, -1], 0, 0.1, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000.0, rock_spawner)


# get things rolling
timer.start()
frame.start()
