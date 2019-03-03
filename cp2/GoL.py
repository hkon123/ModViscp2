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



class SIRS(object):

    def __init__(self, dimensions, p1, p2, p3, equilibration, sampleStep, iterations, immuneFraction = 0):
        self.immuneFraction = immuneFraction
        self.immune = 0
        self.iterations = iterations
        self.dimensions = dimensions
        self.equilibration = equilibration
        self.sampleStep = sampleStep
        self.maxImmune = np.power(dimensions, 2)*self.immuneFraction
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.infectedFraction = np.array(())
        self.state = np.zeros((self.dimensions,self.dimensions)).astype(int)
        if self.immuneFraction == 0:
            self.setRandomState()
        else:
            self.setRandomStateWithImmune()

    def setRandomState(self):
        for i in range(0,self.dimensions):
            for j in range(self.dimensions):
                rand = np.random.uniform(0,1)
                if rand<=0.33:
                    self.state[i,j] = 1         #S
                elif rand>0.33 and rand<=0.66:
                    self.state[i,j] = 0         #I
                else:
                    self.state[i,j] = -1        #R

    def setRandomStateWithImmune(self):
        for i in range(0,self.dimensions):
            for j in range(self.dimensions):
                rand = np.random.uniform(0,1)
                if rand<=0.33:
                    self.state[i,j] = 1         #S
                elif rand>0.33 and rand<=0.66:
                    self.state[i,j] = 0         #I
                else:
                    self.state[i,j] = -1        #R
        while self.immune<self.maxImmune:
            for i in range(0,self.dimensions):
                for j in range(self.dimensions):
                    if self.state[i,j]!=-2:
                        rand = np.random.uniform(0,1)
                        self.immuneProb = 0.5-float(self.immune)/float(2*self.maxImmune)
                        if rand<=self.immuneProb:
                            self.state[i,j] = -2      #Immune
                            self.immune+=1
                            continue


    def getInfectedNeighbours(self,index1,index2):
        if self.state[(index1-1)%self.dimensions,index2] == 0:
            return True
        if self.state[index1,(index2+1)%self.dimensions] == 0:
            return True
        if self.state[(index1+1)%self.dimensions,index2] == 0:
            return True
        if self.state[index1,(index2-1)%self.dimensions] == 0 :
            return True
        return False



    def updateNoAnim(self):
        for i in range(self.iterations):
            for sweep in range(self.dimensions*self.dimensions):
                index = np.random.randint(0,self.dimensions,2)
                randomNr = np.random.uniform(0,1)
                if self.state[index[0],index[1]]==1 and randomNr<=self.p1:
                    if self.getInfectedNeighbours(index[0],index[1])==True:
                        self.state[index[0],index[1]] = 0
                        continue
                elif self.state[index[0],index[1]]==0 and randomNr<=self.p2:
                    self.state[index[0],index[1]] = -1
                    continue
                elif self.state[index[0],index[1]]==-1 and randomNr<=self.p3:
                    self.state[index[0],index[1]] = 1
            if i ==self.equilibration or (i>self.equilibration and i%self.sampleStep==0):
                    self.infectedFraction = np.append(self.infectedFraction, self.getInfFrac())


    def update(self,i):
        for sweep in range(self.dimensions*self.dimensions):
            index = np.random.randint(0,self.dimensions,2)
            randomNr = np.random.uniform(0,1)
            if self.state[index[0],index[1]]==1 and randomNr<=self.p1:
                if self.getInfectedNeighbours(index[0],index[1])==True:
                    self.state[index[0],index[1]] = 0
                    continue
            elif self.state[index[0],index[1]]==0 and randomNr<=self.p2:
                self.state[index[0],index[1]] = -1
                continue
            elif self.state[index[0],index[1]]==-1 and randomNr<=self.p3:
                self.state[index[0],index[1]] = 1
                continue
            elif self.state[index[0],index[1]]==2:
                continue
        self.im = plt.imshow(self.state, interpolation='nearest', cmap = 'brg')
        return [self.im]

    def run(self):
        fig, ax = plt.subplots()
        self.im=plt.imshow(self.state, interpolation='nearest', cmap = 'brg')
        anim = FuncAnimation(fig, self.update, frames = self.iterations, repeat = False, interval = 1, blit = True)
        plt.show()


    def getInfFrac(self):
        infSum = 0
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                if self.state[i,j] == 0:
                    infSum += 1
        return float(infSum)/float(self.dimensions*self.dimensions)


    def plotInfFrac(self):
        x = np.arange(self.equilibration,self.iterations,self.sampleStep)
        plt.plot(x,self.infectedFraction)
        plt.show()


class Multiple(object):

    def __init__(self, equilibration, sampleStep, iterations, p2 = 0.5, dimensions = 50):
        self.equilibration = equilibration
        self.sampleStep = sampleStep
        self.iterations = iterations
        self.p2 = p2
        self.dimensions = dimensions
        self.p1 = np.arange(0.0,1,0.2)
        self.p3 = np.arange(0.0,1,0.2)
        self.infecFrac = np.zeros((len(self.p3),len(self.p1)))
        self.variance = np.zeros((len(self.p3),len(self.p1)))
        self.current = 0
        self.total = len(self.p1)*len(self.p3)

    def runM(self):
        for i in range(len(self.p1)):
            for j in range(len(self.p3)):
                A = SIRS(self.dimensions, self.p1[i],self.p2,self.p3[j],self.equilibration,self.sampleStep,self.iterations)
                A.updateNoAnim()
                self.infecFrac[j,i] = np.mean(A.infectedFraction)
                self.variance[j,i] = (np.mean(np.square(A.infectedFraction))-np.square(np.mean(A.infectedFraction)))/np.power(self.dimensions,2)
                print(str(self.current) + "/" + str(self.total))
                self.current +=1

    def getPlot(self):
        fig, ax = plt.subplots()
        self.im=plt.imshow(self.infecFrac, interpolation='nearest', cmap = 'inferno', extent = [0.0,1.0,0.0,1.0], origin = 'lower')
        plt.colorbar()
        plt.savefig('infectedFraction.png')
        plt.show()
        fig, ax = plt.subplots()
        self.im=plt.imshow(self.variance, interpolation='nearest', cmap = 'inferno', extent = [0.0,1.0,0.0,1.0], origin = 'lower')
        plt.colorbar()
        #plt.savefig('variancetest.png')
        plt.show()

class ReadFromFile(object):

    def Cmap(self):
        filename = raw_input("text file: ")
        new = []
        with open(filename, 'r') as f:
            for line in f:
                test = line.split(' ')
                new.append(test)
        for i in new:
            del(i[-1])
        self.infecFrac = np.array(new).astype(float)
        fig, ax = plt.subplots()
        self.im=plt.imshow(self.infecFrac, interpolation='nearest', cmap = 'inferno', extent = [0.0,1.0,0.0,1.0], origin = 'lower')
        plt.colorbar()
        plt.savefig('50by50fraction(10000sweeps).png')
        plt.show()

    def Graph(self):
        filename = raw_input("Plot file: ")
        new = []
        with open(filename, 'r') as f:
            for line in f:
                test = line.split(' ')
                new.append(test)
        #del(new[0,-1])
        infecFrac = np.array(new)
        infecFrac = np.delete(infecFrac,-1)
        infecFrac = infecFrac.astype(float)
        filename = raw_input("Error file: ")
        new = []
        with open(filename, 'r') as f:
            for line in f:
                test = line.split(' ')
                new.append(test)
        #del(new[0,-1])
        variance = np.array(new)
        variance = np.delete(variance,-1)
        variance = variance.astype(float)
        x = np.arange(0,1,0.01)
        plt.plot(x,infecFrac)
        plt.errorbar(x, infecFrac, yerr = variance)
        #plt.savefig("plot.png")
        plt.show()

#A = GameOfLife()

#A = SIRS(50, 0.5,0.5,0.5, 100,10,10000, immuneFraction =0.25)
#print(A.immune)
#A.run()
#A.updateNoAnim()
#A.plotInfFrac()

#A = Multiple(100,10,500)
#A.runM()
#A.getPlot()
if int(raw_input("countour(0) or graph plot(1)?"))==1:
    A=ReadFromFile().Graph()
else:
    A=ReadFromFile().Cmap()
