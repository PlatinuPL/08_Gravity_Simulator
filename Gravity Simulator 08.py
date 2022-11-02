#A simple gravity simulator that can show how the balls will behave at a certain gravity value
from ast import main
from cProfile import label
from ipaddress import collapse_addresses
import tkinter as tk
from tkinter import BOTH, CURRENT, HORIZONTAL, END
from matplotlib import pyplot

# Define window
root = tk.Tk()
root.title("Graity Simulator")
root.iconbitmap("earth.ico")
root.geometry("500x650")
root.resizable(0,0)

# Define fonts and colors
# system default

# Define global variables
time = 0
data = {}
for i in range(1,5):
    data['data_%d' % i] = []
# Define functions
def move(event):
    if "ball" in main_canvas.gettags(CURRENT):
        x1 = main_canvas.coords(CURRENT)[0]
        x2 = main_canvas.coords(CURRENT)[2]
        
        main_canvas.coords(CURRENT, x1, event.y, x2, event.y + 10)

        if main_canvas.coords(CURRENT)[3] <15:
            main_canvas.coords(CURRENT, x1, 5 , x2, 15)
            
        if main_canvas.coords(CURRENT)[3] >415:
            main_canvas.coords(CURRENT, x1, 405 , x2, 415)
        
    update_height()

def update_height():
    for i in range(1,5):
        heights["height_%d" % i].config(text = "Height: " + str(round(415- main_canvas.coords(balls["ball_%d" % i])[3], 2)))


def step(t):
    global time

    for i in range(1,5):
        a = -1*float(accelerations['a_%d' % i].get()) 
        v = -1*float(velocities['v_%d' % i].get())               
        d = v*t + .5*a*t**2 

        x1 =main_canvas.coords(balls["ball_%d" % i])[0]
        x2 =main_canvas.coords(balls["ball_%d" % i])[2]

        if main_canvas.coords(balls["ball_%d" % i])[3] + d <= 415:
            main_canvas.move(balls["ball_%d" % i], 0, d)
            y2 =main_canvas.coords(balls["ball_%d" % i])[3]
            main_canvas.create_line(x1, y2, x2, y2, tag ="DASH")
        else:
            main_canvas.coords(balls["ball_%d" % i], x1, 405, x2, 415)

        #Do more physics
        vf = v + a*t

        velocities["v_%d" %  i].delete(0,END)
        velocities["v_%d" % i].insert(0, str(round(-1*vf, 2)))

        data['data_%d' % i].append((time, 415 - main_canvas.coords(balls['ball_%d' % i])[3]))

    update_height()

    time += t 




def run():
    step(t_slider.get())
    while 15 < main_canvas.coords(balls["ball_1"])[3] < 415 or 15 < main_canvas.coords(balls["ball_2"])[3] <415 or 15 < main_canvas.coords(balls["ball_3"])[3] <415 or 15 < main_canvas.coords(balls["ball_4"])[3] <415:
        step(t_slider.get())



def graph():
    colors = ["red", "green", 'blue', 'yellow']

    for i in range(1,5):
        x = []
        y = []
        for data_list in data["data_%d" % i]:
            x.append(data_list[0])
            y.append(data_list[1])
        pyplot.plot(x,y,color = colors[i-1])


    pyplot.title('Distance vs. Time')
    pyplot.xlabel('Time')
    pyplot.ylabel('Distance')
    pyplot.show()



def reset():
    global time

    time = 0
    main_canvas.delete("DASH")

    for i in range (1,5):
        velocities["v_%d" % i].delete(0,END)
        velocities["v_%d" % i].delete(0,"0")
        accelerations["a_%d" % i].delete(0,END)
        accelerations["a_%d" % i].delete(0,"0")

        main_canvas.coords(balls['ball_%d' % i ], 45+(i-1)*100, 405, 55+(i-1)*100, 415)

        data["data_%d" % i].clear()
    
    update_height()
    t_slider.set(1)




# Create layout
canvas_frame = tk.Frame(root)
input_frame = tk.Frame(root)

canvas_frame.pack(padx =10)
input_frame.pack(fill = BOTH, expand = True)
 
# Canvas frame layout
main_canvas = tk.Canvas(canvas_frame, width=400, height=415, bg = "white")
main_canvas.grid(row=0,column=0,padx=5, pady=5)

line_0 = main_canvas.create_line(2,0,2,415)
line_1 = main_canvas.create_line(100,0,100,415)
line_2 = main_canvas.create_line(200,0,200,415)
line_3 = main_canvas.create_line(300,0,300,415)
line_4 = main_canvas.create_line(400,0,400,415)

balls = {}
balls["ball_1"] = main_canvas.create_oval(45, 405, 55, 415, fill = "red", tag = "ball")
balls["ball_2"] = main_canvas.create_oval(145, 405, 155, 415, fill = "green", tag = "ball")
balls["ball_3"] = main_canvas.create_oval(245, 405, 255, 415, fill = "blue", tag = "ball")
balls["ball_4"] = main_canvas.create_oval(345, 405, 355, 415, fill = "yellow", tag = "ball")

#Input frame layput
# Row labels
tk.Label(input_frame, text = "d").grid(row =0, column=0, ipadx = 22)
tk.Label(input_frame, text = "vi").grid(row =1, column=0)
tk.Label(input_frame, text = "a").grid(row =2, column=0)
tk.Label(input_frame, text = "t").grid(row =3, column=0)

# Heights/Distance labels
heights = {}
for i in range (1,5):
    heights["height_%d" % i] = tk.Label(input_frame, text="Height: " + str(415 - main_canvas.coords(balls["ball_%d" % i])[3]))
    heights["height_%d" % i].grid(row=0, column= i)

# Velocity entry  boxes
velocities = {}
for i in range (1,5):
    velocities["v_%d" % i ] = tk.Entry(input_frame, width=15)
    velocities["v_%d" % i ].grid(row=1, column= i, padx=1)
    velocities["v_%d" % i ].insert(0, "0")

# Acceleration entry boxes
accelerations = {}
for i in range (1,5):
    accelerations["a_%d" % i] = tk.Entry(input_frame, width=15)
    accelerations["a_%d" % i].grid(row = 2, column = i, padx =1)
    accelerations["a_%d" % i].insert(0, "0")

# Time slider
t_slider = tk.Scale(input_frame, from_ = 0, to=1, tickinterval=.2,resolution= .01, orient= HORIZONTAL)
t_slider.grid(row=3,column=1, columnspan=4, sticky= "WE")
t_slider.set(1)


# Define Buttons
step_button = tk.Button(input_frame, text = "Step", command=lambda:step(t_slider.get()))
run_button = tk.Button(input_frame, text = "Run", command= run)
graph_button = tk.Button(input_frame, text = "Graph", command = graph)
reset_button = tk.Button(input_frame, text = "Reset", command = reset)
quit_button = tk.Button(input_frame, text = "Quit", command= root.destroy)

step_button.grid(row =4, column=1, pady = (0,10), sticky="WE")
run_button.grid(row =4, column=2, pady = (0,10), sticky="WE")
graph_button.grid(row =4, column=3, pady = (0,10), sticky="WE")
reset_button.grid(row =4, column=4, pady = (0,10), sticky="WE")
quit_button.grid(row =5, column=1, columnspan=4, sticky="WE")

# Make each ball "dragable" in the vertical direction
root.bind("<B1-Motion>", move)


# Root main loop
root.mainloop()