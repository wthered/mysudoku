# nma May 2020/ v0.1 #TODO / improve the strategy for forward move

import copy
import time

class State:
    theStates = []

    @staticmethod
    def moveForward():
        # produce next state and check if finished
        print('FORWARD MOVE number of states=', len(State.theStates))
        latestState = State.theStates[-1] # curent best state
        for nextItem in sorted(latestState.next.items()):
            # print(nextItem);
            newPosition = (nextItem[0], nextItem[1][0])
            # print("new position=", newPosition)
            State(newPosition = newPosition, sqBoard = latestState.sqBoard)
            return True
                # TODO improve strategy for next

    @staticmethod
    def backTrack():
        print('BAKCWORD MOVE ...', len(State.theStates))
        stateToRemove = State.theStates[-1]
        badPosition = stateToRemove.newPosition
        State.theStates.pop()
        del stateToRemove # remove the state that failed
        # and update the new last state
        lastState = State.theStates[-1]
        lastState.removeNext(badPosition) #we remove the candidate that failed
        lastState.checkImpossible()
        if not lastState.impossibleState: lastState.next = lastState.findNext()
        # print('the state of the last round is...', State.theStates[-1].impossibleState)

    def __init__(self, newPosition=None, sqBoard=[]):
        self.newPosition = newPosition
        self.sqBoard = copy.deepcopy(sqBoard) # take a copy of the 2-dimensional array sqBoard
        # print(self.sqBoard)
        if newPosition: self.addNew()
        self.defineCandidates()
        # print(self.theCandidates)
        if len(self.theCandidates)==0: self.winning = True
        else: self.winning = False
        self.checkImpossible()
        if not self.impossibleState: self.next = self.findNext()
        else: self.next = {}
        # print(self.next)
        State.theStates.append(self)
    
    def defineCandidates(self):
        self.theCandidates = {}
        for i in range(9):
            for j in range(9):
                if not self.sqBoard[i][j].isdigit():
                    self.theCandidates[(i,j)] = self.findCandidates(i,j)

    def findCandidates(self, x,y):
        myx, myy = x,y
        # print('findCandidates', x,y)
        # if self.sqBoard[x][y] != '-': return None
        candidates = '1 2 3 4 5 6 7 8 9'.split()
        # check line
        for i,value in enumerate(self.sqBoard[x]):
                # print(i,value)
                if i != y and self.sqBoard[x][i].isdigit():
                    if value in candidates: candidates.remove(value)
        # print('lines', x,y, candidates)
        # check column
        for i,line in enumerate(self.sqBoard):
            if i != x and line[y].isdigit():
                if line[y] in candidates: candidates.remove(line[y])
        # print('columns', x,y, candidates)
        #check 3x3 shell  /// DEBUG THIS 
        for i in range(x-x%3, x+2-x%3+1):
            for j in range(y-y%3, y+2-y%3+1):
                if not (i==myx and j==myy) and self.sqBoard[i][j].isdigit(): 
                    # if(i==0 and j==0): 
                        # print('value=', self.sqBoard[i][j])
                    if self.sqBoard[i][j] in candidates: 
                        candidates.remove(self.sqBoard[i][j])
                # print('incandidates', sqBoard[i][j], len(sqBoard[i][j]), sqBoard[i][j].isdigit(), i,j, candidates)
        # print('3x3 cells', x,y, candidates)
        # input()
        # print(candidates)
        # input()
        return candidates

    def addNew(self):
        self.sqBoard[self.newPosition[0][0]][self.newPosition[0][1]] = str(self.newPosition[1].strip())
        # print('added new item...', self.newPosition)
        self.validate()

    def validate(self):
        fault = False
        #check lines
        for i in range(9):
            theLine = [x for x in self.sqBoard[i] if x.isdigit()]
            if len(set(theLine)) != len(theLine): fault = True
        #check columns
        for j in range(9):
            theColumn = []
            for i in range(9):
                if self.sqBoard[j][i].isdigit(): theColumn.append(self.sqBoard[j][i])
            if len(set(theColumn)) != len(theColumn): fault = True
        #check 3x3 cells:
        for i in [0,3,6]:
            for j in [0,3,6]:
                theCell=[]
                for x in range(i, i+3):
                    for y in range(j, j+3):
                        if self.sqBoard[x][y].isdigit(): theCell.append(self.sqBoard[x][y])
                if len(set(theCell)) != len(theCell): fault = True
        if fault:
            print("FAULT", self.sqBoard)
            input()

    def removeNew(self):
        self.sqBoard[newPosition[0][0]][newPosition[0][1]] = "-"

    def checkImpossible(self):
        # print('CHECKING IMPOSSIBILITY', self.theCandidates)
        self.minLen = 0
        if self.theCandidates: 
            self.minLen = min([len(self.theCandidates[x]) for x in self.theCandidates])
        if self.minLen == 0: self.impossibleState = True
        else: self.impossibleState = False

    def removeNext(self, badPosition):
        # print('bad position=', badPosition)
        self.theCandidates[badPosition[0]].remove(badPosition[1])
        self.checkImpossible()
        # input()

    def findNext(self):
        if not self.theCandidates: return None
        theProbableNexts = {}
        for x,value in sorted(self.theCandidates.items()):
            if len(value) == self.minLen: theProbableNexts[x] = value
        return theProbableNexts

    def __repr__(self):
        print('current board state...')
        sym = {'nw': '┌', 'ne': '┐', 'sw': '└', 'se':'┘',
                    'side': '│', 'top': '─', 'cross': '┼',  
                    'bottom-x': '┴', 'top-x': '┬', 'e-x': '┤', 'w-x': '├'}
                    
        def drawRow(i):
            for cell in range(9):
                print(sym['side']+' '+self.sqBoard[i][cell]+' ', end='')
            print(sym['side'])
        def drawLine():
            print(sym['w-x'], end='')
            for cell in range(8):
                print(3*sym['top']+ sym['cross'], end='')
            print(3*sym['top']+sym['e-x'])

        for row in range(9):
            if row == 0: # top line
                print(sym['nw'], end='')
                for cell in range(8):
                    print(3*sym['top']+sym['top-x'], end='')
                print(3*sym['top']+sym['ne'])
                drawRow(row)
                drawLine()
            elif row == 8:  # bottom line
                drawRow(row)
                print(sym['sw'], end='')
                for cell in range(8):
                    print(3*sym['top']+sym['bottom-x'], end='')
                print(3*sym['top']+sym['se'])
            else:
                drawRow(row)
                drawLine()
        return ""

        # for line in self.sqBoard:
        #     for sq in line:
        #         toPrint = sq if sq != '-' else ' '
        #         print (toPrint, end = ' ')
        #     print()
        # if self.theCandidates: print(self.theCandidates)
        # if self.next:
        #     print("probable nexts are ... ")
        #     print(self.next)
        # if self.winning: return "WON"
        # else: return "NOT FINISHED YET"

######################### main #######################    

#content = input('δώσε περιεχόμενο χωρισμένο με κενά, - για άδεια τετράγωνα:')



# πολύ δύσκολο sudoku
content = '''- - 3 - 2 - - - 1
9 - - - - - - - -
- 7 - - - 5 - 8 6
- - 1 3 5 - - - -
- 2 - - - - - 1 -
- - - - 4 6 5 - -
4 3 - 8 - - - 9 -
- - - - - - - - 3
2 - - - 9 - 4 - -'''




# δύσκολο sudoku
content = '''- - 7 5 1 3 - 6 9
3 - 1 9 - - - - 7
6 - 9 7 - 4 1 3 -
4 - - 1 - 7 5 9 -
- 1 - - - - - 7 -
- 7 6 2 - - - - 1
- 9 - 8 7 - - 1 -
7 - - - - 1 9 - 8
1 6 8 - 9 5 7 - -'''

# world's hardest sudoku
content = '''8 - - - - - - - -
- - 3 6 - - - - -
- 7 - - 9 - 2 - -
- 5 - - - 7 - - -
- - - - 4 5 7 - -
- - - 1 - - - 3 -
- - 1 - - - - 6 8
- - 8 5 - - - 1 -
- 9 - - - - 4 - -'''


# εύκολο sudoku
content='''- 2 - 1 - - 7 4 -
- 3 - - - - 1 - 6
4 7 - - 9 6 - 5 -
- - 6 5 4 - - - 3
1 - - 9 - 8 - - 2
8 - - - 2 3 5 - -
- 8 - 7 5 - - 1 4
9 - 5 - - - - 8 -
- 6 4 - - 2 - 3 -'''

#kathimerini dyskolo #4 26-5-2020
content = '''- - 5 - 1 - - - 3
4 - - 6 - - 2 - -
- - 3 - 9 7 5 - -
7 - 6 - - - - - -
5 - - - - - - - 4
- - - - - - 8 - 9
- - 7 2 5 - 4 - -
- - 8 - - 1 - - 6
1 - - - 8 - 9 - -'''

board = content.split('\n')
sqBoard = []
for line in board:
    sqBoard.append(line.split())

start = time.perf_counter()
State(sqBoard=sqBoard)
print(State.theStates[-1])
movesCount = 0
while not State.theStates[-1].winning:
    if State.theStates[-1].impossibleState:
        State.backTrack()
    else: State.moveForward()
    print(State.theStates[-1])
    movesCount += 1
    # input()
print('after {} moves\n'.format(movesCount), 'time taken ....', time.perf_counter() - start)
