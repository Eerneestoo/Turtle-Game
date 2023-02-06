from turtle import Turtle, Screen
import random
import datetime
from datetime import timedelta

win = Screen()
win.colormode(255)
win.bgcolor(0, 0, 255)

screen_size = win.screensize()

players = []
characters = []

class Player:
    def __init__(self,color,position,players,characters,):
        self.bias = 7
        self.state = { "direction": "", "key_pressed": False }
        self.player = Turtle()
        self.player.shape("turtle")
        self.player.color(color[0],color[1],color[2])
        self.player.penup()
        self.player.setposition(position[0],position[1])
        

        players.append(self)
        characters.append(self)

    def pos(self):
        return self.player.pos()

    def forward(self,value):
        self.player.forward(value)

    def back(self,value):
        self.player.back(value)

    def right(self,value):
        self.player.right(value)

    def left(self,value):
        self.player.left(value)

    def resize(self,x,y,o):
        self.player.shapesize(x,y,o)

    def get_size(self):
        return self.player.shapesize()

    def set_keys(self,win,keys):
        keymap = [self.move_up, self.move_down, self.move_left, self.move_right]
        for i in range(4):
            win.onkeypress(keymap[i],keys[i])
            win.onkeyrelease(self.stop,keys[i])

    def move_up(self):
        self.state["direction"] = "up"
        self.state["key_pressed"] = True

    def move_down(self):
        self.state["direction"] = "down"
        self.state["key_pressed"] = True

    def move_left(self):
        self.state["direction"] = "left"
        self.state["key_pressed"] = True

    def move_right(self):
        self.state["direction"] = "right"
        self.state["key_pressed"] = True

    def stop(self):
        self.state["direction"] = ""
        self.state["key_pressed"] = False
            
        
        


def createFood(position):
    food = Turtle()
    food.shape("circle")
    food.setposition(position[0],position[1])

    characters.append(food)

p1 = Player((100,0,125),(0,0),players,characters)
p2 = Player((0,255,2),(30,0),players,characters)

p1.set_keys(win,["w","s","a","d"])
p2.set_keys(win,["i","k","j","l"])

createFood((0,0))

p1_key_state = { "direction": "", "key_pressed": False }
p2_key_state = { "direction": "", "key_pressed": False }
player_speed = 15
sensetivity = 15

previous_text = None

def speed1():
    global player_speed
    player_speed = 1
def speed2():
    global player_speed
    player_speed = 2
def speed3():
    global player_speed
    player_speed = 3
def speed4():
    global player_speed
    player_speed = 4
def speed5():
    global player_speed
    player_speed = 5
def speed6():
    global player_speed
    player_speed = 6
def speed7():
    global player_speed
    player_speed = 7
def speed8():
    global player_speed
    player_speed = 8
def speed9():
    global player_speed
    player_speed = 9
def speedr():
    global player_speed
    player_speed = 15
def speedmore():
    global player_speed
    player_speed = 30

win.onkey(speed1,"1")
win.onkey(speed2,"2")
win.onkey(speed3,"3")
win.onkey(speed4,"4")
win.onkey(speed5,"5")
win.onkey(speed6,"6")
win.onkey(speed7,"7")
win.onkey(speed8,"8")
win.onkey(speed9,"9")
win.onkey(speedr,"r")
win.onkey(speedmore,"m")

previous_time = datetime.datetime.now()
dt = 0

def process_events():
    for player in players:
        if player.state["direction"] == "up":
            player.forward(player_speed)
        if player.state["direction"] == "down":
            player.back(player_speed)
        if player.state["direction"] == "left":
            player.left(player_speed)
        if player.state["direction"] == "right":
            player.right(player_speed)
        
    p1_pos_x = players[0].pos()[0]
    p1_pos_y = players[0].pos()[1]
    p2_pos_x = players[1].pos()[0]
    p2_pos_y = players[1].pos()[1]
    food_pos_x = characters[2].pos()[0]
    food_pos_y = characters[2].pos()[1]

    if players[0].bias >= abs(p1_pos_x - food_pos_x) and players[0].bias >= abs(p1_pos_y - food_pos_y):
        current_size = players[0].get_size()
        players[0].resize(current_size[0]+1,current_size[1]+1,current_size[2])
        players[0].bias = players[0].bias + 20
        characters[2].setposition(random.randrange(-1*screen_size[0]*0.5,screen_size[0]*0.5),\
                          random.randrange(-1*screen_size[1]*0.5,screen_size[1]*0.5))   

    if players[1].bias >= abs(p2_pos_x - food_pos_x) and players[1].bias >= abs(p2_pos_y - food_pos_y):
        current_size = players[1].get_size()
        players[1].resize(current_size[0]+1,current_size[1]+1,current_size[2])
        players[1].bias = players[1].bias + 20
        characters[2].setposition(random.randrange(-1*screen_size[0]*0.5,screen_size[0]*0.5),\
                          random.randrange(-1*screen_size[1]*0.5,screen_size[1]*0.5)) 

    global previous_time
    global dt
    global previous_text

    current_time = datetime.datetime.now()
    delta = current_time - previous_time
    dt = dt + delta.total_seconds()*1000
    previous_time = current_time

    if dt > 2000:
        print(delta)
        dt = 0

        if previous_text != None:
            previous_text.clear()

    win.ontimer(process_events)
    
process_events()

win.listen()
win.mainloop()


