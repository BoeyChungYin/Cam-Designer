#Boey Chung Yin - Mini Project
#Formulas are seperated into different functions
#x and y coordinates are multiplied by a scaling factor to adjust for screen size


import csv
import turtle
from math import *

#Ask the user whether they wish to enter new data
y = input("Do you wish to create a new file?\nThis may overwrite existing data.\n(Enter Y or N): ")

#This sections runs only if users wishes to input data
if y == 'Y' or y == 'y' or y == 'yes' or y == 'Yes':
    
    #creating the data file used to store information on the cams
    with open("cam_data.csv", 'w') as data_file:
        headers = ['cam', 'segment', 'displacement', 'range', 'motion', 'motion type', 'base', 'follower']
        data_writer = csv.DictWriter(data_file, fieldnames=headers)
        data_writer.writeheader()

    #Keep prompting if invalid value entered
    while True:
        try:
            num_cam = int(input("Enter the number of Cams you wish to design: "))   #user enters number of cams
        except ValueError:
            print("***Please re enter an integer value***")
            continue
        if num_cam < 0:
            print("***Number cannot be negative, please re enter***")
            continue
        break
            
    for cam in range(1, num_cam+1):
        print("\nCAM", cam)

        #Keep prompting if invalid Base Radius entered
        while True:
            try:
                base = float(input("Enter the radius of the base circle(mm): "))  #user enters the base radius
            except ValueError:
                print("***Please re enter an number***")
                continue
            if base < 0:
                print("***Base radius cannot be negative, please re enter***")
                continue
            break

        #Keep prompting if invalid Follower Radius entered
        while True:
            try:
                follow = float(input("Enter the radius of the follower(mm): "))    #user enters the follower radius
            except ValueError:
                print("***Please re enter an number***")
                continue
            if follow < 0:
                print("***Follower radius cannot be negative, please re enter***")
                continue
            break

        #Keep prompting if number of segments is out of range
        while True:
            try:
                num_seg = int(input("Enter the number of segments(2 to 6): "))   #user enters number of segments
            except ValueError:
                print("***Please re enter an integer value***")
                continue
            if num_seg > 6 or num_seg < 2:
                print("***Number of segments out of range, please re enter (2 to 6)***")
            else:
                break

        #Keep prompting to enter information if degerees don't add up to 360
        while True:
            maxDis = 0          #Keeps track of the maximum displacement
            tot_ang = 0         #Holds the total degrees
            tot_dis = 0         #Holds the total displacement
            seg_info = list()   #List to hold all the information (resets each loop)
            
            for i in range(1, num_seg+1):
                print(f"\nFor segment {i}:")

                #Keep prompting until valid motion is entered
                while True:
                    motion = input("Enter the motion of the segment (rise/dwell/return): ") #user enters motion
                    if motion != 'rise' and motion != 'dwell' and motion != 'return':
                        print("***Invalid input, please re enter***")
                    elif i == 1 and motion == 'return':
                        print("***Cannot start with \'return\', please re enter***")
                    elif tot_dis == 0 and motion == 'return':
                        print("***Cannot \'return\' when displacement is 0***")
                    elif tot_dis == 2*base and motion == 'rise':
                        print("***Maximum displacement reached, cannot \'rise\' further***")
                    else:
                        break
                    
                if motion == 'dwell':
                    motion_type = None
                    d = 0
                else:
                    print("1: Constant Acceleration\n2: Simple Harmonic Motion\n3: Cycloidal Motion")

                    #Keep prompting until valid motion type is entered
                    while True:
                        try:
                            motion_type = int(input("Enter the type of motion (enter the number): "))   #user enters type of motion
                        except ValueError:
                            print("***Please re enter an integer value***")
                            continue
                        if motion_type < 1 or motion_type > 3:
                            print("***Invalid input, please enter an integer between 1 to 3***")
                        else:
                            break

                    #Keep prompting until valid displacement height is entered
                    while True:
                        try:
                            d = float(input("Enter the height of displacement(mm): ")) #user enters the displacement
                        except ValueError:
                            print("***Please re enter a valid number***")
                            continue
                        if d < 0:
                            print("***Displacement cannot be negative, please re enter***")
                            continue
                        if motion == 'rise':
                            tot_dis += d
                            if tot_dis > 2*base:
                                tot_dis -= d    #resets the value of tot_dis to previous value
                                print("***Maximum displacement cannot be more than diameter of base circle***")
                                print("***Maximum displacement exceeded, please re enter***")
                                continue
                            if tot_dis > maxDis:    #update the maximum displacement
                                maxDis = tot_dis
                        elif motion == 'return':
                            tot_dis -= d
                            if tot_dis < 0:
                                tot_dis += d    #resets the value of tot_dis to previous value
                                print("***Total displacement cannot be negative, please re enter***")
                                continue
                        break

                #Keep prompting until valid angle is entered
                while True:
                    try:
                        ang_range = float(input("Enter the angle the segment will span(Degrees): "))#user enters the degree range
                    except ValueError:
                        print("***Please enter a valid number***")
                        continue
                    if ang_range < 0:
                        print("***Angle cannot be negative, please re enter***")
                        continue
                    break
                    
                tot_ang += ang_range    #keep track of the total angle

                #display current displacement and angle for reference
                print(f"Current Displacement is {tot_dis}mm")
                print(f"Current angle is {tot_ang}" + u'\N{DEGREE SIGN}')

                #add the information(dictionary) into the list seg_info
                seg_info.append({'cam': cam, 'segment': i, 'displacement': d,
                                 'range': ang_range, 'motion': motion, 'motion type': motion_type,
                                 'base': base, 'follower': follow})
            
            #check if angles add to 360 and total displacement = 0
            if tot_ang == 360 and tot_dis == 0:
                with open("cam_data.csv", 'a') as data_file:    #enter the user input into the data file
                    headers = ['cam', 'segment', 'displacement', 'range', 'motion', 'motion type', 'base', 'follower']
                    data_writer = csv.DictWriter(data_file, fieldnames=headers)
                    for line in seg_info:
                        data_writer.writerow(line)
                break
            else:
                print("\n***Angles do not add up to 360 degrees or displacement does not return to 0, Please re-enter cam data***")


#Get the maximum displacement value for a CAM
def getMaxDis(cam):
    maxDis = 0
    currDis = 0
    
    with open('cam_data.csv', 'r') as data_file:
        data_reader = csv.DictReader(data_file)

        for line in data_reader:
            if int(line['cam']) == cam:
                
                #Keep track of the current displacement
                if line['motion'] == 'rise':
                    currDis += float(line['displacement'])
                elif line['motion'] == 'return':
                    currDis -= float(line['displacement'])
                    
                #Keep track of the maximum displacement
                if currDis > maxDis:
                    maxDis = currDis
    return maxDis

#Read the number of CAMs in the file
def getNumCam():
    with open('cam_data.csv', 'r') as data_file:
        data_reader = csv.DictReader(data_file)
        num_cam = 0
        
        for line in data_reader:
            if int(line['cam']) > num_cam:
                num_cam = int(line['cam'])
    return num_cam

#Formulas
def constAccRise1(theta, h, beta, angle):   #Constant Acceleration Rise 1
    theta = radians(theta)
    beta = radians(beta)
    angle = radians(angle)
    
    f0 = 2*h*(theta/beta)**2

    xPrime = cos(angle)*(4*h*theta/beta**2) - (r0 + f0)*sin(angle)
    yPrime = sin(angle)*(4*h*theta/beta**2) + (r0 + f0)*cos(angle)
    m = sqrt((-yPrime)**2 + xPrime**2)
    nX = (-yPrime)/m
    nY = xPrime/m
    return f0, nX, nY

def constAccRise2(theta, h, beta, angle):   #Constant Acceleration Rise 2
    theta = radians(theta)
    beta = radians(beta)
    angle = radians(angle)

    f0 = h*(1-2*(1-theta/beta)**2)

    xPrime = cos(angle)*(4*h/beta-4*h*theta/beta**2) - (r0 + f0)*sin(angle)
    yPrime = sin(angle)*(4*h/beta-4*h*theta/beta**2) + (r0 + f0)*cos(angle)
    m = sqrt((-yPrime)**2 + xPrime**2)
    nX = (-yPrime)/m
    nY = xPrime/m
    return f0, nX, nY

def constAccRe1(theta, h, beta, angle): #Constant Acceleration Return 1
    theta = radians(theta)
    beta = radians(beta)
    angle = radians(angle)

    f0 = h*(1-2*(theta/beta)**2)

    xPrime = cos(angle)*(-4*h*theta/beta**2) - (r0 + f0)*sin(angle)
    yPrime = sin(angle)*(-4*h*theta/beta**2) + (r0 + f0)*cos(angle)
    m = sqrt((-yPrime)**2 + (xPrime**2))
    nX = (-yPrime)/m
    nY = xPrime/m
    return f0, nX, nY

def constAccRe2(theta, h, beta, angle): #Constant Acceleration Return 2
    theta = radians(theta)
    beta = radians(beta)
    angle = radians(angle)

    f0 = 2*h*(1-theta/beta)**2
    
    xPrime = cos(angle)*(-4*h/beta+4*h*theta/beta**2) - (r0 + f0)*sin(angle)
    yPrime = sin(angle)*(-4*h/beta+4*h*theta/beta**2) + (r0 + f0)*cos(angle)
    m = sqrt((-yPrime)**2 + xPrime**2)
    nX = (-yPrime)/m
    nY = xPrime/m
    return f0, nX, nY

def harRise(theta, h, beta, angle): #Harmonic Rise
    theta = radians(theta)
    beta = radians(beta)
    angle = radians(angle)

    f0 = h*(1-cos(pi*theta/beta))/2

    xPrime = cos(angle)*(h*pi*sin(pi*theta/beta)/(2*beta)) - (r0 + f0)*sin(angle)
    yPrime = sin(angle)*(h*pi*sin(pi*theta/beta)/(2*beta)) + (r0 + f0)*cos(angle)
    m = sqrt((-yPrime)**2 + xPrime**2)
    nX = (-yPrime)/m
    nY = xPrime/m
    return f0, nX, nY

def harRe(theta, h, beta, angle):   #Harmonic Return
    theta = radians(theta)
    beta = radians(beta)
    angle = radians(angle)

    f0 = h*(1+cos((pi*theta)/beta))/2

    xPrime = cos(angle)*(-h*pi*sin(pi*theta/beta)/(2*beta)) - (r0 + f0)*sin(angle)
    yPrime = sin(angle)*(-h*pi*sin(pi*theta/beta)/(2*beta)) + (r0 + f0)*cos(angle)
    m = sqrt((-yPrime)**2 + xPrime**2)
    nX = (-yPrime)/m
    nY = xPrime/m
    return f0, nX, nY

def cycRise(theta, h, beta, angle): #Cycloidal Rise
    theta = radians(theta)
    beta = radians(beta)
    angle = radians(angle)

    f0 = h*(theta/beta-sin(2*pi*theta/beta)/(2*pi))

    xPrime = cos(angle)*((h/beta)*(1-cos(2*pi*theta/beta))) - (r0 + f0)*sin(angle)
    yPrime = sin(angle)*((h/beta)*(1-cos(2*pi*theta/beta))) + (r0 + f0)*cos(angle)
    m = sqrt((-yPrime)**2 + xPrime**2)
    nX = (-yPrime)/m
    nY = xPrime/m
    return f0, nX, nY

def cycRe(theta, h, beta, angle):   #Cycloidal Return
    theta = radians(theta)
    beta = radians(beta)
    angle = radians(angle)

    f0 = h*(1-theta/beta+sin(2*pi*theta/beta)/(2*pi))

    xPrime = cos(angle)*((h/beta)*(cos(2*pi*theta/beta)-1)) - (r0 + f0)*sin(angle)
    yPrime = sin(angle)*((h/beta)*(cos(2*pi*theta/beta)-1)) + (r0 + f0)*cos(angle)
    m = sqrt((-yPrime)**2 + xPrime**2)
    nX = (-yPrime)/m
    nY = xPrime/m
    return f0, nX, nY

#Get the x,y coordinates of the CAM in dwell segment
def dwell(currDis, angle):
    x = (baseR+currDis)*cos(radians(angle))
    y = (baseR+currDis)*sin(radians(angle))
    return x,y

#Get the x,y coordinates of the pitch curve
def pitchXY(f0, angle):
    r = r0 + f0
    x = r*cos(radians(angle))
    y = r*sin(radians(angle))
    return x,y

#Get the x,y cooridnates of the CAM in Rise or Return segments
def camXY(x, y, nX, nY):
    xCam = x + followR*nX
    yCam = y + followR*nY
    return xCam, yCam

#Writing the segment information
def writeinfo(tinfo, seg, motion, angle, dis, motionType):
    L = seg + '. ' + motion.capitalize() + ', ' + str(int(angle)) + u'\N{DEGREE SIGN}'

    if motion != 'dwell':
        L += ', ' + str(int(dis)) + 'mm, '
    
        if motionType == '1':
            L += 'constant acceleration'
        elif motionType == '2':
            L += 'simple harmonic'
        elif motionType == '3':
            L += 'cycloidal'
        
    tinfo.write(L, align='left', font=('Arial', 12, 'normal'))
    tinfo.sety(tinfo.ycor()-20)
    

#Attempt to obtain the number of CAMs
try:
    numOfCam = getNumCam()
except FileNotFoundError:   #print error message if no existing file
    close = input("***No existing file found, enter any key to exit***")
    exit()
    
cam = 0                 #Initialize the cam counter
r0 = 0                  #Initialize the variable Ro
baseR = 0               #Initialize the variable for base circle radius
followR = 0             #Initialize the variable for the follower radius

#Set up the screen
s = turtle.Screen()
#Place the screen on the front
rootwindow = s.getcanvas().winfo_toplevel()
rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
rootwindow.call('wm', 'attributes', '.', '-topmost', '0')
s.setup(0.8, 0.8)   #set screen to 80% of display size

#This function is to be called when drawing each CAM
def draw(dummy1, dummy2):   #Takes 2 arguments which are not used, to use "onclick()" method
    s.clear()   #clears out the current screen
    global cam
    cam += 1    #Increment the cam counter

    global baseR
    global followR
    global r0

    #Read the Base Radius and Follower Radius
    with open('cam_data.csv', 'r') as data_file:
        data_reader = csv.DictReader(data_file)

        for line in data_reader:
            cam_num = int(line['cam'])

            if cam_num == cam:  #Check whether the line information is for the current CAM
                baseR = float(line['base'])
                followR = float(line['follower'])
                r0 = baseR + followR    #Calculate Ro

    #Read the file for drawing
    with open('cam_data.csv', 'r') as data_file:
        data_reader = csv.DictReader(data_file)
        
        maxDis = getMaxDis(cam)             #Getting the maximum displacement value
        yMax = maxDis + 5 - (maxDis % 5)    #Calculate the maximum y value on the y-axis
        yStep = int(yMax/5)                 #Calculate each step on the y-axis
        yScale = s.window_height()/3/yMax   #Get the screen distance of one mm of displacement
        xScale = s.window_width()/3/360     #Get the screen distance of one degree

        global camScale
        camScale = s.window_height()/3/(yMax+r0)    #Scale factor for the CAM

        #create turtle for drawing the displacement graph
        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        t.pensize(2)
        t.pu()
        t.goto(-s.window_width()/2.5, -s.window_height()/4)   #origin of display graph
        startX, startY = t.xcor(), t.ycor() #store the coordinates of the origin
        t.pd()

        #drawing x-axis
        t.seth(270)
        t.fd(5)
        t.pu()
        t.fd(20)    #draw the first marking
        t.write('0', align='center', font=('Arial', 10, 'normal'))
        t.sety(startY)
        t.seth(0)
        t.pd()
        for i in range(1,13):   #Divide 360 degrees into 12 parts
            t.fd(s.window_width()/36)   #1/3 window width / 12 parts (360/30 = 12)
            t.seth(270)
            t.pen({'pencolor': 'grey80', 'pensize': 1})   #drawing the lines
            t.bk(s.window_height()/3)
            t.sety(startY)
            t.pen({'pencolor': 'black', 'pensize': 2})
            t.fd(5)
            t.pu()
            t.fd(20)
            t.write(str(i*30), align='center', font=('Arial', 10, 'normal'))
            t.sety(startY)
            t.seth(0)
            t.pd()
        t.goto(startX, startY)  #go back to origin

        #drawing the y-axis
        t.seth(180)
        t.fd(5)
        t.pu()
        t.fd(10)    #draw the first marking
        t.write('0', align='right', font=('Arial', 10, 'normal'))
        t.setx(startX)
        t.seth(90)
        t.pd()
        for i in range(1,6):    #Divide the y-axis into 5 parts
            t.fd(s.window_height()/15)  #1/3 window height / 5 parts
            t.seth(180)
            t.pen({'pencolor': 'grey80', 'pensize': 1})   #drawing the lines
            t.bk(s.window_width()/3)
            t.setx(startX)
            t.pen({'pencolor': 'black', 'pensize': 2})
            t.fd(5)
            t.pu()
            t.fd(10)    #draw the markings
            t.write(str(i* yStep), align='right', font=('Arial', 10, 'normal'))
            t.setx(startX)
            t.seth(90)
            t.pd()

        #drawing the labels
        t.pu()
        t.goto(startX + s.window_width()/6, startY-50)  #position of x-axis label
        t.write("CAM angle (degrees)", align='center', font=('Arial', 14, 'normal'))
        t.goto(startX - 80, startY + s.window_height()/3 + 30)   #position of y-axis label
        t.write("Displacement (mm)", align='left', font=('Arial', 14, 'normal'))
        t.goto(0, s.window_height()*4/10)   #postion of the title
        t.write("CAM", move = True, align='center', font=('Arial', 16, 'normal'))
        t.write(cam, font=('Arial', 16, 'normal'))
        t.goto(0, s.window_height()*36/100)  #postion for displaying the Base Radius
        t.write("(Red circle)Base Radius(mm) = ", move = True, align='center', font=('Arial', 16, 'normal'))
        t.write(baseR, font=('Arial', 16, 'normal'))
        t.goto(0, s.window_height()*32/100)   #position for displaying the Follow Radius
        t.write("(Blue circle)Follower Radius(mm) = ", move = True, align='center', font=('Arial', 16, 'normal'))
        t.write(followR, font=('Arial', 16, 'normal'))
        t.goto(startX, startY)  #go back to origin
        t.seth(0)
        t.pd()

        #Create a turtle for drawing the pitch circle
        tpitch = turtle.Turtle()
        tpitch.hideturtle()
        tpitch.speed(0)
        tpitch.pencolor("blue")
        tpitch.fillcolor("cyan")
        tpitch.pu()
        tpitch.goto(s.window_width()/4, 0)  #move to the center of the CAM
        xCamStart = tpitch.xcor()           #x-coordinate of the CAM center (y is 0)
        tpitch.goto(s.window_width()/4 + r0*camScale, -followR*camScale)    #position of the follower
        tpitch.pd()
        tpitch.begin_fill()
        tpitch.circle(followR*camScale) #draw the follower
        tpitch.end_fill()
        tpitch.pu()
        tpitch.sety(0)  #move to beginning of the pitch curve
        tpitch.pd()

        #Create a turtle for drawing the CAM circle
        tcam = turtle.Turtle()
        tcam.hideturtle()
        tcam.speed(0)
        tcam.fillcolor("grey80")
        tcam.pu()
        tcam.goto(s.window_width()/4 + baseR*camScale, 0)   #move to beginning of the CAM
        tcam.pd()
        tcam.begin_fill()

        #Create a turtle for writing the segment information
        tinfo = turtle.Turtle()
        tinfo.hideturtle()
        tinfo.speed(0)
        tinfo.pu()
        tinfo.goto(startX, s.window_height()*4/10)
        
        currDis = 0     #Hold the current displacement
        angle = 0       #Hold the current angle (theta)
        t.pencolor('red')
        
        #draw the displacement graph, CAM and pitch curve
        for line in data_reader:
            cam_num = int(line['cam'])

            if cam_num == cam:  #Check whether the line information is for the current CAM

                segNum = line['segment']            #Read the segment number
                motionType = line['motion type']    #Read the motion type (i.e. harmonic)
                motion = line['motion']             #Read the motion (i.e. rise)
                angRange = float(line['range'])     #Read the angle range (degrees)
                dis = float(line['displacement'])   #Read the displacement (mm)

                #write the segment information
                writeinfo(tinfo, segNum, motion, angRange, dis, motionType)
                
                #dwell segments
                if motion == 'dwell':
                    t.fd(angRange*xScale)   #for displacement graph
                    
                    for i in range(int(angRange)):
                        x,y = pitchXY(currDis, angle)   #pitch curve
                        tpitch.goto(x*camScale+xCamStart, y*camScale)
                        
                        xCam, yCam = dwell(currDis, angle)  #CAM
                        tcam.goto(xCam*camScale+xCamStart, yCam*camScale)
                        
                        angle = angle + 1
                
                #rise segments
                elif motion == 'rise':

                    #constant acceleration
                    if motionType == '1':
                        for theta in range(int(angRange/2)):
                            f0, nX, nY = constAccRise1(theta,dis,angRange,angle)

                            #displacement graph
                            t.goto(t.xcor()+ xScale, (f0+currDis)*yScale + startY)

                            #pitch curve
                            x,y = pitchXY(f0+currDis, angle)
                            tpitch.goto(x*camScale+xCamStart,y*camScale)

                            #CAM
                            xCam, yCam = camXY(x, y, nX, nY)
                            tcam.goto(xCam*camScale+xCamStart, yCam*camScale)
                            
                            angle = angle + 1
                            
                        for theta in range(int(angRange/2), int(angRange)):
                            f0, nX, nY = constAccRise2(theta,dis,angRange,angle)

                            #displacement graph
                            t.goto(t.xcor()+ xScale, (f0+currDis)*yScale + startY)

                            #pitch curve
                            x,y = pitchXY(f0+currDis, angle)
                            tpitch.goto(x*camScale+xCamStart,y*camScale)

                            #CAM
                            xCam, yCam = camXY(x, y, nX, nY)
                            tcam.goto(xCam*camScale+xCamStart, yCam*camScale)
                            
                            angle = angle + 1

                    #simple harmonic motion
                    elif motionType == '2':
                        for theta in range(int(angRange)):
                            f0, nX, nY = harRise(theta,dis,angRange,angle)

                            #displacement graph
                            t.goto(t.xcor()+ xScale, (f0+currDis)*yScale + startY)

                            #pitch curve
                            x,y = pitchXY(f0+currDis, angle)
                            tpitch.goto(x*camScale+xCamStart,y*camScale)

                            #CAM
                            xCam, yCam = camXY(x, y, nX, nY)
                            tcam.goto(xCam*camScale+xCamStart, yCam*camScale)
                            
                            angle = angle + 1
                        

                    #cyclodial motion
                    elif motionType == '3':
                        for theta in range(int(angRange)):
                            f0, nX, nY = cycRise(theta,dis,angRange,angle)

                            #displacement graph
                            t.goto(t.xcor()+ xScale, (f0+currDis)*yScale + startY)

                            #pitch curve
                            x,y = pitchXY(f0+currDis, angle)
                            tpitch.goto(x*camScale+xCamStart,y*camScale)

                            #CAM
                            xCam, yCam = camXY(x, y, nX, nY)
                            tcam.goto(xCam*camScale+xCamStart, yCam*camScale)
                            
                            angle = angle + 1

                    currDis += dis  #Update current displacement
                        
                #return segments
                elif motion == 'return':

                    #constant acceleration
                    if motionType == '1':
                        for theta in range(int(angRange/2)):
                            f0, nX, nY = constAccRe1(theta,dis,angRange,angle)

                            #displacement graph
                            t.goto(t.xcor()+ xScale, (f0+currDis-dis)*yScale + startY)

                            #pitch curve
                            x,y = pitchXY(f0+currDis-dis, angle)
                            tpitch.goto(x*camScale+xCamStart,y*camScale)

                            #CAM
                            xCam, yCam = camXY(x, y, nX, nY)
                            tcam.goto(xCam*camScale+xCamStart, yCam*camScale)
                            
                            angle = angle + 1
                            
                        for theta in range(int(angRange/2), int(angRange)):
                            f0, nX, nY = constAccRe2(theta,dis,angRange,angle)

                            #displacement graph
                            t.goto(t.xcor()+ xScale, (f0+currDis-dis)*yScale + startY)

                            #pitch curve
                            x,y = pitchXY(f0+currDis-dis, angle)
                            tpitch.goto(x*camScale+xCamStart,y*camScale)

                            #CAM
                            xCam, yCam = camXY(x, y, nX, nY)
                            tcam.goto(xCam*camScale+xCamStart, yCam*camScale)
                            
                            angle = angle + 1

                    #simple harmonic motion
                    if motionType == '2':
                        for theta in range(int(angRange)):
                            f0, nX, nY = harRe(theta, dis, angRange,angle)

                            #displacement graph
                            t.goto(t.xcor()+ xScale, (f0+currDis-dis)*yScale + startY)

                            #pitch curve
                            x,y = pitchXY(f0+currDis-dis, angle)
                            tpitch.goto(x*camScale+xCamStart,y*camScale)

                            #CAM
                            xCam, yCam = camXY(x, y, nX, nY)
                            tcam.goto(xCam*camScale+xCamStart, yCam*camScale)
                            
                            angle = angle + 1

                    #cyclodial motion
                    if motionType == '3':
                        for theta in range(int(angRange)):
                            f0, nX, nY = cycRe(theta,dis,angRange,angle)

                            #displacement graph
                            t.goto(t.xcor()+ xScale, (f0+currDis-dis)*yScale + startY)

                            #pitch
                            x,y = pitchXY(f0+currDis-dis, angle)
                            tpitch.goto(x*camScale+xCamStart,y*camScale)

                            #CAM
                            xCam, yCam = camXY(x, y, nX, nY)
                            tcam.goto(xCam*camScale+xCamStart, yCam*camScale)
                            
                            angle = angle + 1

                    currDis -= dis  #Update current displacement
        #After the loop
        tcam.end_fill()
        tpitch.pu()
        tpitch.goto(xCamStart, -baseR*camScale)     #Draw the base circle
        tpitch.pen({'pendown': True, 'pencolor': 'red'})
        tpitch.circle(baseR*camScale)
        tpitch.pen({'pendown': False, 'pencolor': 'black'}) #Draw the center cross
        tpitch.goto(xCamStart, 0)
        tpitch.pd()
        tpitch.fd(s.window_height()/20)
        tpitch.bk(s.window_height()/10)
        tpitch.goto(xCamStart, 0)
        tpitch.seth(90)
        tpitch.fd(s.window_height()/20)
        tpitch.bk(s.window_height()/10)
        t.pu()
        t.goto(0,-s.window_height()*4/10)   #Position of the next prompt

    #check if there are still anymore CAMs
    if cam < numOfCam:
        t.write("Click to proceed to next CAM", align='center', font=("Arial", 16, 'normal'))
        s.onclick(draw) #click to call the draw function for the next CAM
    else:
        t.write("Click to exit", align='center', font=("Arial", 16, 'normal'))
        s.exitonclick() #click to exit

#Call the draw function for the first CAM
draw(None, None)


