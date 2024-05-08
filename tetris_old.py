#!/usr/bin/python3
import sys
import itertools
import datetime

grid = [[0,0,0,0,0,0,1],[0,0,0,0,0,0,1], [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,1,1,1,1] ]
mPo = [0,0]
dPo = [2,0]
# grid = [[0,1,0,0,1,0,1],[1,0,1,1,0,0,1], [0,1,0,0,1,0,0],[0,0,1,1,0,0,0],[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,1,1,1,1] ]

def getStartPointInRow(row,sc):
    print(row,sc)
    for column in range(7-(sc)):
        # print(column)
        try:
            if(grid[row][column+sc] == 0):
                # print('returning',[row,column+sc],'as start')
                return column+sc
        except:
            return 'impossible'


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

def gridChecker():
    holes = []


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

def gridHasHoles(startPoint):
    # print("start point is ",startPoint)

    for rowId ,row in enumerate(grid):
        for columnId,cell in enumerate(row):
            if(cell == 0):
                if(rowId<startPoint[0]):
                    # print('0 bfr start row')
                    return True
                elif(rowId == startPoint[0] and columnId < startPoint[1]):
                    # print('0 bfr start column')
                    return True

                sideBlock, freeSide = cellChecker(rowId, columnId)

                #if blocked 4 sides - hole
                if(sideBlock==4):
                    return True
                #if 2 cells blocked 3 sides each - 2 holes
                elif(sideBlock==3):
                    blocks , otherSide = cellChecker(freeSide[0],freeSide[1])
                    if(blocks == 3): return True
                    elif(blocks == 2): 
                        othersBlock = cellChecker(otherSide[0],otherSide[1])[0]
                        # print(othersBlock)
                        if(othersBlock == 3): 
                            return True
                            if freeSide not in holes: holes.append(freeSide)

    return False

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

# def getHolesOfDate(month,date):
#     monthPos = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5]]
#     mPo = monthPos[month - 1]
#     dPo = [date/7, date - date/7]
#     return mPO, dPo

    

class Polyominoe:
    def __init__(self,name, shape, color,elementOffset):
        self.name  = name
        self.shape = shape
        self.color = color
        self.elementOffset = elementOffset

    # def rotate(self):
    #     temp = self.shape
    #     self.shape = []
    #     for j in range(len(temp[0])):
    #         self.shape.append([None]*len(temp))
    #     for i in range(len(temp)):
    #         for j in range(len(temp[i])):
    #             self.shape[j][i] = temp[len(temp)-(i+1)][j]
    #     #print(temp,self.shape)        

    # def flip(self):
    #     temp = self.shape
    #     self.shape = []
    #     for j in range(len(temp)):
    #         self.shape.append([None]*len(temp[0]))
    #     for i in range(len(temp)):
    #         for j in range(len(temp[i])):
    #             self.shape[i][j] = temp[i][len(temp[i])-(j+1)]
    #     #print(temp,self.shape)      

    def fitInGrid(self,start,transform):

        # for t in transform:
        #     if (t == "f"):
        #         self.flip()
        #     elif (t == "r"):
        #         self.rotate()
        
        def fitter(fitted=0):
            # print(start)
            sr = start[0]
            # sc = start[1]
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
                            # print("\033[1;45m Overlap \033[0m")
                            start[1]+=1
                            return fitted
                            
                    except IndexError as err:
                        # print(err)
                        start[0]+=1
                        start[1]=0
                        return fitted

            
            if(fitted == 1):
                for row in range(len(self.shape)):
                    for column in range(len(self.shape[0])):
                        if (self.shape[row][column] == 1):
                            grid[row+sr][column+sc] = self.color
            return fitted

        fitter_result = fitter()
        # print(fitter_result)
        if(fitter_result == 'impossible'):  return 'impossible'
        while(fitter_result == 0):
            fitter_result = fitter(0)
            # print(fitter_result)
            if(fitter_result == 'impossible'):  return 'impossible'
        # print(fitter_result[1])

        startColumn = getStartPointInRow(start[0],start[1])
        while(startColumn == None):
            start[0]+= 1
            start[1]=0
            startColumn = getStartPointInRow(start[0],0)
        if(startColumn == 'impossible'):
            return 'nomorestart'
        return [start[0],startColumn]
        #print(grid) 


b = [
        Polyominoe('Br0' , [[1,0],[1,1],[1,1]]       , 40 , 0), #blue
        Polyominoe('Br1' , [[1,1,1],[1,1,0]]         , 40 , 0),
        Polyominoe('Br2' , [[1,1],[1,1],[0,1]]       , 40 , 0),
        Polyominoe('Br3' , [[0,1,1],[1,1,1]]         , 40 ,-1),
        Polyominoe('Bfr0', [[0,1],[1,1],[1,1]]       , 40 ,-1),
        Polyominoe('Bfr1', [[1,1,0],[1,1,1]]         , 40 , 0),
        Polyominoe('Bfr2', [[1,1],[1,1],[1,0]]       , 40 , 0),
        Polyominoe('Bfr3', [[1,1,1],[0,1,1]]         , 40 , 0)
    ]
c = [
        Polyominoe('Cr0', [[1,1],[1,0],[1,1]]       , 41 , 0), #yellow
        Polyominoe('Cr1', [[1,1,1],[1,0,1]]         , 41 , 0), 
        Polyominoe('Cr2', [[1,1],[0,1],[1,1]]       , 41 , 0), 
        Polyominoe('Cr3', [[1,0,1],[1,1,1]]         , 41 , 0)
    ]
f = [
        Polyominoe('Fr0',  [[1,1],[1,0],[1,0],[1,0]] , 42 , 0), #green
        Polyominoe('Fr1',  [[1,1,1,1],[0,0,0,1]]     , 42 , 0),
        Polyominoe('Fr2',  [[0,1],[0,1],[0,1],[1,1]] , 42 ,-1),
        Polyominoe('Fr3',  [[1,0,0,0],[1,1,1,1]]     , 42 , 0),
        Polyominoe('Ffr0', [[1,1],[0,1],[0,1],[0,1]] , 42 , 0),
        Polyominoe('Ffr1', [[0,0,0,1],[1,1,1,1]]     , 42 , 0),
        Polyominoe('Ffr2', [[1,0],[1,0],[1,0],[1,1]] , 42 , 0),
        Polyominoe('Ffr3', [[1,1,1,1],[1,0,0,0]]     , 42 , 0)
    ]
l = [   
        Polyominoe('Lr0', [[1,0,0],[1,0,0],[1,1,1]] , 43 , 0), #light blue
        Polyominoe('Lr1', [[1,1,1],[1,0,0],[1,0,0]] , 43 , 0),
        Polyominoe('Lr2', [[1,1,1],[0,0,1],[0,0,1]] , 43 , 0),
        Polyominoe('Lr3', [[0,0,1],[0,0,1],[1,1,1]] , 43 ,-2)
    ]
o = [
        Polyominoe('Or0', [[1,1],[1,1],[1,1]]      , 44 , 0), #pink
        Polyominoe('Or1', [[1,1,1],[1,1,1]]        , 44 , 0), 
    ]
s = [
        Polyominoe('Sr0', [[0,1,1],[0,1,0],[1,1,0]]  , 45 ,-1), #red
        Polyominoe('Sr1', [[1,0,0],[1,1,1],[0,0,1]]  , 45 , 0), 
        Polyominoe('Sfr0', [[1,1,0],[0,1,0],[0,1,1]] , 45 , 0), 
        Polyominoe('Sfr1', [[0,0,1],[1,1,1],[1,0,0]] , 45 ,-2), 
    ]
t = [
        Polyominoe('Tr0',  [[0,1],[1,1],[0,1],[0,1]] , 46 ,-1), #grey
        Polyominoe('Tr1',  [[0,0,1,0],[1,1,1,1]]     , 46 ,-2), 
        Polyominoe('Tr2',  [[1,0],[1,0],[1,1],[1,0]] , 46 , 0), 
        Polyominoe('Tr3',  [[1,1,1,1],[0,1,0,0]]     , 46 , 0), 
        Polyominoe('Tfr0', [[1,0],[1,1],[1,0],[1,0]] , 46 , 0), 
        Polyominoe('Tfr1', [[1,1,1,1],[0,0,1,0]]     , 46 , 0), 
        Polyominoe('Tfr2', [[0,1],[0,1],[1,1],[0,1]] , 46 ,-1), 
        Polyominoe('Tfr3', [[0,1,0,0],[1,1,1,1]]     , 46 ,-1)
    ]
z = [
        Polyominoe('zr0',  [[1,1,0,0],[0,1,1,1]]      , 47 , 0), #white
        Polyominoe('zr1',  [[0,1],[1,1],[1,0],[1,0]]  , 47 ,-1), 
        Polyominoe('zr2',  [[1,1,1,0],[0,0,1,1]]      , 47 , 0), 
        Polyominoe('zr3',  [[0,1],[0,1],[1,1],[1,0]]  , 47 ,-1), 
        Polyominoe('zrf0', [[0,0,1,1],[1,1,1,0]]      , 47 ,-2), 
        Polyominoe('zrf1', [[1,0],[1,0],[1,1],[0,1]]  , 47 , 0), 
        Polyominoe('zrf2', [[0,1,1,1],[1,1,0,0]]      , 47 ,-1), 
        Polyominoe('zrf3', [[1,0],[1,1],[0,1],[0,1]]  , 47 , 0)
    ]


def display():    
    for row in range(7):
        # print("\033[40m",end="")
        for column in range(7): 
            if(grid[row][column] != 0):
                print(f"\033[1;{grid[row][column]}m",end="")
                if(grid[row][column] == 1):
                    print ('#',end=" ")
                else:
                    print(' ',end=" ")
                # print("\033[0m",end="")
            else:
                # print(f"\033[40m",end="")
                print(" ", end =" ")  
            # print (' ',end=" ")
            print("\033[0m",end="")
        print("\033[0m")
    print("\033[0m")
    

def arrangeTetrominos(currentOrder = ['z6', 'b3', 't7', 'f4', 'c1', 'l0', 'o1', 's0']):
# def arrangeTetrominos(currentOrder = ['t0', 'f1', 'b1', 'z1', 's0', 'c3', 'l3', 'o1']):
    global grid
    grid = [[0,0,0,0,0,0,1],[0,0,0,0,0,0,1], [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,1,1,1,1] ] 

    if(mPo != None and dPo != None):
        grid[mPo[0]][mPo[1]] = 1
        grid[dPo[0]][dPo[1]] = 1

    nextStartPoint = [0,0]
    for i , name in enumerate(currentOrder):
        element = globals()[name[0]][int(name[1])] #enum in javascript
        nextStartPoint = element.fitInGrid(nextStartPoint,"")
        # print(element.name,nextStartPoint,'start point')
        # print(i)
        # display()
        print(nextStartPoint)
        # print('--------------------')

        #if testing for any date
        # holes = gridChecker()
        # print(holes)
        # if(nextStartPoint == 'impossible' or len(holes) > 2 or holesInMonths(holes)>1 or noHoleInMonths()):
        #     # print("\033[1;45m IMPOSSIBLE COMBO \033[0m")
        #     # display()
        #     if nextStartPoint == 'impossible' : return i-1
        #     return i

        #if arranging for specific date
        # if(nextStartPoint == 'impossible'): print('impossible')
        # if(gridHasHoles(nextStartPoint)): print('holes')
        if(nextStartPoint == 'impossible' ):
            return i-1
        elif(nextStartPoint == "nomorestart"):
            break
        else:
            if(gridHasHoles(nextStartPoint)):
                # display()
                return i


        # input()
    
    display()
    # print('success')
    # testing all dates
    # return i,holes

    # specific date 
    return i


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
def permutations(elements =['b3', 'c1', 'f4', 'l0', 'o1', 's0', 't7', 'z6'], current_permutation = []):
    global count
    global backStep

    if len(elements) == 0:
        count+=1
        print(current_permutation)

        #all dates 
        # arrangeResult = arrangeTetrominos(current_permutation) 
        # if isinstance(arrangeResult, tuple) and len(arrangeResult) == 2:
        #     blocksFixed , holes = arrangeResult
        # else:
        #     blocksFixed = arrangeResult

        # specific date
        blocksFixed = arrangeTetrominos(current_permutation) 

        # print(blocksFixed+1, ' blocks')
        backStep = 6 - blocksFixed
        # with open('output.txt', 'a') as f:
        #     f.write(f"{', '.join(current_permutation)} - {blocksFixed+1}\n")
        if(blocksFixed == 7):
            realDate = getFilledDate([mPo,dPo])
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

    # return count
    

def Combinations():
    global count
    combinations = list(itertools.product(b0 , c0, f0, l0, o0, s0, t0, z0))
    for comb in combinations:
        permutations(comb)
        print(comb,' - ',count)
        count = 0
        # with open('seq_list.txt', 'a') as f:
        #     f.write(f"{comb}\n")
        # input()

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
        grid = [[0,0,0,0,0,0,1],[0,0,0,0,0,0,1], [0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0], [0,0,0,0,0,0,0], [0,0,0,1,1,1,1] ] 

        tetro.fitInGrid([0,0],"")
        display()

def testPerms():
    with open('test.txt', 'r') as file:
        perms = file.readlines()
        for i in range(0,6):
            current_permutation = perms[i].strip().split(',')
            arrangeResult = arrangeTetrominos(current_permutation) 

def getSolutionForDate(month,date):
    global mPo, dPo
    monthPos = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5]]
    mPo = monthPos[month - 1]
    dPo = [date//7+2, date%7-1]
    print(mPo, dPo)

    # grid[mPo[0]][mPo[1]]=1
    # grid[dPo[0]][dPo[1]]=1
    print(grid)
    display()
    Combinations()


def testOutputFile():
    with open('success.txt', 'r') as file:
        results = file.readlines()
        for order in results:
            print(order.split('-')[0].strip().split(', '))
            arrangeTetrominos(order.split('-')[0].strip().split(', '))



# testTetroBlock()
# Combinations()
# combFromFile()
# permutations()
# gridChecker()
# getFilledDate([[1,3],[4,4]])
# testPerms()
# noHoleInMonths()
# getSolutionForDate(1,1)
print(arrangeTetrominos())
# testOutputFile()
