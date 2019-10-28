import scipy.io
import random
import numpy
import math
import matplotlib.pyplot as plt

class kMeans:

    def __init__(self):
        self.data= scipy.io.loadmat('AllSamples.mat')
        self.dataPoints=numpy.array(self.data['AllSamples'])
        
        
    """ ---------------------------------------- INITIALIZE CENTROID USING STRATEGY 1 ----------------------------------------- """
    def initializeCenter_Strategy1(self, k):
        centroidList=[]
        i=1;
        while(i<=k):
            randomPoint = self.dataPoints[random.randint(0,len(self.dataPoints)-1)]              # 9 to len(dataPoints)-1) a<=random<=b
            #randomPoint = dataPoints[random.sample(300,k)]
            #print(randomPoint)
            x=randomPoint[0]
            y=randomPoint[1]
            centroid = (x,y)
            if centroid not in centroidList:
                centroidList.append(centroid)
                i+=1
            #else:
            #print("same point selected")
        return centroidList
        
    """ ---------------------------------------- INITIALIZE CENTROID USING STRATEGY 2 ----------------------------------------- """
    def initializeCenter_Strategy2(self, k):
        centroidList=[]
        randomPoint = self.dataPoints[random.randint(0,len(self.dataPoints)-1)]              # 9 to len(dataPoints)-1) a<=random<=b
        #print("FIRST POINT : ", randomPoint)
        x1=randomPoint[0]
        y1=randomPoint[1]
        centroidList.append((x1,y1))
        
        i=2;
        while(i<=k):
            #print("ITERATION ------------ ",i)
            center=()
            maximum=float('-inf')
            for p in range(30):
                x = self.dataPoints[p][0]
                y = self.dataPoints[p][1]
                #print("P:   ",x,y)
                #c=0
                distance=0
                if (x,y) not in centroidList:
                    for centroid in centroidList:
                        #print("C:   ",centroid)
                        distance+=self.euclideanDistance(centroid,(x,y))
                        #c+=1
                    #print("******",distance,"******")
                    #distance/=c
                    if(distance>maximum):
                        #print("IN")
                        maximum=distance
                        center=(x,y)
                        #print("----",maximum)
                        #print("----",center)
            
            #print("Distance is : ", maximum)
            centroidList.append(center)
            i+=1
            #if center not in centroidList:
            #   centroidList.append(center)
            #   i+=1
            #   print("CCCCC: ", centroidList)
            #else:
            #   print("CENTER IS ALREADY PRESENT", center)
            #   print(centroidList)
            
        return centroidList

    """ ---------------------------------------- CALCULATE EUCLIDEAN DISTANCE ----------------------------------------------- """
    def euclideanDistance(self,point1,point2):
        return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

    """ ---------------------------------------- GET NEW CENTROIDS ----------------------------------------------------------- """
    def getNewCentroid(self,clusterDist,k):
        centroidList=[]
        for i in range(k):                          #change 2 to k
            numberOfPoints = len(clusterDist[i])
            avgX = 0
            avgY = 0
            #print(i,"-------",len(clusterDist[i]))
            if(numberOfPoints != 0):
                for points in clusterDist[i]:
                    avgX+=points[0]
                    avgY+=points[1]
                centroidList.append(((avgX/numberOfPoints),(avgY/numberOfPoints)))
        return centroidList
    
    """ ---------------------------------------- CHECK CHANGE IN CENTROID VALUES --------------------------------------------- """
    def checkCentroidEquality(self,newCentroidList, oldCentroidList,k):
        for i in range(k):
            #print(i, "-----------")
            #print(newCentroidList[i])
            #print(oldCentroidList[i])
            if newCentroidList[i] != oldCentroidList[i]:
                return False
        return True
        
        
    """ ---------------------------------------- OBJECTIVE FUNCTION ---------------------------------------------------------- """
    def objectiveFunction(self,centroidList,clusterDist,k):
        value = 0;
        for i in range(k):
            for p in range(len(clusterDist[i])):
                value = value+self.euclideanDistance(centroidList[i],clusterDist[i][p])**2   #Square of the distance
        return value

    """ ---------------------------------------- K MEAN ALGORITHM ------------------------------------------------------------ """
    def kMeansAlgorithm(self, choice):
        y_axis=[]
        for k in range(2,11):
            print("---------------------------------- K = ",k," ----------------------------------")
            if choice == 1 :
                centroidList = self.initializeCenter_Strategy1(k)
            elif choice == 2:
                centroidList = self.initializeCenter_Strategy2(k)
            #print("Centroid List : ", centroidList)
            
            iteration = 1
            while(True):
                clusterDist={}
                for i in range(k):                                      #change 2 to k
                    clusterDist[i] = []
                print("Iteration ", iteration)
                iteration+=1
                print("Centroid List : ", centroidList)
                for i in range(len(self.dataPoints)):                                  #change 5 to len(dataPoints) and even it the initialCenter
                    x = self.dataPoints[i][0]
                    y = self.dataPoints[i][1]
                    #print("Data Point : ", x," ",y)
                    cluster=0
                    maximum = float('inf')
                    for c in range(len(centroidList)):
                        distance = self.euclideanDistance(centroidList[c],(x,y))
                        #print("Distance from ", centroidList[c], "is", distance)
                        if distance<maximum:
                            maximum=distance
                            cluster=c
                    #print("Selected :", cluster)
                    clusterDist[cluster].append((x,y))
                #print("CLUSTERS")
                #print(clusterDist)
                #print("CLUSTER",len(clusterDist[0]))
                #print("CLUSTER",clusterDist[0][3])
                #print("CLUSTER",clusterDist)
                #print("OBJECTIVE FUNCTION COST :", self.objectiveFunction(centroidList,clusterDist,k))
                newCentroidList=self.getNewCentroid(clusterDist,k)
                #print("OLDDdddddddddddddd")
                #print(centroidList)
                #print("NEWWWWWWWWWWWWWWWW")
                #print(newCentroidList)
                if self.checkCentroidEquality(newCentroidList,centroidList,k):
                    #print("EQUAL")
                    break
                else:
                    #print("NOT EQUAL")
                    centroidList=newCentroidList
            #print("FINAL ---------- \n",centroidList)
            #print(clusterDist)
            print("******* Objective Function Value : ", self.objectiveFunction(centroidList,clusterDist,k))
            print()
            print()
            y_axis.append(self.objectiveFunction(centroidList,clusterDist,k))

        #print("Y**************************")
        #print(y_axis)
        x_axis=[2,3,4,5,6,7,8,9,10]
        plt.plot(x_axis,y_axis,linestyle='--',marker='o')
        plt.show()

    def main(self):
        choice = 0
        while(choice!=3):
            print("\n******* SELECT AN OPTION *******")
            print("1 : Strategy 1 - Pick centers randomly")
            print("2 : Strategy 2 - Pick centers based on average distance")
            print("3 : Exit")
            
            choice=int(input("Enter Choice: "))
            
            if choice == 1:
                self.kMeansAlgorithm(1)
            elif choice == 2:
                self.kMeansAlgorithm(2)
            elif choice == 3:
                print("Thank you")
            else:
                print("Incorrect option. Select again")
                
""" ------------------------------------- CALLING THE CLASS ----------------------------- """

run = kMeans()
run.main()

"""
TO DO LIST:

Multi-dimensional input
Multi-class classification

"""
