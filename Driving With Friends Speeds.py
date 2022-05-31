from matplotlib import pyplot as plt
from matplotlib import colors as col
import random as rand
import numpy as np
from celluloid import Camera

NumberOfSnapshots = 51 #aka tMax
v0 = 0 #Initial velocity
p0 = 0.25 #Probability of slowing down
vMax = 5 #Maximum Speed
RoadLength = 100 #Length of road
n = 45 #Number of drivers
#Credit https://stackoverflow.com/questions/9401658/how-to-animate-a-scatter-plot

x = np.ones((RoadLength, 2))
x = np.negative(x)
yArray = np.zeros(n)

#Randomise Initial Positions
def RandomStart(x, v0, p0):
    Counter = 0
    while Counter != n:
        Random = rand.randint(0, RoadLength - 1)
        if x[Random, 0] == -1:
            x[Random, 0] = v0
            x[Random, 1] = p0 + (rand.random()-0.5)/2.5
            Counter += 1
    return(x)

x = RandomStart(x, v0, p0)

camera = Camera(plt.figure())

for t in range(NumberOfSnapshots):
    
    Positions = []
    SpeedColours = [()]
    Buffer = np.ones((RoadLength, 2))
    Buffer = np.negative(Buffer)
    
    #i represents the current position being inspected
    for Pos in range(RoadLength):
        
        #Pos = RoadLength - i - 1
        R = rand.random()
        v = x[Pos, 0]
        
        #Check if a car is present in position i.
        if v != -1:
            Prob = x[Pos, 1]
            SpeedColours = np.append(SpeedColours, col.to_hex((v/vMax*0.9+0.05, 0, 0.95-v/vMax*0.9)))
            
            #Calculate new speed:
                
            #Slowing down to avoid crash: scan 
            #Distance in front to look = ((v - 1)^2 + v - 1) / 2 + 0-to-v room to stop.
            d = ((v - 1)**2 + v - 1) / 2 + 1
            SlowDown = False
            
            #CarCheck is position ahead of car we look to know to slow down.
            if v != 0:
                for j in range(int(v)):
                    CarCheck = Pos + d + j
                    if CarCheck >= RoadLength:
                        CarCheck = CarCheck - RoadLength
                    #SlowDown true if velocity present in CarCheck-th position.
                    if x[int(CarCheck) , 0] != -1 and v != 0:
                        SlowDown = True
            
            #Continuing at current speed to avoid crash: scan
            #Distance in front to look = v^2 + v / 2 + 0-to-v
            d = (v**2 + v) / 2 + 1
            StayConstant = False
            
            for j in range(int(v) + 1):
                CarCheck = Pos + d + j
                if CarCheck >= RoadLength:
                    CarCheck = CarCheck - RoadLength
                #StayStill true if velocity present CarCheck-th position.
                if x[int(CarCheck), 0] != -1:
                        StayConstant = True
            
            #Slowing down
            if SlowDown == True:
                print("WHOA NELLY!", Pos)
                v -= 1

            #Attempting to speed up
            elif v < vMax and StayConstant != True:
                v += 1
                
            #Chance to slow down
            if R <= Prob and v != 0:
                v -= 1
            
            #Reset current position & probability
            Buffer[Pos, 0] = -1
            Buffer[Pos, 1] = -1
            
            #Calculate new position
            if Pos + v < RoadLength:
                Buffer[int(Pos + v), 0] = v
                Buffer[int(Pos + v), 1] = Prob
                
            else:
                Buffer[int(Pos + v - RoadLength), 0] = v
                Buffer[int(Pos + v - RoadLength), 1] = Prob
            
            Positions = np.append(Positions, Pos)
            print(v/vMax*0.9+0.05, 0, 0.95-v/vMax*0.9)

    x = Buffer
    
    label = str("t = " + str(t) + "; n = " + str(n))
    
    plt.ylim((-1, 1))
    plt.plot((0, RoadLength), (0, 0), c="black")
    print(SpeedColours)
    print("Pos:", Positions)
    print("yArray:", yArray)
    plt.scatter(Positions, yArray, c=SpeedColours, s=100)
    plt.text(0, 0.8, label)
    
    camera.snap()
anim = camera.animate(blit=True)
saveName = str(label + " Run 1.gif")
anim.save(saveName)

#Record final average speed
vAvg = 0
for Pos in range(RoadLength):
    v = x[Pos, 0]
    if v != -1:
        vAvg = vAvg + v/n
        
print("vAvg=", vAvg)