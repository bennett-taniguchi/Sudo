import sys
from PyQt6.QtCore import Qt
import math
from PyQt6.QtGui import *
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QWidget,
    QTableWidget,QTableWidgetItem, QGridLayout, QSpinBox
)

from PyQt6.QtWidgets import QApplication, QStyledItemDelegate, QWidget
from PyQt6.QtCore import Qt

'''
11/17

Current Issues:

Cells are turning into ints and viceversa, hard for cell validation and they turn into qspinboxes sometimes

Solved qspinbox issue, this is what happens when the qtablewidgetitem becomes an actual int

some boxes are 'sticky' and they stay after clearing or solvingnbn
'''

class CellDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        
        validator = QIntValidator(0,9,self)
        editor = QStyledItemDelegate.createEditor(self, parent, option, index)
        editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if(not isinstance(editor, QSpinBox) ):
            
            editor.setValidator(validator)
        return editor

class Window(QWidget):

    
    '''Display Internal Values on TableWidgets'''
    def displayValues(self):
        for a in range(3):
            
            for b in range(9):
                box = 3*a
                offset = b
 
                if(b in [1,4,7]):
                    offset -= 1
                    box += 1
                    
                elif(b in [2,5,8]):
                    offset -= 2
                    box += 2

                offset = math.floor(offset / 3)
                
                first = self.table[box].item(offset,0)    
                second = self.table[box].item(offset,1) 
                third = self.table[box].item(offset,2) 
                        
                if(None is not first and None is not second and None is not third):
                    col = 0
                    row = offset
                    if(box in [1,4,7]): col += 3

                    elif(box in [2,5,8]): col += 6

                    if(box in [3,4,5]): row += 3

                    elif(box in [6,7,8]): row += 6

                    first.setData(Qt.ItemDataRole.DisplayRole,str(self.b[row][col]))
                    second.setData(Qt.ItemDataRole.DisplayRole,str(self.b[row][col+1]))
                    third.setData(Qt.ItemDataRole.DisplayRole,str(self.b[row][col+2]))
                    

    ''' Resursively Backtracks to solve 0 spaces '''
    def solve(self):
        
        empties = self.findEmpties(self.b)
        if not empties:
            return True

        else : x, y = empties

        for i in range(1,10):
            if(self.legalMove(i,(x,y),self.b)):
                self.b[x][y] = i
                if(self.solve()): 
                    for x in range(9):
                        print(self.b[x])
                    print('')
                    self.displayValues()
                    return True   
                self.b[x][y] = 0
        return False

    ''' Ensures number placement follows Sudoku Rules '''
    def legalMove(self,i, coords, b):
        # row
        if(i in b[coords[0]]): return False

        # col
        for x in range(len(self.b)):
            if self.b[x][coords[1]] == i: return False
                
        #box
        if(coords[0] in [0,1,2]): row = 0
        if(coords[0] in [3,4,5]): row = 3
        if(coords[0] in [6,7,8]): row = 6
        if(coords[1] in [0,1,2]): col = 0
        if(coords[1] in [3,4,5]): col = 3
        if(coords[1] in [6,7,8]): col = 6
        for a in range(row, row+3):
            for c in range(col, col+3):
                if(self.b[a][c] == i): return False

        return True

    ''' Ensures we Solve zero tiles only'''
    def findEmpties(self,b):
        for x in range (0,9):
            for y in range(0,9):
                if (self.b[x][y] in [0,'0']): return (x,y)
        return None

    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Sudoku Solver")
        self.box = QGridLayout()
        self.makeGrid()
        self.setFixedSize(580,610)
        self.show()
        self.b = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],]

    def clearMatrix(self):
        for a in range(9):
            #print(a)
            for b in range(9):
                row = 0
                col = 0
                if(b < 3):
                    row = 0
                    col = b
                elif(b > 2 and b < 6):
                    row = 1
                    col = b-3
                else:
                    row = 2
                    col = b-6   

                cellUsed = self.table[a].item(row,col)          
                if(cellUsed is not None):
                    #print(cellUsed.type)
                    cellUsed.setData(Qt.ItemDataRole.DisplayRole,"0")
    def cellEntry(self):
        #print("clicked")
        box = int(self.sender().objectName())

        if (self.table[box].currentItem() is not None):
            col = int(self.table[box].currentItem().column())
            row = int(self.table[box].currentItem().row())
            data = int(self.table[box].item(row,col).text())
            
            
            if(box > 2 and box < 5):
                row += 3
            elif(box > 5):
                row += 6

            if(box in [1,4,7]):
                col += 3
            elif(box in [2,5,8]):
                col += 6
            print(self.b[row][col])
            self.b[row][col] = data
            
            
            
    def setupCell(self,x,table):
        
        for a in range(3):
            for b in range(3):
                table.setItem(a,b,QTableWidgetItem("0"))
                table.item(a,b).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
        table.setObjectName(str(x))
               
    def makeButtons(self):
        self.solveButton= QPushButton('Solve')
        self.clearButton= QPushButton('Clear')
        self.helpButton= QPushButton('Help')

        self.box.addWidget(self.solveButton,3,0)
        self.box.addWidget(self.clearButton,3,1)
        self.box.addWidget(self.helpButton,3,2)

        self.solveButton.clicked.connect(self.solve)
        self.clearButton.clicked.connect(self.clearMatrix)

    def makeGrid(self):
        self.cellDelegate = CellDelegate()
        self.table = [QTableWidget(3,3),QTableWidget(3,3),QTableWidget(3,3),QTableWidget(3,3),QTableWidget(3,3),QTableWidget(3,3),QTableWidget(3,3),QTableWidget(3,3),QTableWidget(3,3),]
        row = col = 0
        # self.focusNextPrevChild(True)
        # self.focus = QApplication.focusWidget()
        for x in range(9):
            
            self.table[x].setObjectName(str(x))

            self.setupCell(x,self.table[x])
            self.table[x].setItemDelegate(self.cellDelegate)
            self.table[x].verticalHeader().setVisible(False)
            self.table[x].horizontalHeader().setVisible(False)
            self.table[x].verticalHeader().setDefaultSectionSize(60)
            self.table[x].horizontalHeader().setDefaultSectionSize(60)
            self.table[x].clicked.connect(self.cellEntry)
            self.table[x].cellChanged.connect(self.cellEntry)
            
            self.box.addWidget(self.table[x],row,col)
            
            col+=1
            if(col == 3): 
                col = 0
                row += 1

        self.makeButtons()
        self.setLayout(self.box)

app = QApplication(sys.argv)

window = Window()
sys.exit(app.exec())

