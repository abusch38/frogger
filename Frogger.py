#in Anaconda, use Tkinter, otherwise tkinter
from tkinter import *
import time
import random


###################################

class Frog(object):
    global lily_pad_array
    
    def __init__(self, canvas, color, score, car, log):
        self.canvas = canvas
        self.color = color
        self.score = score
        self.car = car
        self.log = log
        #width of the frog
        self.rectWidth = 20
        
        #initializes the speed
        self.x = 0
        self.y = 0

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

        #setting the initial conditions.
        self.hit_object = False
        self.frog_on_log = False
        self.log_speed = 0
        self.started = False
        self.condition = True
        self.win = False
        self.initial_position = []

        #used by frog.cheat() to check end of game functions
        self.cheat_count = 0

        #binds the movement of the frog to the arrows.
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Up>', self.turn_up)
        self.canvas.bind_all('<KeyPress-Down>', self.turn_down)
        self.canvas.bind_all('<KeyPress-C>', self.cheat)

        #the game will start once the left-mouse button is pushed.
        self.canvas.bind_all('<Button-1>', self.start_game)

        #calls the create_frog function to create the initial frog 
        self.create_frog()

        #arrays for the coordinates of the cars in rows 1 through 5
        self.car_row_1_coord = []
        self.car_row_2_coord = []
        self.car_row_3_coord = []
        self.car_row_4_coord = []
        self.car_row_5_coord = []
        self.get_car_coordinates()

        #arrays for the coordinates of the logs in rows 1 through 5
        self.car_log_1_coord = []
        self.car_log_2_coord = []
        self.car_log_3_coord = []
        self.car_log_4_coord = []
        self.car_log_5_coord = []
        self.get_log_coordinates()

        #has the frog hit the lily pads?
        self.lily_pad_pos_array = [] 
        self.hit_lily_pad_array = [False, False, False, False, False]
        self.unwrap_lily_pad_array()
        
    #function starts the game
    def start_game(self, evt):
        self.started = True

    #creates the initial frog on the canvas
    def create_frog(self):
        #we will eventually want this to be a jpg file
        self.id = canvas.create_rectangle(0,0,self.rectWidth,
                            self.rectWidth, fill = self.color)

        #move frog to this location.
        self.canvas.move(self.id, self.canvas_width/2 - 10, self.canvas_height-1.5*self.rectWidth)
        self.initial_position = self.canvas.coords(self.id)

    # draw the frog in the window/canvas
    def draw(self):
        current_pos = self.canvas.coords(self.id)
        move_frog = False

        #To get the animation of the frog, the frog.draw() checks the current position
        #to the new position defined by the turn_...() functions.

        self.canvas.move(self.id, 1.5*self.rectWidth*self.x, 1.5*self.rectWidth*self.y)
        self.canvas.move(self.id, self.log_speed, 0)

        #returns all speeds back to zero.
        self.x = 0
        self.y = 0
        self.log_speed = 0

        
    #left and right functions
    def turn_left(self, evt):
        self.x = -1
        self.y = 0
            
    def turn_right(self, evt):
        self.x = 1
        self.y = 0
            
    def turn_up(self, evt):
        self.x = 0
        self.y = -1
            
    def turn_down(self, evt):
        self.x = 0
        self.y = 1

                
    #check to see if the frog goes off the edge of the canvas
    def check_hit_object(self):
        position = self.canvas.coords(self.id)
        
        x1 = position[0]
        y1 = position[1]
        x2 = position[2]
        y2 = position[3]
        
        #check the hit functions depending on where the frog is on the screen
        self.check_hit_edge(x1, y1, x2, y2)

        #Check to see if the from hits a car
        if y1>= self.car_row_5_coord[1]:
            self.log_speed = 0
            self.check_hit_car(x1, y1, x2, y2)

        #check to see if the frog hits the water
        if y2<= self.car_row_5_coord[3] and y1 >= self.log_row_5_coord[1]:
            self.check_hit_water(x1, y1, x2, y2)

        #check to see if the frog lands on a lily pad
        if y2 <= self.log_row_5_coord[1]:
            self.log_speed = 0
            self.check_hit_lily_pad(x1, y1, x2, y2)

        #lose a life if the frog dies
        if self.hit_object == True:
            self.score.lose_life()
           
    def check_hit_edge (self, x1, y1, x2, y2):
        if x1 < 0 or x2 > self.canvas_width:
            self.hit_object = True
            
        if y1 <0 or y2 > self.canvas_height:
            self.hit_object = True

    #Get the coordinates of the rows for the cars and pull them into the frog object
    def get_car_coordinates (self):
        self.car_row_1_coord = self.canvas.coords(self.car.car_row_1[1])
        self.car_row_2_coord = self.canvas.coords(self.car.car_row_2[1])
        self.car_row_3_coord = self.canvas.coords(self.car.car_row_3[1])
        self.car_row_4_coord = self.canvas.coords(self.car.car_row_4[1])
        self.car_row_5_coord = self.canvas.coords(self.car.car_row_5[1])
        #print(self.car_row_5_coord)
     
    #check to see if the frog hits a car
    def check_hit_car(self, x1, y1, x2, y2):
        #check the y-values for row 1
        if y1>= self.car_row_1_coord[1] and y2 <= self.car_row_1_coord[3]:
            #check the x-values
            self.check_hit_row(x1, y1, x2, y2, 1)
            
        #check the y-values for row 2
        if y1>= self.car_row_2_coord[1] and y2 <= self.car_row_2_coord[3]:
            #check the x-values
            self.check_hit_row(x1, y1, x2, y2, 2)
            
        #check the y-values for row 3
        if y1>= self.car_row_3_coord[1] and y2 <= self.car_row_3_coord[3]:
            #check the x-values
            self.check_hit_row(x1, y1, x2, y2, 3)
            
        #check the y-values for row 4
        if y1>= self.car_row_4_coord[1] and y2 <= self.car_row_4_coord[3]:
            #check the x-values
            self.check_hit_row(x1, y1, x2, y2, 4)
            
        #check the y-values for row 5
        if y1>= self.car_row_5_coord[1] and y2 <= self.car_row_5_coord[3]:
            #check the x-values
            self.check_hit_row(x1, y1, x2, y2, 5)
            
    #used by the check_hit_car function to cut down on repeated code
    def check_hit_row (self, x1, y1, x2, y2, row_num):
        if row_num == 1: 
            row_array = self.car.car_row_1
        elif row_num == 2:
            row_array = self.car.car_row_2
        elif row_num == 3:
            row_array = self.car.car_row_3
        elif row_num == 4:
            row_array = self.car.car_row_4
        elif row_num == 5:
            row_array = self.car.car_row_5
            
        for i in range(len(row_array)):
            self.car.id = row_array[i]
            car_pos = self.canvas.coords(self.car.id)
            
            if x1 <= car_pos[2] and x2 >= car_pos[0]:
                print("you hit a car!")
                self.hit_object = True
                
    #pull log coordinates into the frog object. 
    def get_log_coordinates (self):
        self.log_row_1_coord = self.canvas.coords(self.log.log_row_1[1])
        print("Log Row 1: ", self.log_row_1_coord)
        self.log_row_2_coord = self.canvas.coords(self.log.log_row_2[1])
        print("Log Row 2: ", self.log_row_2_coord)
        self.log_row_3_coord = self.canvas.coords(self.log.log_row_3[1])
        print("Log Row 3: ", self.log_row_3_coord)
        self.log_row_4_coord = self.canvas.coords(self.log.log_row_4[1])
        print("Log Row 4: ", self.log_row_4_coord)
        self.log_row_5_coord = self.canvas.coords(self.log.log_row_5[1])
        print("Log Row 5: ", self.log_row_5_coord)

    #check to see if the frog hits the water
    def check_hit_water(self, x1, y1, x2, y2):
        #check the y-values for row 1
        if y1>= self.log_row_1_coord[1] and y2 <= self.log_row_1_coord[3]:
            #print("checking row 1")
            #check the x-values
            self.check_hit_water_row(x1, y1, x2, y2, 1)
            
        #check the y-values for row 2
        if y1>= self.log_row_2_coord[1] and y2 <= self.log_row_2_coord[3]:
            #check the x-values
            #print("checking row 2")
            self.check_hit_water_row(x1, y1, x2, y2, 2)
                        
        #check the y-values for row 3
        if y1>= self.log_row_3_coord[1] and y2 <= self.log_row_3_coord[3]:
            #check the x-values
            #print("checking row 3")
            self.check_hit_water_row(x1, y1, x2, y2, 3)
                        
        #check the y-values for row 4
        if y1>= self.log_row_4_coord[1] and y2 <= self.log_row_4_coord[3]:
            #check the x-values
            #print("checking row 4")
            self.check_hit_water_row(x1, y1, x2, y2, 4)
            
        #check the y-values for row 5
        if y1>= self.log_row_5_coord[1] and y2 <= self.log_row_5_coord[3]:
            #print("checking row 5")
            self.check_hit_water_row(x1, y1, x2, y2, 5)
            
        
    #used by the check_hit_water function to cut down on repeated code.
    def check_hit_water_row(self, x1, y1, x2, y2, row_num):
        self.frog_on_log = False
        
        if row_num == 1: 
            row_array = self.log.log_row_1

        elif row_num == 2:
            row_array = self.log.log_row_2
        elif row_num == 3:
            row_array = self.log.log_row_3
        elif row_num == 4:
            row_array = self.log.log_row_4
        elif row_num == 5:
            row_array = self.log.log_row_5

        #cycle through all logs in row to see if the frog is on any of them.
        for i in range(len(row_array)):
            self.log.id = row_array[i]
            log_pos = self.canvas.coords(self.log.id)

            #check to see if the frog is on a log.
            if x1 <= log_pos[2] and x2 >= log_pos[0]:
                self.frog_on_log = True
                
                if row_num ==1:
                    self.log_speed =  3
                elif row_num == 2:
                    self.log_speed = -2
                elif row_num == 3:
                    self.log_speed = 5
                elif row_num == 4:
                    self.log_speed = -2.5
                elif row_num == 5:
                    self.log_speed = 4
                    
        #If the frog is not on a log, it dies.
        if self.frog_on_log == False:
            print("you fell in the water!")
            self.hit_object = True 

    #pull information in from the lily pad set up. 
    def unwrap_lily_pad_array(self):
        global lily_pad_array

        for i in range(len(lily_pad_array)):
            self.lily_pad_id = lily_pad_array[i]
            #print(self.lily_pad_id)
            lily_pad_pos = self.canvas.coords(self.lily_pad_id)
            #print(lily_pad_pos)
            self.lily_pad_pos_array.append(lily_pad_pos)

    def check_hit_lily_pad(self, x1, y1, x2, y2):
        global lily_pad_array
        #check to see if the frog makes it into the top spots.
        print("Checking the lily pad function")
        #check to see if the the frog makes it between the x-values.
        
        for i in range(len(self.lily_pad_pos_array)):
            lily_pad_pos = self.lily_pad_pos_array[i]
            #print(lily_pad_pos)
            #print("self.hit_lily_pad_array[i]: ", self.hit_lily_pad_array[i])
            #check to see if the frog is on a lilypad.
            if x1 <= lily_pad_pos[2] and x2 >= lily_pad_pos[0]:
                #has the frog already been on that lilypad?
                if self.hit_lily_pad_array[i] == True:
                    print("You've already jumped on this lily pad!")
                    self.hit_object = True
                    #print("Inside the 'True': ", self.hit_lily_pad_array[i])
                elif self.hit_lily_pad_array[i] == False:
                    #print("Inside the 'False': ", self.hit_lily_pad_array[i])
                    print("The frog is on lily pad: ", [i])
                    self.hit_lily_pad_array[i] = True
                    #print(lily_pad_array[i])
                    self.canvas.itemconfig(lily_pad_array[i], fill="green")
                    self.move_frog_back()
                    self.score.increase()

                #Controls the values of the self.cheat()
                self.cheat_count +=1

        #check to see if all 5 lily pads have been landed on
        self.check_win()

    def move_frog_back(self):
        frog_position = self.canvas.coords(self.id)
        self.canvas.move(self.id, -frog_position[0], -frog_position[1])
        self.canvas.move(self.id, self.initial_position[0], self.initial_position[1])
        
    #once the frog has filled in all the lily pads, the game is won                      
    def check_win(self):
        lily_pad_count = 0
        for i in range(len(self.hit_lily_pad_array)):
            if self.hit_lily_pad_array[i] == True:
                lily_pad_count +=1
                print("lily pad count: ", lily_pad_count)
            elif self.hit_lily_pad_array[i] == False:
                pass

        if lily_pad_count == 5:
            self.win == True
            print("You win!!!")

    #Pressing Shift+C will move the frog directly to the lily pad
    #Use this function to test end-of-game functions.
    def cheat(self, evt):
        global lily_pad_array
        print("Running the cheat function")
        i = self.cheat_count
        frog_position = self.canvas.coords(self.id)
        lily_pad_pos = self.lily_pad_pos_array[i]
        self.canvas.move(self.id, -frog_position[0], -frog_position[1])
        self.canvas.move(self.id, lily_pad_pos[0]+2, lily_pad_pos[1]+2)



###################################### 
class Car(object):
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.color = ""
        self.car_type = ""
        self.row = 1
        self.column = 1

        #setting up the car arrays
        #this one is for animation
        self.car_object_wrapper = []
        
        #these are for checking to see if the frog gets hit
        self.car_row_1 = []
        self.car_row_2 = []
        self.car_row_3 = []
        self.car_row_4 = []
        self.car_row_5 = []
        
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        
        #width of car
        self.rectWidth = 20
        self.carLength = 2*self.rectWidth

        #the x-value and y-value placement of the car
        self.col_placement = self.rectWidth
        self.row_placement = self.rectWidth
        
        #initializes the speed
        self.x = 4
        self.set_up_cars(canvas)

    def set_up_cars(self, canvas):
        #self.set_up_cars_row(canvas, color, row #, car type, x speed)
        self.set_up_cars_row(canvas, "purple", 1, "car", 5)
        self.set_up_cars_row(canvas, "blue", 2, "truck", -4)
        self.set_up_cars_row(canvas, "red", 3, "car", 3, )
        self.set_up_cars_row(canvas, "yellow", 4, "truck", -5)
        self.set_up_cars_row(canvas, "orange", 5, "car", 6)

    def set_up_cars_row(self, canvas, color, row, car_type, x_speed):
        self.color = color
        self.row = row
        self.car_type = car_type
        self.x = x_speed

        for i in range(1, 6):
            self.choose_col(i)
            self.create_car()
        
    def choose_car_type(self):
        if self.car_type == "car":
            self.carLength = 2*self.rectWidth
        if self.car_type == "truck":
            self.carLength = 3*self.rectWidth

    def choose_row(self):
        #choosing the y-value placement
        self.row_placement = self.canvas_height-self.row*1.5*self.rectWidth-(1.5*self.rectWidth)

    def choose_col(self, column):
        self.column = column
        #choosing the x-value placement
        self.col_placement = -self.carLength + (self.column-1)*self.canvas_width/5
    
    #creates the initial car on the canvas
    def create_car(self):
        self.choose_car_type()
        self.choose_row()
        
        #we will eventually want this to be a jpg file
        self.id = canvas.create_rectangle(0,0,self.carLength,
                            self.rectWidth, fill = self.color)

        #move car to this location:
        self.canvas.move(self.id, self.col_placement, self.row_placement)
        self.car_object_wrapper.append([self.id, self.row, self.x])

        #add the newly created cars to their respective lists for the check_hit functions
        if self.row == 1:
            self.car_row_1.append(self.id)
        elif self.row == 2:
            self.car_row_2.append(self.id)
        elif self.row == 3:
            self.car_row_3.append(self.id)
        elif self.row == 4:
            self.car_row_4.append(self.id)
        elif self.row == 5:
            self.car_row_5.append(self.id)

    #animate the car in the window/canvas
    def draw(self):
        for i in range(0, len(self.car_object_wrapper)):
            car_id = self.car_object_wrapper[i][0]
            row_id= self.car_object_wrapper[i][1]
            speed_id = self.car_object_wrapper[i][2]
            self.canvas.move(car_id, speed_id, 0)
            self.reset_car(car_id, row_id, speed_id)

    #move the car back to the beginning
    def reset_car(self, car_id, row_id, speed_id):
        self.id = car_id
        self.row = row_id
        self.x = speed_id
        position = self.canvas.coords(self.id)
        if self.x > 0:
            if position[0] > self.canvas_width:
                self.canvas.move(self.id, -self.canvas_width-20, 0)
        if self.x < 0:
            if position[2] < 0:
                self.canvas.move(self.id, self.canvas_width+20, 0)


######################################
class Log(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.color = ""
        self.log_type = ""
        self.row = 1
        self.column = 1

        #setting up the log arrays
        #this one is for animation
        self.log_object_wrapper = []
        
        #these are for checking to see if the frog gets hit
        self.log_row_1 = []
        self.log_row_2 = []
        self.log_row_3 = []
        self.log_row_4 = []
        self.log_row_5 = []
        
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        
        #width of log
        self.rectWidth = 20
        self.logLength = 2*self.rectWidth

        #the x-value and y-value placement of the log
        self.col_placement = self.rectWidth
        self.row_placement = self.rectWidth
        
        #initializes the speed
        self.x = 4
        self.set_up_logs(canvas)

    def set_up_logs(self, canvas):
        #self.set_up_logs_row(canvas, color, row #, log type, x speed)
        self.set_up_logs_row(canvas, "brown", 1, "log", 3)
        self.set_up_logs_row(canvas, "dark green", 2, "turtle", -2)
        self.set_up_logs_row(canvas, "brown", 3, "log", 5, )
        self.set_up_logs_row(canvas, "dark green", 4, "turtle", -2.5)
        self.set_up_logs_row(canvas, "brown", 5, "log", 4)

    def set_up_logs_row(self, canvas, color, row, log_type, x_speed):
        self.color = color
        self.row = row
        self.log_type = log_type
        self.x = x_speed

        for i in range(1, 6):
            self.choose_col(i)
            self.create_log()
        
    def choose_log_type(self):
        if self.log_type == "log":
            self.logLength = 3*self.rectWidth
        if self.log_type == "turtle":
            self.logLength = 2*self.rectWidth

    def choose_row(self):
        #choosing the y-value placement
        self.row_placement = self.canvas_height-self.row*1.5*self.rectWidth-(7*30)
        #canvas_height-(35+ 2*1.5*5*20+30+30)
    def choose_col(self, column):
        self.column = column
        #choosing the x-value placement
        self.col_placement = -self.logLength + (self.column-1)*self.canvas_width/5
    
    #creates the initial log on the canvas
    def create_log(self):
        self.choose_log_type()
        self.choose_row()
        
        #we will eventually want this to be a jpg file
        self.id = canvas.create_rectangle(0,0,self.logLength,
                            self.rectWidth, fill = self.color)

        #move log to this location:
        self.canvas.move(self.id, self.col_placement, self.row_placement)
        self.log_object_wrapper.append([self.id, self.row, self.x])

        #add the newly created logs to their respective lists for the check_hit functions
        if self.row == 1:
            self.log_row_1.append(self.id)
        elif self.row == 2:
            self.log_row_2.append(self.id)
        elif self.row == 3:
            self.log_row_3.append(self.id)
        elif self.row == 4:
            self.log_row_4.append(self.id)
        elif self.row == 5:
            self.log_row_5.append(self.id)

    #animate the log in the window/canvas
    def draw(self):
        for i in range(0, len(self.log_object_wrapper)):
            log_id = self.log_object_wrapper[i][0]
            row_id= self.log_object_wrapper[i][1]
            speed_id = self.log_object_wrapper[i][2]
            self.canvas.move(log_id, speed_id, 0)
            self.reset_log(log_id, row_id, speed_id)

    #move the log back to the beginning
    def reset_log(self, log_id, row_id, speed_id):
        self.id = log_id
        self.row = row_id
        self.x = speed_id
        position = self.canvas.coords(self.id)
        if self.x > 0:
            if position[0] > self.canvas_width:
                self.canvas.move(self.id, -self.canvas_width-50, 0)
        if self.x < 0:
            if position[2] < 0:
                self.canvas.move(self.id, self.canvas_width+40, 0)



######################################       
class Score(object):
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.color = color
        self.score = 0
        self.lives = 3
        self.lose = False
        self.canvas_width = self.canvas.winfo_width()
        self.id = canvas.create_text(self.canvas_width-60, 10, text = "Score: ", \
                                     fill = color)
        self.score_id = canvas.create_text(self.canvas_width-30, 10, text=self.score, \
                                     fill=color)

        self.id = canvas.create_text(30, 10, text = "Lives: ", \
                                     fill = color)
        self.lives_id = canvas.create_text(60, 10, text = self.lives, \
                                     fill = color)

    #increase the score by 1
    def increase(self):
        self.score += 1
        self.canvas.itemconfig(self.score_id, text=self.score)

    #lose a life
    def lose_life(self):
        self.lives -=1
        self.canvas.itemconfig(self.lives_id, text=self.lives)
        self.check_life()

    #check to see if the player has any lives left
    def check_life(self):
        if self.lives == 0:
            self.lose = True

            


###################################### 
class Game(object):
    def __init__(self, canvas, frog, car, log, score):
        self.canvas = canvas
        self.frog = frog
        self.car = car
        self.log = log
        self.score = score
        self.speed = 0.05
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def restart(self):

        self.frog.condition = False
        self.hit_text = canvas.create_text(self.canvas_width/2,200,text="You Died!",
                                    fill="black",font="TimesNewRoman 36")
        tk.update_idletasks()
        tk.update()

        if self.score.lose == False:
            self.frame = Frame(tk)
            self.frame.pack()
            
            self.button_quit = Button(self.frame, text="QUIT", bg="green", command = quit)
            self.button_quit.pack(side=LEFT)
            self.button_again = Button(self.frame,text="PLAY AGAIN", bg = 'green', command = self.play_again)
            self.button_again.pack(side=LEFT)

        if self.score.lose == True:
            if frog.hit_object == True:
                self.canvas.delete(self.hit_text)
                self.gameOverText = canvas.create_text(self.canvas_width/2,200,text="Game Over",
                                    fill="black",font="TimesNewRoman 15")
                time.sleep(2)
                self.frog.condition = False
                    
    def win_the_game(self):
        self.frog.condition = False
        self.hit_text = canvas.create_text(self.canvas_width/2,200,text="You Win!",
                                    fill="black",font="TimesNewRoman 36")
        tk.update_idletasks()
        tk.update()
    
    def play_again(self):
        #removes the buttons and the extra row off the canvas
        self.button_quit.destroy()
        self.button_again.destroy()
        self.frame.destroy()

        #resets the score
        self.score.score = 0
        self.canvas.itemconfig(self.score.score_id, text=self.score.score)
        self.canvas.delete(self.hit_text)

        #resets the frog
        self.canvas.delete(self.frog.id)
        frog = Frog(canvas, "green", score, car, log)
        self.frog = frog

        #starts the mainloop again
        self.mainloop()

            
    #This is our animation loop
    def mainloop(self):
        while self.frog.condition: 
            if self.frog.started == True:
                if self.frog.hit_object==False:
                    self.frog.check_hit_object()
                    self.frog.draw()
                    self.car.draw()
                    self.log.draw()
                elif self.frog.hit_object==True:
                    self.restart()
                if self.score.score >= 5:
                    self.win_the_game()

            tk.update_idletasks()
            tk.update()
            time.sleep(self.speed)


def window_setup(canvas):
    global lily_pad_array
    
    canvas_height = canvas.winfo_height()
    canvas_width = canvas.winfo_width()
    
    #create the grass areas
    grass1 = canvas.create_rectangle (0,0,canvas_width, 35, fill="dark green")
    canvas.move(grass1, 0, canvas_height-35)
    grass2 = canvas.create_rectangle(0,0, canvas_width, 30, fill = "dark green")
    canvas.move(grass2, 0, canvas_height-(35+1.5*6*20))
    grass3 = canvas.create_rectangle (0,0,canvas_width, 35, fill="dark green")
    canvas.move(grass3, 0, canvas_height-(35+ 2*1.5*5*20+30+35))

    #create the spaces for the frog to go in (lily pads)
    lily_pad_1 = canvas.create_rectangle (0,0, 30, 30, fill = "dark gray")
    canvas.move(lily_pad_1, canvas_width/6-15,canvas_height-(35+ 2*1.5*5*20+30+30))

    lily_pad_2 = canvas.create_rectangle (0,0, 30, 30, fill = "dark gray")
    canvas.move(lily_pad_2, 2*canvas_width/6-15,canvas_height-(35+ 2*1.5*5*20+30+30))

    lily_pad_3 = canvas.create_rectangle (0,0, 30, 30, fill = "dark gray")
    canvas.move(lily_pad_3, 3*canvas_width/6-15, canvas_height-(35+ 2*1.5*5*20+30+30))

    lily_pad_4 = canvas.create_rectangle (0,0, 30, 30, fill = "dark gray")
    canvas.move(lily_pad_4, 4*canvas_width/6-15,canvas_height-(35+ 2*1.5*5*20+30+30))

    lily_pad_5 = canvas.create_rectangle (0,0, 30, 30, fill = "dark gray")
    canvas.move(lily_pad_5, 5*canvas_width/6-15,canvas_height-(35+ 2*1.5*5*20+30+30))

    lily_pad_array.append(lily_pad_1)
    lily_pad_array.append(lily_pad_2)
    lily_pad_array.append(lily_pad_3)
    lily_pad_array.append(lily_pad_4)
    lily_pad_array.append(lily_pad_5)
    
    #create the road area
    road = canvas.create_rectangle(0,0, canvas_width, 1.5*5*20, fill = "dark gray")
    canvas.move(road, 0, canvas_height-(35 + 1.5*5*20))

    #create the water area
    water = canvas.create_rectangle(0,0, canvas_width, 1.5*5*20, fill = "light blue")
    canvas.move(water, 0, canvas_height-(35 + 2*1.5*5*20 + 30))


#Normal tkinter intro.
tk = Tk()
#Title of the game
tk.title("Frogger")
tk.resizable(0, 0)
#window appears on top
tk.wm_attributes("-topmost", 1)
#dimensions of the canvas
canvas = Canvas(tk, width=900, height=420, bd=0, highlightthickness=0)
canvas.pack()

#tkinter redraws the canvas
tk.update()

#this array contains the coordinates for the winning spaces at the top of the game board
lily_pad_array = []
#runs the function which sets up the game window
window_setup(canvas)

#defines all the objects on the screen
car = Car(canvas)
log = Log(canvas)
score = Score(canvas, "blue")
frog = Frog(canvas, "green", score, car, log)
game = Game(canvas, frog, car, log, score)

#run the main loop
game.mainloop()
