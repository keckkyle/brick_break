from tkinter import *
import random
import time

tk = Tk()

## set up window
tk.title("Bounce")
tk.resizable(0,0)
tk.wm_attributes("-topmost",1)
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
tk.update()


## set game object classes
class Life:
    def __init__(self, canvas):
        self.canvas = canvas
        self.lives = 0
        self.id = canvas.create_text(5,0,text="", fill="#A00", anchor=NW)

    def setLives(self, lives):
        self.lives = lives
        hearts = ""
        for i in range(0, lives):
            if i == 0:
                hearts = "♥︎"
            else: 
                hearts += " ♥︎"
        self.canvas.itemconfig(self.id, text=hearts)

    def getLives(self):
        return self.lives



class Ball:
    def __init__(self, canvas, color, paddle, life):
        self.canvas = canvas
        self.paddle = paddle
        self.life = life
        self.id = canvas.create_oval(10,10,20,20, fill=color, outline=color)
        self.canvas.move(self.id,250,450)
        self.x = 0
        self.y = 0
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.canvas.bind_all("<space>", self.startBall)
        self.life.setLives(5)
        self.bricks = []

        for row in range(0,random.randrange(25)+1):
            color = "#%03x" % random.randint(0,0xFFF)
            for col in range(0, 33):
                self.bricks.append(Brick(canvas, color, 2+(15*col), (15*row)+20))

    def startBall(self,evt):
        if self.y == 0 and self.life.getLives() > 0:
            self.x = 5
            self.y = -4
        
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
            return False

    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = -self.x
        if pos[1] <= 0:
            self.y = 4
        if pos[2] >= self.canvas_width:
            self.x = -self.x
        if pos[3] >= self.canvas_height:
            self.y = 0
            self.x = 0
            self.life.setLives(self.life.getLives()-1)
            if self.life.getLives() > 0:
                self.canvas.coords(self.id, 260,450,270,460)
            else:
                for brick in self.bricks:
                    self.canvas.delete(brick.id)
                canvas.create_text(250,250, text="Game Over", font=("Luminari",20))
        if self.hit_paddle(pos) == True:
            if self.x > 0:
                self.x += 0
            else:
                self.x -= 0
            self.y = -4
        for brick in self.bricks: 
            if brick.side_hit(pos) == True:
                self.x = -self.x
                self.bricks.remove(brick)  
            if brick.hit(pos) == True:
                self.y = -self.y
                if brick in self.bricks:
                    self.bricks.remove(brick)  



class Paddle:
    def __init__(self,canvas,color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0,100,10, fill=color, outline=color)
        self.canvas.move(self.id,0,480)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all("<KeyPress-Left>",self.turn_left)
        self.canvas.bind_all("<KeyPress-Right>",self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0 or pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self,evt):
        if self.canvas.coords(self.id)[0] > 0:
            self.x = -5
    
    def turn_right(self, evt):
        if self.canvas.coords(self.id)[2] < self.canvas_width:
            self.x = 5



class Brick:
    def __init__(self, canvas, color, hor, vert):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0,15,15, fill=color, outline="white")
        self.canvas.move(self.id, hor, vert)
        self.coords = canvas.coords(self.id)

    def side_hit(self, pos):
        if pos[1] <= self.coords[3] and pos[3] >= self.coords[1]:
            if pos[0] <= self.coords[2] and pos[0] >= self.coords[2]-3:
                self.canvas.delete(self.id)
                return True
            if pos[2] >= self.coords[0] and pos[2] <= self.coords[0]+3:
                self.canvas.delete(self.id)
                return True
        return False

    def hit(self, pos):
        if pos[2] >= self.coords[0] and pos[0] <= self.coords[2]:
            if pos[3] >= self.coords[1] and pos[3] <= self.coords[1]+3:
                self.canvas.delete(self.id)
                return True
            if pos[1] <= self.coords[3] and pos[1] >= self.coords[3]-3:
                self.canvas.delete(self.id)
                return True
        return False



class BrickGrid:
    def __init__(self, rows, columns, ball):
        self.ball = ball
        self.midpoint = canvas.winfo_width()/2
        self.start = 5+self.midpoint-(columns*25)/2
        self.bricks = []
        self.coords = []
        for row in range(0,rows):
            color = "#%03x" % random.randint(0,0xFFF)
            for col in range(0, columns):
                self.bricks.append(Brick(canvas, color, self.start+(25*col), (25*row)+20))
        for brick in self.bricks:
            self.coords.append(canvas.coords(brick.id))

    def draw(self):
        if self.ball.hit_paddle(canvas.coords(self.ball.id)) == True:
            print('hi')
        

                


## create objects
paddle = Paddle(canvas, "#AA8833")
life= Life(canvas)
ball = Ball(canvas, "#00AA88", paddle, life)
# bricks = BrickGrid(random.randrange(15)+1, random.randrange(20)+1, ball)

## loop to run game code
while 1:
    ball.draw()
    paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)