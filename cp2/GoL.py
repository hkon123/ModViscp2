import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

class GameOfLife(object):

    def __init__(self):
        self.dimensions = 50
        self.CoM = np.array((0,0))
        self.state = np.zeros((self.dimensions,self.dimensions)).astype(int)
        if int(raw_input('initialize random(1) or with a preset(0)? ')) == 0:
            self.setStateFromFile(str(raw_input('text file: ')))
        else:
        #self.writeToFile()
            self.setRandomState()

    def setRandomState(self):
        for i in range(0,self.dimensions):
            for j in range(self.dimensions):
                if np.random.uniform(0,1)>=0.5:
                    self.state[i,j] = 1
                else:
                    self.state[i,j] = 0

    def writeToFile(self):
        f = open('initial.txt', 'w')
        for i in self.state:
            for j in i:
                f.write(str(j))
                f.write(' ')
            f.write('\n')

    def readFromFile(self, filename):
        new = []
        with open(filename, 'r') as f:
            for line in f:
                test = line.split(' ')
                new.append(test)

        for i in new:
            del(i[-1])
            i.append(0)

        return np.array(new).astype(int)

    def setStateFromFile(self, filename):
        self.state = self.readFromFile(filename)


    def getLiveNeighbours(self,index1,index2):
        sum = 0
        sum += self.state[(index1-1)%self.dimensions,(index2-1)%self.dimensions]
        sum += self.state[(index1-1)%self.dimensions,index2]
        sum += self.state[(index1-1)%self.dimensions,(index2+1)%self.dimensions]
        sum += self.state[index1,(index2+1)%self.dimensions]
        sum += self.state[(index1+1)%self.dimensions,(index2+1)%self.dimensions]
        sum += self.state[(index1+1)%self.dimensions,index2]
        sum += self.state[(index1+1)%self.dimensions,(index2-1)%self.dimensions]
        sum += self.state[index1,(index2-1)%self.dimensions]
        return sum



    def updateNoAnim(self):
        t = time.time()
        for it in range(10000):
            self.currentStep = it
            if it%100==0:
                print(it/(time.time()-t))
            newState=np.zeros((self.dimensions,self.dimensions))
            for i in range(self.dimensions):
                for j in range(self.dimensions):
                    nrOfLiveNeighbours = self.getLiveNeighbours(i,j)
                    if self.state[i,j]==1:
                        if nrOfLiveNeighbours == 2 or nrOfLiveNeighbours==3:
                            newState[i,j] = 1
                    else:
                        if nrOfLiveNeighbours == 3:
                            newState[i,j] = 1
        self.state = newState
        self.CoM = np.vstack((self.CoM, self.getCentreOfMass()))


    def update(self, i):
        newState=np.zeros((self.dimensions,self.dimensions))
        self.currentStep = i
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                nrOfLiveNeighbours = self.getLiveNeighbours(i,j)
                if self.state[i,j]==1:
                    if nrOfLiveNeighbours == 2 or nrOfLiveNeighbours==3:
                        newState[i,j] = 1
                else:
                    if nrOfLiveNeighbours == 3:
                        newState[i,j] = 1
        self.state = newState
        self.im = plt.imshow(self.state, cmap='winter', interpolation='nearest')
        self.CoM = np.vstack((self.CoM, self.getCentreOfMass()))
        return [self.im]


    def run(self):
        fig, ax = plt.subplots()
        self.im=plt.imshow(self.state, cmap='winter', interpolation='nearest')
        anim = FuncAnimation(fig, self.update, frames = 10000, repeat = False, interval = 1, blit = True)
        plt.show()


    def getCentreOfMass(self):
        r= np.array((0,0))
        alive = 0
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                if self.state[i,j]==1:
                    if i == 0 or j == 0 or i == self.dimensions or j == self.dimensions:
                        return np.array((None,None))
                    else:
                        r[0]+=i
                        r[1]+=j
                        alive+=1
        r[0] = float(r[0])/float(alive)
        r[1] = float(r[1])/float(alive)
        return r

    def getAvrgSpeed(self):
        newCoM = np.array(())
        xsum = 0
        ysum = 0
        testVar = False
        for i in range(2,len(self.CoM)):
            if self.CoM[i,0] != None and testVar==False:
                xsum+= self.CoM[i,0] - self.CoM[i-1,0]
                ysum+= self.CoM[i,1] - self.CoM[i-1,1]
            elif self.CoM[i,0] != None and testVar == True:
                testVar = False
                continue
            elif self.CoM[i,0] == None:
                testVar = True
        speedx = float(xsum)/float(self.currentStep)
        speedy = float(ysum)/float(self.currentStep)
        return np.sqrt(np.power(speedx,2)+np.power(speedy,2))










A = GameOfLife()
A.run()
print(A.getAvrgSpeed())
