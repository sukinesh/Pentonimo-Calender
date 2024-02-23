#!/usr/bin/python3
import sys
import itertools
import datetime

#grid = [[0,0,0,0,0,0,41],[0,0,0,0,0,0,41], [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,41,41,41,41] ]
grid = [[0,41,0,0,41,0,41],[41,0,41,41,0,0,41], [0,41,0,0,41,0,0],[0,0,41,41,0,0,0],[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,41,41,41,41] ]

def getStartPointInRow(row,sc):
    # print(row,sc)
    for column in range(7-(sc)):
        # print(column)
        try:
            if(grid[row][column+sc] == 0):
                # print('returning',[row,column+sc],'as start')
                return column+sc
        except:
            return 'impossible'

def gridChecker():
    holes = []

    def cellChecker(rowId, columnId):
        sideBlock =0 
        sides = [0,0,0,0]
        freeSide = [0,0]
        if (rowId    == 0 or grid[rowId-1][columnId] != 0 ): sides[0] =1
        else: freeSide = [rowId-1 , columnId]
        if (columnId == 0 or grid[rowId][columnId-1] != 0 ): sides[1] =1
        else: freeSide = [rowId , columnId-1]
        if (rowId    == 6 or grid[rowId+1][columnId] != 0 ): sides[2] =1
        else: freeSide = [rowId+1 , columnId]
        if (columnId == 6 or grid[rowId][columnId+1] != 0 ): sides[3] =1
        else: freeSide = [rowId , columnId+1]

        for cell in sides: sideBlock+=cell 
        
        return sideBlock, freeSide

    for rowId ,row in enumerate(grid):
        for columnId,cell in enumerate(row):
            if(cell == 0):
                sideBlock, freeSide = cellChecker(rowId, columnId)

                #if blocked 4 sides - hole
                if(sideBlock==4):
                    holes.append([rowId,columnId])
                #if 2 cells blocked 3 sides each - 2 holes
                elif(sideBlock==3):
                    blocks , otherSide = cellChecker(freeSide[0],freeSide[1])
                    if(blocks == 3): holes.append([rowId,columnId])
                    elif(blocks == 2): 
                        othersBlock = cellChecker(otherSide[0],otherSide[1])[0]
                        # print(othersBlock)
                        if(othersBlock == 3): 
                            holes.append([rowId,columnId])
                            if freeSide not in holes: holes.append(freeSide)

    # print(len(holes), ' holes')
    return holes

def holesInMonths(holes):
    inMonth = 0
    for hole in holes:
        if (hole[0] < 2):
            inMonth +=1
    
    return inMonth

def noHoleInMonths():
    for i in range(2):
        for j in range(7):
            if(grid[i][j]==0): return False
    return True

def getFilledDate(holes):
    monthPos = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5]]
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    month = months[monthPos.index(holes[0])]
    date = (holes[1][0]-2)*7 + (holes[1][1] + 1)
    print(month,' ',date)
    return f'{month}-{date}'
    

class Polyominoe:
    def __init__(self,name, shape, color,elementOffset):
        self.name  = name
        self.shape = shape
        self.color = color
        self.elementOffset = elementOffset

    def rotate(self):
        temp = self.shape
        self.shape = []
        for j in range(len(temp[0])):
            self.shape.append([None]*len(temp))
        for i in range(len(temp)):
            for j in range(len(temp[i])):
                self.shape[j][i] = temp[len(temp)-(i+1)][j]
        #print(temp,self.shape)        

    def flip(self):
        temp = self.shape
        self.shape = []
        for j in range(len(temp)):
            self.shape.append([None]*len(temp[0]))
        for i in range(len(temp)):
            for j in range(len(temp[i])):
                self.shape[i][j] = temp[i][len(temp[i])-(j+1)]
        #print(temp,self.shape)      

    def fitInGrid(self,start,transform):

        for t in transform:
            if (t == "f"):
                self.flip()
            elif (t == "r"):
                self.rotate()
                
        def fitter(fitted=0):
            # print(start)
            sr = start[0] 
            startColumn = getStartPointInRow(sr,start[1])
            while(startColumn == None):
                sr+=1
                start[0]=sr
                start[1]=0
                startColumn = getStartPointInRow(sr,0)
            if(startColumn == 'impossible'):
                return 'impossible'
            sc = startColumn
            if(sc != 0):
                sc += self.elementOffset
            # print(self.name,sr,sc,'start')            
            
            for row in range(len(self.shape)):
                for column in range(len(self.shape[0])):
                    try: 
                        # print(row+sr,column+sc,grid[row+sr][column+sc])
                        if(grid[row+sr][column+sc] == 0 or self.shape[row][column] == 0):
                            if(row+1 == len(self.shape) and column+1 == len(self.shape[0])):
                                fitted = 1
                        else:
                            # print("\033[1;31m Overlap \033[0m")
                            start[1]+=1
                            return [fitted,[sr,sc]]
                            
                    except IndexError as err:
                        # print(err)
                        start[0]+=1
                        start[1]=0
                        return [fitted,[sr,sc]]

            
            if(fitted == 1):
                for row in range(len(self.shape)):
                    for column in range(len(self.shape[0])):
                        if (self.shape[row][column] == 1):
                            grid[row+sr][column+sc] = self.color
            return [fitted,[sr,sc]]

        fitter_result = fitter()
        if(fitter_result == 'impossible'):  return 'impossible'
        while(fitter_result[0] == 0):
            # input()
            # start[0] = fitter_result[2][0]
            fitter_result = fitter(fitter_result[0])
            # print(fitter_result)
            if(fitter_result == 'impossible'):  return 'impossible'
        # print(fitter_result[1])
        return fitter_result[1]
        #print(grid) 


b = [
        Polyominoe('Br0' , [[1,0],[1,1],[1,1]]       , 34 , 0), #blue
        Polyominoe('Br1' , [[1,1,1],[1,1,0]]         , 34 , 0),
        Polyominoe('Br2' , [[1,1],[1,1],[0,1]]       , 34 , 0),
        Polyominoe('Br3' , [[0,1,1],[1,1,1]]         , 34 ,-1),
        Polyominoe('Bfr0', [[0,1],[1,1],[1,1]]       , 34 ,-1),
        Polyominoe('Bfr1', [[1,1,0],[1,1,1]]         , 34 , 0),
        Polyominoe('Bfr2', [[1,1],[1,1],[1,0]]       , 34 , 0),
        Polyominoe('Bfr3', [[1,1,1],[0,1,1]]         , 34 , 0)
    ]
c = [
        Polyominoe('Cr0', [[1,1],[1,0],[1,1]]       , 33 , 0), #yellow
        Polyominoe('Cr1', [[1,1,1],[1,0,1]]         , 33 , 0), 
        Polyominoe('Cr2', [[1,1],[0,1],[1,1]]       , 33 , 0), 
        Polyominoe('Cr3', [[1,0,1],[1,1,1]]         , 33 , 0)
    ]
f = [
        Polyominoe('Fr0',  [[1,1],[1,0],[1,0],[1,0]] , 32 , 0), #green
        Polyominoe('Fr1',  [[1,1,1,1],[0,0,0,1]]     , 32 , 0),
        Polyominoe('Fr2',  [[0,1],[0,1],[0,1],[1,1]] , 32 ,-1),
        Polyominoe('Fr3',  [[1,0,0,0],[1,1,1,1]]     , 32 , 0),
        Polyominoe('Ffr0', [[1,1],[0,1],[0,1],[0,1]] , 32 , 0),
        Polyominoe('Ffr1', [[0,0,0,1],[1,1,1,1]]     , 32 , 0),
        Polyominoe('Ffr2', [[1,0],[1,0],[1,0],[1,1]] , 32 , 0),
        Polyominoe('Ffr3', [[1,1,1,1],[1,0,0,0]]     , 32 , 0)
    ]
l = [   
        Polyominoe('Lr0', [[1,0,0],[1,0,0],[1,1,1]] , 36 , 0), #light blue
        Polyominoe('Lr1', [[1,1,1],[1,0,0],[1,0,0]] , 36 , 0),
        Polyominoe('Lr2', [[1,1,1],[0,0,1],[0,0,1]] , 36 , 0),
        Polyominoe('Lr3', [[0,0,1],[0,0,1],[1,1,1]] , 36 ,-2)
    ]
o = [
        Polyominoe('Or0', [[1,1],[1,1],[1,1]]      , 35 , 0), #pink
        Polyominoe('Or1', [[1,1,1],[1,1,1]]        , 35 , 0), 
    ]
s = [
        Polyominoe('Sr0', [[0,1,1],[0,1,0],[1,1,0]]  , 31 ,-1), #red
        Polyominoe('Sr1', [[1,0,0],[1,1,1],[0,0,1]]  , 31 , 0), 
        Polyominoe('Sfr0', [[1,1,0],[0,1,0],[0,1,1]] , 31 , 0), 
        Polyominoe('Sfr1', [[0,0,1],[1,1,1],[1,0,0]] , 31 ,-2), 
    ]
t = [
        Polyominoe('Tr0',  [[0,1],[1,1],[0,1],[0,1]] , 90 ,-1), #grey
        Polyominoe('Tr1',  [[0,0,1,0],[1,1,1,1]]     , 90 ,-2), 
        Polyominoe('Tr2',  [[1,0],[1,0],[1,1],[1,0]] , 90 , 0), 
        Polyominoe('Tr3',  [[1,1,1,1],[0,1,0,0]]     , 90 , 0), 
        Polyominoe('Tfr0', [[1,0],[1,1],[1,0],[1,0]] , 90 , 0), 
        Polyominoe('Tfr1', [[1,1,1,1],[0,0,1,0]]     , 90 , 0), 
        Polyominoe('Tfr2', [[0,1],[0,1],[1,1],[0,1]] , 90 ,-1), 
        Polyominoe('Tfr3', [[0,1,0,0],[1,1,1,1]]     , 90 ,-1)
    ]
z = [
        Polyominoe('zr0',  [[1,1,0,0],[0,1,1,1]]      , 37 , 0), #white
        Polyominoe('zr1',  [[0,1],[1,1],[1,0],[1,0]]  , 37 ,-1), 
        Polyominoe('zr2',  [[1,1,1,0],[0,0,1,1]]      , 37 , 0), 
        Polyominoe('zr3',  [[0,1],[0,1],[1,1],[1,0]]  , 37 ,-1), 
        Polyominoe('zrf0', [[0,0,1,1],[1,1,1,0]]      , 37 ,-2), 
        Polyominoe('zrf1', [[1,0],[1,0],[1,1],[0,1]]  , 37 , 0), 
        Polyominoe('zrf2', [[0,1,1,1],[1,1,0,0]]      , 37 ,-1), 
        Polyominoe('zrf3', [[1,0],[1,1],[0,1],[0,1]]  , 37 , 0)
    ]


def display():    
    for row in range(7):
        print("\033[40m",end="")
        for column in range(7): 
            if(grid[row][column] != 0):
                print(f"\033[1;{grid[row][column]}m",end="")
                print ('#',end=" ")
            else:
                print(" ", end =" ")    
        print("\033[0m")
    print("\033[0m"
    )
    

def arrangeTetrominos(currentOrder = ['c0', 't0', 'l1', 's1', 'f0', 'z6', 'b0', 'o1'] ):
    global grid
    grid = [[0,0,0,0,0,0,41],[0,0,0,0,0,0,41], [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,41,41,41,41] ] 
    nextStartPoint = [0,0]
    for i , name in enumerate(currentOrder):
        element = globals()[name[0]][int(name[1])] #enum in javascript
        nextStartPoint = element.fitInGrid(nextStartPoint,"")
        # print(element.name,nextStartPoint,'start point')
        # display()

        holes = gridChecker()
        # print(holes)

        if(nextStartPoint == 'impossible' or len(holes) > 2 or holesInMonths(holes)>1 or noHoleInMonths()):
            # print("\033[1;31m IMPOSSIBLE COMBO \033[0m")
            # display()
            if nextStartPoint == 'impossible' : return i-1
            return i


        # input()
    
    display()
    return i,holes


tetros = [b, c, f, l, o, s, t, z]

b0 = [ 'b0' , 'b1' , 'b2' , 'b3' , 'b4' , 'b5' , 'b6' , 'b7']
c0 = [ 'c0' , 'c1' , 'c2' , 'c3' ]
f0 = [ 'f0' , 'f1' , 'f2' , 'f3' , 'f4' , 'f5' , 'f6' , 'f7']
l0 = [ 'l0' , 'l1' , 'l2' , 'l3' ]
o0 = [ 'o0' , 'o1' ]
s0 = [ 's0' , 's1' , 's2' , 's3' ]
t0 = [ 't0' , 't1' , 't2' , 't3' , 't4' , 't5' , 't6' , 't7']
z0 = [ 'z0' , 'z1' , 'z2' , 'z3' , 'z4' , 'z5' , 'z6' , 'z7']

count = 0 
backStep = 0 
def permutations(elements =['c0', 't0', 'l1', 's1', 'f0', 'z6', 'b0', 'o1'], current_permutation = []):
    global count
    global backStep

    if len(elements) == 0:
        count+=1
        # print(count)
        arrangeResult = arrangeTetrominos(current_permutation) 
        if isinstance(arrangeResult, tuple) and len(arrangeResult) == 2:
            blocksFixed , holes = arrangeResult
        else:
            blocksFixed = arrangeResult
        # print(blocksFixed+1, ' blocks')
        backStep = 6 - blocksFixed
        # with open('output.txt', 'a') as f:
        #     f.write(f"{', '.join(current_permutation)} - {blocksFixed+1}\n")
        if(blocksFixed == 7):
            realDate = getFilledDate(holes)
            with open('success.txt', 'a') as f:
                f.write(f"{', '.join(current_permutation)} - {realDate}\n")
        # print(f"{', '.join(current_permutation)} - {blocksFixed+1}\n")
        # display()
        # input()
    else:
        for i in range(len(elements)):
            if(backStep>0): 
                backStep-=1
                return count
            new_permutation = current_permutation + [elements[i]]
            remaining_elements = elements[:i] + elements[i+1:]
            permutations(remaining_elements, new_permutation)

    return count
    

def Combinations():
    combinations = list(itertools.product(b0 , c0, f0, l0, o0, s0, t0, z0))
    for comb in combinations:
        # Check if each element in the permutation comes from a different array
        print(comb)
        with open('seq_list.txt', 'a') as f:
            f.write(f"{comb}\n")

def combFromFile():
    global count
    startTime = datetime.datetime.now()
    with open('combinations.txt', 'r') as file:
        combinations = file.readlines()
        for i in range(400000,524288):
            combination = combinations[i].strip().split(',')
            noOfPerm = permutations(combination)
            print(i, 'comb', noOfPerm,'perms')
            # with open('output.txt', 'a') as f:
            #     f.write(f"{combination} - {noOfPerm}\n")
            # print(f"{combination} - {noOfPerm}\n")
            count = 0


    endTime = datetime.datetime.now()
    processTime = endTime - startTime
    print(processTime)

def testTetroBlock():
    for tetro in z:
        global grid
        grid = [[0,0,0,0,0,0,41],[0,0,0,0,0,0,41], [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,41,41,41,41] ] 

        tetro.fitInGrid([0,0],"")
        display()

def testPerms():
    with open('test.txt', 'r') as file:
        perms = file.readlines()
        for i in range(0,6):
            current_permutation = perms[i].strip().split(',')
            arrangeResult = arrangeTetrominos(current_permutation) 

# testTetroBlock()
# Combinations()
combFromFile()
# print(arrangeTetrominos())
# permutations()
# gridChecker()
# getFilledDate([[1,3],[4,4]])
# testPerms()
# noHoleInMonths()
