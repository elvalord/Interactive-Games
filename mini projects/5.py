# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos=[300,200]
ball_vel=[2.0,-2.0]
paddle1_pos=HEIGHT/2
paddle2_pos=HEIGHT/2
paddle1_vel=0
paddle2_vel=0
left_score=0
right_score=0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos=[300,200]
    if direction==RIGHT:
    #    ball_vel=[1,-1]
        ball_vel[0]=random.randrange(2,4)
        ball_vel[1]=-random.randrange(1,3)
    elif direction==LEFT:
    #    ball_vel=[-1,-1]
        ball_vel[0]=-random.randrange(2,4)
        ball_vel[1]=-random.randrange(1,3)

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global left_score,right_score
    left_score=0
    right_score=0
    spawn_ball(True)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, left_score,right_score
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[0]-BALL_RADIUS<=0+PAD_WIDTH:
        if ball_pos[1]<=paddle1_pos+HALF_PAD_HEIGHT and ball_pos[1]>=paddle1_pos-HALF_PAD_HEIGHT:
            ball_vel[0]=-ball_vel[0]
            ball_vel[0]=1.1*ball_vel[0]
            ball_vel[1]=1.1*ball_vel[1]
        else:
            right_score+=1
            spawn_ball(RIGHT)
    elif ball_pos[0]+BALL_RADIUS>=WIDTH-1-PAD_WIDTH:
        if ball_pos[1]<=paddle2_pos+HALF_PAD_HEIGHT and ball_pos[1]>=paddle2_pos-HALF_PAD_HEIGHT:
            ball_vel[0]=-ball_vel[0]
            ball_vel[0]=1.1*ball_vel[0]
            ball_vel[1]=1.1*ball_vel[1]
        else:
            left_score+=1
            spawn_ball(LEFT)                
    elif ball_pos[1]-BALL_RADIUS<=0:
        ball_vel[1]=-ball_vel[1]
    elif ball_pos[1]+BALL_RADIUS>=HEIGHT-1:
        ball_vel[1]=-ball_vel[1]
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos+paddle1_vel<=HEIGHT-1-HALF_PAD_HEIGHT and paddle1_pos+paddle1_vel>=HALF_PAD_HEIGHT:
        paddle1_pos+=paddle1_vel
    if paddle2_pos+paddle2_vel<=HEIGHT-1-HALF_PAD_HEIGHT and paddle2_pos+paddle2_vel>=HALF_PAD_HEIGHT:    
        paddle2_pos+=paddle2_vel
    # draw paddles
    canvas.draw_line((HALF_PAD_WIDTH,paddle1_pos-HALF_PAD_HEIGHT), (HALF_PAD_WIDTH,paddle1_pos+HALF_PAD_HEIGHT), PAD_WIDTH, "White")
    canvas.draw_line((WIDTH-1-HALF_PAD_WIDTH,paddle2_pos-HALF_PAD_HEIGHT),(WIDTH-1-HALF_PAD_WIDTH,paddle2_pos+HALF_PAD_HEIGHT), PAD_WIDTH, "White")
    # draw scores
    canvas.draw_text(str(left_score), (150,100), 20, "Red")
    canvas.draw_text(str(right_score), (450,100), 20,"Red")    
def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 3
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = vel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel= vel
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel= -vel    
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel= 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel= 0    

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset",new_game)


# start frame
new_game()
frame.start()
