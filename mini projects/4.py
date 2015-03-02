# template for "Stopwatch: The Game"
import simplegui
# define global variables
tenth=0
x=0
y=0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    A=t/600
    B=(t-A*600)/100
    C=t%100/10
    D=t%10
    return str(A)+":"+str(B)+str(C)+"."+str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
def stop():    
    if timer.is_running():
        timer.stop()
        global y
        y+=1
        global x
        if tenth%10==0:
            x+=1
def reset():
    timer.stop()
    global tenth
    tenth=0
    global y
    y=0
    global x
    x=0
# define event handler for timer with 0.1 sec interval
def tick():
    global tenth
    tenth+=1

# define draw handler
def draw(canvas):
    global tenth
    canvas.draw_text(format(tenth), (100,100), 20, 'White')
    canvas.draw_text(str(x)+"/"+str(y), (250,50), 20, 'Green')
    
# create frame
f=simplegui.create_frame("Home",300,200)

# register event handlers
f.add_button("Start",start)
f.add_button("Stop",stop)
f.add_button("Reset",reset)
f.set_draw_handler(draw)
timer=simplegui.create_timer(100, tick)
# start frame
f.start()
timer.start

# Please remember to review the grading rubric
