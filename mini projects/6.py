# implementation of card game - Memory

import simplegui
import random

deck=range(0,8)*2
random.shuffle(deck)
exposed=[False,False]*8
num_x=20
num_y=55
state = 0
pre=[]
turn=0


# helper function to initialize globals
def new_game():
    global state, turn, deck, exposed, pre
    exposed=[False,False]*8
    state = 0 
    turn=0
    label.set_text("Turns ="+str(turn))
    random.shuffle(deck)
    pre=[]
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, pre, turn
    if state == 0:
        exposed[pos[0]/50]=True
        pre.append(pos[0]/50)
        state = 1
    elif state == 1:
        if exposed[pos[0]/50]==False:
            exposed[pos[0]/50]=True
            pre.append(pos[0]/50)
            turn+=1
            label.set_text("Turns ="+str(turn))
            state = 2
    else:
        if exposed[pos[0]/50]==False:            
            a=pre.pop()
            b=pre.pop()
            if deck[a]!=deck[b]:
                exposed[a]=False
                exposed[b]=False
            exposed[pos[0]/50]=True
            pre.append(pos[0]/50)
            state = 1       
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global deck,num_x,num_y,exposed
    num_x=20
    i=0
    for num in deck:
        if exposed[i]==True:
            canvas.draw_text(str(num),(num_x,num_y),20,'White')
        else:
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 1, 'Black', 'Green')
        i+=1
        num_x+=50


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric