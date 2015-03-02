# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import random
import simplegui

# initialize global variables used in your code
secret_num=0
user_guess=0
upperbound=100
guess_time=7

# helper function to start and restart the game
def new_game():
    # remove this when you add your code   
    global guess_time
    if upperbound==100:
        guess_time=7
    elif upperbound==1000:
        guess_time=10
    global secret_num
    secret_num=random.randrange(0,upperbound)
    print ""
    print "New game. Range is 0-"+str(upperbound)+"."
    print "Number of remaining guesses is "+str(guess_time)+"."

# define event handlers for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global upperbound
    upperbound=100     
    new_game()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global upperbound
    upperbound=1000    
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global guess_time
    guess_time-=1
    if guess_time==0:
        print ""
        print "Game over."
        new_game()
        return
    print ""
    print "Guess was "+guess+"."
    print "Number of remaining guesses is "+str(guess_time)+"."
    # remove this when you add your code
    if int(guess)>secret_num:
        print "Lower!"
    elif int(guess)<secret_num:
        print "Higher!"
    else:
        print "Correct!"

    
# create frame
frame=simplegui.create_frame("Home",300,200)

# register event handlers for control elements
frame.add_button("Range is [0,100)",range100)
frame.add_button("Range is [0,1000)",range1000)
frame.add_input("Enter a guess",input_guess,50)

# call new_game and start frame
frame.start()
new_game()

# always remember to check your completed program against the grading rubric
