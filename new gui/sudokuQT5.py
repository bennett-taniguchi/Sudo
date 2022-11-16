import sys

from PyQt5.QtGui import QIntValidator,QIcon
from PyQt5.QtWidgets import QGridLayout,QPushButton,QWidget,QLineEdit,QApplication, QMessageBox

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Sudoku Solver')
window.setWindowIcon(QIcon('Sudoku.png')) # Image Credit: https://www.pngegg.com/en/png-hycen

msg = QMessageBox()
msg.setWindowIcon(QIcon('Sudoku.png'))
msg.setWindowTitle("Tips")
msg.setText("Enter Sudoku puzzle into boxes, valid puzzles will be solved. Invalid will not run!")

msgError = QMessageBox()
msgError.setWindowIcon(QIcon('Sudoku.png'))
msgError.setWindowTitle("Error")
msgError.setText("Enter a Sudoku puzzle that is solvable. Duplicates in rows/columns/boxes are not solvable!")

layout = QGridLayout()
layout.setHorizontalSpacing(0)
layout.setVerticalSpacing(0)

window.setFixedHeight(900)
window.setFixedWidth(900)

layout.addWidget(QPushButton('Solve it!'), 10, 0)
layout.addWidget(QPushButton('More Info'), 10, 4)
layout.addWidget(QPushButton('Clear'), 10, 8)

butt = layout.itemAtPosition(10, 0).widget()
info = layout.itemAtPosition(10, 4).widget()
clear = layout.itemAtPosition(10, 8).widget()

buttonStyle = "QPushButton""{""background-color : lightblue;""}QPushButton::hover""{" "background-color : lavender;""}""QPushButton::pressed""{" "background-color : teal;""} "
butt.setStyleSheet(buttonStyle)
clear.setStyleSheet(buttonStyle)
info.setStyleSheet(buttonStyle)
layout.onlyInt = QIntValidator()

validator = QIntValidator(0,9,layout)
for x in range (9):
    for y in range (9):
        layout.addWidget(QLineEdit('0'), y+1, x)
        item = layout.itemAtPosition(y+1, x).widget()
        item.setTextMargins(49,0,10,20)
        item.setMaxLength(1)
        item.setValidator(validator)
        font = item.font()
        font.setPointSize(18)  
        item.setFont(font) 
        if(y in [2,5]):
            item.setStyleSheet("QLineEdit::hover"
                            "{"
                            "background-color : lightgreen;"                         
                            "}"
                            "QLineEdit"
                            "{"
                            "border-style: outset;"
                            "border-width: 10px;"
                            "border-color: beige;"
                            "border-bottom: 10px solid black;"
                            "}"
                            "")
            if(x in [2,5]):
                item.setStyleSheet("QLineEdit::hover"
                            "{"
                            "background-color : lightgreen;"                         
                            "}"
                            "QLineEdit"
                            "{"
                            "border-style: outset;"
                            "border-width: 10px;"
                            "border-color: beige;"
                            "border-bottom: 10px solid black;"
                            "border-right: 10px solid black;"
                            "}"
                            "")
        elif(x in [2,5]):
                item.setStyleSheet("QLineEdit::hover"
                            "{"
                            "background-color : lightgreen;"                         
                            "}"
                            "QLineEdit"
                            "{"
                            "border-style: outset;"
                            "border-width: 10px;"
                            "border-color: beige;"
                            
                            "border-right: 10px solid black;"
                            "}"
                            "")
        else: 
            item.setStyleSheet("QLineEdit::hover"
                            "{"
                            "background-color : lightgreen;"                         
                            "}"
                            "QLineEdit"
                            "{"
                            "border-style: outset;"
                            "border-width: 10px;"
                            "border-color: beige;"
                            "}"
                            "")

input  = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
]

def sendSudoku():
    for x in range (9):
        for y in range (9):       
            num = layout.itemAtPosition(1+y,x).widget().text()
            if (num == '' or num == ' '): num = 0 
            input[y][x] = int(num)
    if (not checkPuzzle(input)):
        errPopup()
    else:
        solve(input)
        refresh()
      
def refresh():
    for x in range (9):
        for y in range (9):       
            num = input[y][x]
            layout.itemAtPosition(1+y,x).widget().setText(str(num))

def reset():
    for x in range (9):
        for y in range (9):       
            layout.itemAtPosition(1+y,x).widget().setText('0')

def popup():
    x = msg.exec_()

def errPopup():
    x = msgError.exec_()

#################################################
# Sudoku Solving Logic

''' Checks tuple for non-zero duplicates'''
def checkArr(arr):
    found = []
    for x in arr:
        if(x not in found):
            found.append(x)
        elif(x in found and x != 0): return False
    return True

''' Checks rows/columns/boxes for non-zero duplicates'''
def checkPuzzle(b):
    for x in range(9):
        if(not checkArr(b[x])):
            return False

    cols=[]
    for x in range(9):
        if(len(cols) > 0):
            if(not checkArr(cols)): return False
            cols = []
        for y in range(9):
            cols.append(b[y][x])

    box = []
    row = [0,3,6]
    col = [0,3,6]
    for r in row:
        for c in col:
            if(len(box) > 0):
                if(not checkArr(box)): return False
                box = []
            for first in range(r, r+3):
                for second in range(c, c+3):
                    box.append(b[first][second])          
    return True

''' Resursively Backtracks to solve 0 spaces '''
def solve(b):
    empties = findEmpties(b)
    if not empties:
        return True

    else : x, y = empties

    for i in range(1,10):
        if(legalMove(i,(x,y),b)):
            b[x][y] = i
            if(solve(b)): return True   
            b[x][y] = 0
    return False

''' Ensures number placement follows Sudoku Rules '''
def legalMove(i, coords, b):
    # row
    if(i in b[coords[0]]): return False

    # col
    for x in range(len(b)):
        if b[x][coords[1]] == i: return False
            
    #box
    if(coords[0] in [0,1,2]): row = 0
    if(coords[0] in [3,4,5]): row = 3
    if(coords[0] in [6,7,8]): row = 6
    if(coords[1] in [0,1,2]): col = 0
    if(coords[1] in [3,4,5]): col = 3
    if(coords[1] in [6,7,8]): col = 6
    for a in range(row, row+3):
        for c in range(col, col+3):
            if(b[a][c] == i): return False

    return True

''' Ensures we Solve zero tiles only'''
def findEmpties(b):
    for x in range (0,9):
        for y in range(0,9):
            if (b[x][y] == 0): return (x,y)
    return None

#################################################
''' Top-Level Functionality '''

# Bind Buttons to Functions
butt.clicked.connect(sendSudoku)
clear.clicked.connect(reset)
info.clicked.connect(popup)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())

