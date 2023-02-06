from turtle import Turtle, Screen
import random
import datetime
from datetime import timedelta

class GameState:
    def __init__(self):
        self.gameover = False
        self.game_timer = 0
        self.refresh_text_timer = 0
        self.previous_time = datetime.datetime.now()
        self.text = Turtle()
        self.text.penup()
        self.text.setposition((0,350))
        self.text.write(arg="{}".format(120 - int(self.game_timer/1000)),font=("Arial", 64, "normal"))
        self.players = []
        self.characters = []
        self.player_speed = 15
        self.screen_size = None
        
    def update(self):
        current_time = datetime.datetime.now()
        delta = current_time - self.previous_time
        self.refresh_text_timer = self.refresh_text_timer + delta.total_seconds()*1000
        self.game_timer = self.game_timer + delta.total_seconds()*1000
        self.previous_time = current_time
        
        if self.refresh_text_timer > 1000:
            self.refresh_text_timer = 0
            if not self.gameover:
                self.text.clear()
                self.text.write(arg="{}".format(120 - int(self.game_timer/1000)),font=("Arial", 64, "normal"))
        
        if self.game_timer > 120000:
            self.game_timer = 0
            self.text.clear()
        
            winner = "player 2"
        
            if self.players[0].bias > self.players[1].bias:
                winner = "player 1"
            elif self.players[0].bias == self.players[1].bias:
                winner = "nobody"
        
            self.text.write(arg="The winner is {}".format(winner),font=("Arial", 64, "normal"))
            
            self.gameover = True
            
    def update_players_position(self):
        for player in self.players:
            if player.state["direction"] == "up":
                player.forward(self.player_speed)
            if player.state["direction"] == "down":
                player.back(self.player_speed)
            if player.state["direction"] == "left":
                player.left(self.player_speed)
            if player.state["direction"] == "right":
                player.right(self.player_speed)

    def update_collisions(self):
        p1_pos_x = self.players[0].pos()[0]
        p1_pos_y = self.players[0].pos()[1]
        p2_pos_x = self.players[1].pos()[0]
        p2_pos_y = self.players[1].pos()[1]
        food_pos_x = self.characters[2].pos()[0]
        food_pos_y = self.characters[2].pos()[1]
        
        if self.players[0].bias >= abs(p1_pos_x - food_pos_x) and self.players[0].bias >= abs(p1_pos_y - food_pos_y):
            current_size = self.players[0].get_size()
            self.players[0].resize(current_size[0]+1,current_size[1]+1,current_size[2])
            self.players[0].bias = self.players[0].bias + 5
            self.characters[2].setposition(random.randrange(-1*self.screen_size[0]*0.5,self.screen_size[0]*0.5),\
                            random.randrange(-1*self.screen_size[1]*0.5,self.screen_size[1]*0.5))   

        if self.players[1].bias >= abs(p2_pos_x - food_pos_x) and self.players[1].bias >= abs(p2_pos_y - food_pos_y):
            current_size = self.players[1].get_size()
            self.players[1].resize(current_size[0]+1,current_size[1]+1,current_size[2])
            self.players[1].bias = self.players[1].bias + 5
            self.characters[2].setposition(random.randrange(-1*self.screen_size[0]*0.5,self.screen_size[0]*0.5),\
                            random.randrange(-1*self.screen_size[1]*0.5,self.screen_size[1]*0.5)) 

        

class Player:
    def __init__(self,color,position):
        self.bias = 7
        self.state = { "direction": "", "key_pressed": False }
        self.player = Turtle()
        self.player.shape("turtle")
        self.player.color(color[0],color[1],color[2])
        self.player.penup()
        self.player.setposition(position[0],position[1])
        self.eaten = 0
                
    def reset(self):
        self.eaten = 0
        self.bias = 7

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
            
class TurtleGame:
    def __init__(self):
        self.win = Screen()
        self.win.colormode(255)
        self.win.bgcolor(0, 0, 255)
        
        self.screen_size = self.win.screensize()
                
        self.state = GameState()
        self.state.screen_size = self.screen_size

        p1 = Player((100,0,125),(0,0))
        p2 = Player((0,255,2),(30,0))

        self.state.players.append(p1)
        self.state.players.append(p2)
        self.state.characters.append(p1)
        self.state.characters.append(p2)

        p1.set_keys(self.win,["w","s","a","d"])
        p2.set_keys(self.win,["i","k","j","l"])

        food = Turtle()
        food.shape("circle")
        food.setposition((0,200))
        self.state.characters.append(food)

    def process_events(self):
        self.state.update()
        self.state.update_players_position()
        self.state.update_collisions()
            
        self.win.ontimer(self.process_events,16)
    
    def run(self):
        self.process_events()
        
        self.win.listen()
        self.win.mainloop()

turtle_game = TurtleGame()
turtle_game.run()

