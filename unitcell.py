import math
from pprint import pprint

class UnitCell(object):
  def __init__(self, a0=[0.0,0.0,0.0], a1=[0.0, 0.0, 0.0], a2=[0.0,0.0,0.0]):
    
    allVectors = [a0, a1, a2]
    self.aMatrix = a0 + a1 + a2
    
    # volume = det(A)
    self.volume = self.scalarProduct (a0, self.crossProduct(a1, a2))
    
    if self.volume > 0.0:
      fac = 1.0 / self.volume
      amt0 = [fac * elem for elem in self.crossProduct(a1, a2)]
      amt1 = [fac * elem for elem in self.crossProduct(a2, a0)]
      amt2 = [fac * elem for elem in self.crossProduct(a0, a1)]
      
      aMatrixInverse = []
      for e1, e2, e3 in zip(amt0, amt1, amt2):
        aMatrixInverse.append(e1)
        aMatrixInverse.append(e2)
        aMatrixInverse.append(e3)
        
      aMatrixInvTranspose = amt0 + amt1 + amt2
      
      self.bVec0 = [2.0 * math.pi * elem for elem in amt0]
      self.bVec1 = [2.0 * math.pi * elem for elem in amt1]
      self.bVec2 = [2.0 * math.pi * elem for elem in amt2]
      
      self.bMatrix = self.bVec0 + self.bVec1 + self.bVec2
    else:
      # Initialize everything to zeros
      self.bVec0 = [0.0] * 3
      self.bVec1 = [0.0] * 3
      self.bVec2 = [0.0] * 3
      self.aMatrixInverse = [0.0] * 9
      self.bMatrix = [0.0] * 9
    
    bVectors = [self.bVec0, self.bVec1, self.bVec2]
    
    self.anMatrix = []
    self.anMatrix.append(allVectors[0])
    self.anMatrix.append(allVectors[1])
    self.anMatrix.append(allVectors[2])
    self.anMatrix.append([x + y for x, y in zip(allVectors[0], allVectors[1])])
    self.anMatrix.append([x - y for x, y in zip(allVectors[0], allVectors[1])])
    self.anMatrix.append([x + y for x, y in zip(allVectors[1], allVectors[2])])
    self.anMatrix.append([x - y for x, y in zip(allVectors[1], allVectors[2])])
    self.anMatrix.append([x + y for x, y in zip(allVectors[2], allVectors[0])])
    self.anMatrix.append([x - y for x, y in zip(allVectors[2], allVectors[0])])
    self.anMatrix.append([x + y + z for x, y, z in zip(allVectors[0], allVectors[1], allVectors[2])])
    self.anMatrix.append([x - y - z for x, y, z in zip(allVectors[0], allVectors[1], allVectors[2])])
    self.anMatrix.append([x + y - z for x, y, z in zip(allVectors[0], allVectors[1], allVectors[2])])
    self.anMatrix.append([x - y + z for x, y, z in zip(allVectors[0], allVectors[1], allVectors[2])])
    
    self.bnMatrix = []
    self.bnMatrix.append(bVectors[0])
    self.bnMatrix.append(bVectors[1])
    self.bnMatrix.append(bVectors[2])
    self.bnMatrix.append([x + y for x, y in zip(bVectors[0], bVectors[1])])
    self.bnMatrix.append([x - y for x, y in zip(bVectors[0], bVectors[1])])
    self.bnMatrix.append([x + y for x, y in zip(bVectors[1], bVectors[2])])
    self.bnMatrix.append([x - y for x, y in zip(bVectors[1], bVectors[2])])
    self.bnMatrix.append([x + y for x, y in zip(bVectors[2], bVectors[0])])
    self.bnMatrix.append([x - y for x, y in zip(bVectors[2], bVectors[0])])
    self.bnMatrix.append([x + y + z for x, y, z in zip(bVectors[0], bVectors[1], bVectors[2])])
    self.bnMatrix.append([x - y - z for x, y, z in zip(bVectors[0], bVectors[1], bVectors[2])])
    self.bnMatrix.append([x + y - z for x, y, z in zip(bVectors[0], bVectors[1], bVectors[2])])
    self.bnMatrix.append([x - y + z for x, y, z in zip(bVectors[0], bVectors[1], bVectors[2])])
         
    self.an2h = []
    self.bn2h = []
    for index in range(len(self.anMatrix)):
      self.an2h.append(0.5 * self.norm(self.anMatrix[index]))
      self.bn2h.append(0.5 * self.norm(self.bnMatrix[index]))
    
    #pprint(self.anMatrix)
    #pprint(self.an2h)
    
           
  def norm(self, a):
    return a[0]*a[0] + a[1]*a[1] + a[2]*a[2]
    
    
  def scalarProduct(self, a, b):
    return sum([elem1 * elem2 for elem1, elem2 in zip(a, b)])
    
  def crossProduct(self, a, b):
    # a.y * b.z - a.z * b.y
    firstComponent = a[1] * b[2] - a[2] * b[1]
    # a.z * b.x - a.x * b.z ,
    secondComponent = a[2] * b[0] - a[0] * b[2]
    # a.x * b.y - a.y * b.x
    thirdComponent = a[0] * b[1] - a[1] * b[0]
    return [ firstComponent, secondComponent, thirdComponent ]  
  
  
  def fold_in_ws(self, v):
    epsilon = 1.0e-10
    done = False
    maxIter = 10
    iterations = 0
    
    while not done and iterations < maxIter:
      done = True
      i = 0
      while i < 13 and done:
        sp = self.scalarProduct(v, self.anMatrix[i])
        if sp > self.an2h[i] + epsilon:
          done = False
          for index in range(len(self.anMatrix[i])):
            v[index] = v[index] - self.anMatrix[i][index]
          #v -= self.anMatrix[i]
          while self.scalarProduct(v, self.anMatrix[i]) > self.an2h[i] + epsilon :
            for index in range(len(self.anMatrix[i])):
              v[index] = v[index] - self.anMatrix[i][index]
        elif sp < -self.an2h[i] - epsilon:
          done = False
          for index in range(len(self.anMatrix[i])):
            v[index] = v[index] + self.anMatrix[i][index]
          #v -= self.anMatrix[i]
          while self.scalarProduct(v, self.anMatrix[i]) < -self.an2h[i] - epsilon :
            for index in range(len(self.anMatrix[i])):
              v[index] = v[index] + self.anMatrix[i][index]
        i += 1
      
      iterations += 1
    return v
    
  def getVolume(self):
    return self.volume
    
  def showStuff(self):
    print self.anMatrix
    #print self.volume
   
    

#uc = UnitCell([4.233416,0.000000,0.000000], [0.000000,4.233416,0.000000], [0.000000,0.000000,4.233416])
#uc.scalarProduct([1, 2, 2], [3, 5, 1])
#uc.showStuff()
#print(uc.fold_in_ws([0.635012,0.635012,-0.635012]))