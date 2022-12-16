import sys,copy
from PyQt6.QtCore import (
    Qt,QModelIndex,QPoint
)
from PyQt6.QtTest import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QWidget,
    QTableWidget,QTableWidgetItem, QGridLayout, QSpinBox, QMessageBox,QStyleOptionViewItem, QSlider, QLabel, 
)
from PyQt6.QtWidgets import QApplication, QStyledItemDelegate, QWidget
from PyQt6.QtCore import Qt
 
'''Centers Text During Editing, Draws Sudoku Grid's Thick Lines'''
class borderDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        validator = QIntValidator(0,9,self)
        editor = QStyledItemDelegate.createEditor(self, parent, option, index)
        editor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if(not isinstance(editor, QSpinBox) ):
            editor.setValidator(validator)
        return editor

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        super().paint(painter, option, index)
        pen = QPen(QColor("black")) 
        pen.setWidth(2)
        painter.setPen(pen)
        offsetY = QPoint(0,0)
        offsetX = QPoint(0,0)
        if(index.row() in [2,5]):
            painter.drawLine(option.rect.bottomLeft()+offsetY,option.rect.bottomRight()+offsetY)
        if(index.row() in [3,6]):
            painter.drawLine(option.rect.topLeft()-offsetX, option.rect.topRight()-offsetX)
        if(index.column() in [2,5]):
            painter.drawLine(option.rect.topRight()+offsetX, option.rect.bottomRight()+offsetX)
        if(index.column() in [3,6]):
            painter.drawLine(option.rect.topLeft()-offsetY, option.rect.bottomLeft()-offsetY)
 
class Window(QWidget): 
    def __init__(self):

        sys.setrecursionlimit(10000)
        super(Window, self).__init__()
 
        self.currentRow = 0
        self.currentCol = 0
        self.setWindowTitle("Sudoku Solver")
        self.box = QGridLayout()
 
        self.makeGrid()
        
        self.setMinimumSize(580,650)
        self.open = False
        self.dialog = QMessageBox(self)
        self.dialog.setWindowTitle("SudokuSolver")
        self.dialog.setText("None")
        self.okay = (QMessageBox.StandardButton.Close)
 
        self.dialog.setStandardButtons(self.okay)
        
 
        self.show()
        self.b =    [[0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],]
                    
        self.saved = copy.deepcopy(self.b)
 
    '''Saves current grid'''
    def save(self):
        for x in range (9):
            for y in range (9):
                self.saved[x][y] = int(self.table.item(x,y).text())

    '''Updates Sudoku grid to previously 'saved' grid'''
    def clear(self):
        for x in range(9):
            for y in range(9):
                self.b[x][y] = self.saved[x][y]
                self.table.item(x, y).setBackground(QColor(250,250,250))
                self.table.item(x,y).setText(str(self.saved[x][y]))
    
    '''Zeroes out Sudoku grid'''
    def reset(self):
        for x in range(9):
            for y in range(9):
                self.b[x][y] = 0
                self.table.item(x, y).setBackground(QColor(250,250,250))
                self.table.item(x,y).setText(str(self.saved[x][y]))
 
 
    ''' Solving Methods '''
    def solve(self):
        if (self.checkDupes()):
            empties = self.findEmpties(self.b)
            QTest.qWait(self.slider.value())
            self.table.item(self.currentRow, self.currentCol).setBackground(QColor(250,250,250))
            self.refreshGrid()      

            if(self.table.item(self.currentRow,self.currentCol) is not None):
                self.table.item(self.currentRow, self.currentCol).setBackground(QColor(100,100,150))

            if not empties:
                return True
            else : x, y = empties
 
            for i in range(1,10):
                if(self.legalMove(i,(x,y),self.b)):
                    self.b[x][y] = i
                    
                    if(self.solve()): 
                        empties = self.findEmpties(self.b)
                        if empties: self.solve()

                        self.refreshGrid()
                        if(self.open == False): 
                            self.checkVictory()
                        return True   
                    self.b[x][y] = 0
            return False
 
    ''' Checks for zero spaces to solve '''
    def findEmpties(self, b):
        for x in range(9):
            for y in range(9):
                if (self.b[x][y] in [0,'0']): return (x,y)
        return None
 
    ''' Checks Grid for Duplicates in Row/Col/Box'''
    def checkArr(self,arr):
        found = []
        for x in arr:
            if(x not in found):
                found.append(x)
            elif(x in found and x not in [0,'0']): return False
        return True
 
    ''' See if move is legal within row, column, and box'''
    def legalMove(self, i, coords, b):
            row = coords[0]
            col = coords[1]
            if i in b[row] or i in [b[r][col] for r in range(9)] or i in [b[r][c] for r in range(row//3*3, row//3*3+3) for c in range(col//3*3, col//3*3+3)]:
                return False
            return True
 
    ''' Checks for duplicates, provides relevant popup message'''
    def checkDupes(self):
        #check row
        for x in range(9):
            if(not self.checkArr(self.b[x])):
                # err row 
                self.dialog.setText("Duplicate in row #" + str(x))
                self.dialog.open()
                return False
        #check col
        cols = []
        for x in range(9):
            if(len(cols) > 0):
                if(not self.checkArr(cols)): 
                    # err col
                    self.dialog.setText("Duplicate in col #" + str(x))
                    self.dialog.open()
                    return False
                cols = []
            for y in range(9):
                cols.append(self.b[y][x])
        #check box
        box = []
        row = [0,3,6]
        col = [0,3,6]
        for r in row:
            for c in col:
                for first in range(r, r+3):
                    for second in range(c, c+3):
                        box.append(self.b[first][second]) 
                if(len(box) > 0):
                    if(not self.checkArr(box)): 
                        boxNum = int(r + c/3)
                        self.dialog.setText("Duplicate in box #" + str(boxNum))
                        self.dialog.open()
                        return False
                    box = []
        return True
 
    '''Victory is reached if there are no empties and no duplicates'''
    def checkVictory(self):

        empties = self.findEmpties(self.b)

        if (self.checkDupes() and empties == None):
            self.dialog.setText("You won!")
            self.dialog.open()
            self.open = True
        self.open = False
 
    '''Stores coordinates of altered cell, calls check for victory condition'''
    def cellEntry(self):
        if(self.table.currentItem() is not None):
            row = self.table.currentRow()
            col = self.table.currentColumn()
            self.b[row][col] = int(self.table.item(row,col).text())
            self.checkVictory()
 
 
    '''Update current values on Grid'''
    def refreshGrid(self):
        for x in range(9):
            for y in range(9):
                 if(self.table.item(x,y).text() != str(self.b[x][y])):
                    self.table.item(x,y).setText(str(self.b[x][y]))
                    self.currentRow = x
                    self.currentCol = y

    '''Displays current delay for solving speed, for visualization purposes'''
    def updateSpeed(self):
        self.label.setText("Solving Delay (mS): " + str(self.slider.value()))

    '''Initializes buttons and connects to relevant functions'''
    def makeButtons(self):
        self.solveButton= QPushButton('Solve')        
        self.clearButton= QPushButton('Clear')
        self.helpButton= QPushButton('Help')
        self.resetButton = QPushButton('Reset')
 
        self.label = QLabel("Solving Delay (mS): 0")
        self.lockLabel = QLabel("Save Puzzle for Clear:")
        self.resetLabel = QLabel("Reset Puzzle to Blanks:")
 
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.lockButton = QPushButton('Lock')
 
        self.slider.sliderReleased.connect(self.updateSpeed)
 
        self.slider.setMaximumWidth(180)
        self.slider.setMinimum(0)
        self.slider.setMaximum(250)
        self.slider.setSingleStep(10)
 
        # row 1 widgets
        self.box.addWidget(self.solveButton,1,0)
        self.box.addWidget(self.clearButton,1,1)
        self.box.addWidget(self.helpButton,1,2)
 
        # row 2 widgets
        self.box.addWidget(self.label,2,0)
        self.box.addWidget(self.lockLabel,2,1)
        self.box.addWidget(self.resetLabel,2,2)
 
        # row 3 widgets
        self.box.addWidget(self.slider,3,0)
        self.box.addWidget(self.lockButton,3,1)
        self.box.addWidget(self.resetButton,3,2)
 
        self.lockButton.clicked.connect(self.save)
        self.solveButton.clicked.connect(self.solve)
        self.clearButton.clicked.connect(self.clear)
        self.resetButton.clicked.connect(self.reset)
 
    '''Initializes Grid with default colors, values, buttons and visibility settings'''
    def makeGrid(self):
        self.table = QTableWidget(9,9)
        self.table.setStyleSheet("gridline-color : black")
        self.cellDelegate = borderDelegate()
 
        for x in range(9):
            for y in range(9):
                self.table.setItem(x,y,QTableWidgetItem("0"))
                self.table.item(x,y).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setItemDelegate(self.cellDelegate)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.horizontalHeader().setDefaultSectionSize(60)
 
        self.table.cellChanged.connect(self.cellEntry)
        self.makeButtons()
        self.box.addWidget(self.table,0,0,1,3)
        self.setLayout(self.box)

app = QApplication(sys.argv)
 
window = Window()
sys.exit(app.exec())