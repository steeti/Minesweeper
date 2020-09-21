from random import randint
path = os.getcwd()
rowsnumber=10
columnsnumber=10
mines=8
rd=64#row id
cd=64#col id
neighbours=[(-1,0),(1,0),(0,-1),(0,1),(-1,1),(-1,-1),(1,-1),(1,1)]
c=(rowsnumber*columnsnumber)-mines


def load_images():
    #function to load the images
    global covered, bomb, number
    
    # Load the image at start of the program
    covered = loadImage(path + "/data/uncovered.png")
    #print(path + "/data/uncovered.png")
    assert covered != None
    bomb = loadImage(path + "/data/bomb.png")
    assert bomb != None
    number = []
    for num in range(0, 9):
        location = path + "/data/" + str(num) + ".png"
        print("Loading image from: " + location)
        img = loadImage(location)
        assert img != None
        number.append(img)
    #creating array for the pictures and appending
    number.append(loadImage(path + "/data/uncovered.png"))
    number.append(loadImage(path + "/data/youwin.png"))
    number.append(loadImage(path + "/data/gameover.png"))


#a class to load the tiles
class Square:
    def __init__(self, row, col, val, con, image1):
        self.row = row
        self.col= col
        self.val= val
        self.con= con
        if (image1 == 10):
            self.image1 = bomb
        else:
            self.image1 = number[image1]
        print(len(number))
        self.image2 = number[9]
        print(path)
#the main class for the game
class Game:
    #parameters
    def __init__(self, rows, columns, mines):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.table = []
        self.tiles = []
        self.wining = "not win"
        self.losing = "not lose"
    #function to make the board
    def creatingtable(self):
        for a in range (self.rows):
            x = []
            for b in range(self.columns):
                x.append(" ")
            self.table.append(x)
    #function to assign the mines
    def assignmines(self):
        for x in range (self.mines):
            while True:
                randomvalue1=randint(0,rowsnumber-1)
                randomvalue2=randint(0,columnsnumber-1)
                if self.table[randomvalue1][randomvalue2]==" ":
                    self.table[randomvalue1][randomvalue2]="M"
                    break
    #function to assign the numbers
    def assignnumbers(self):
        for x in range (self.rows):
            for y in range(self.columns):
                if self.table[x][y]==" ":
                    cnt=0
                    for (a,b) in neighbours:
                        if (x+a>=0 and y+b>=0 and x+a<self.rows and y+b<self.columns):
                            if self.table[x+a][y+b]=="M":
                                cnt=cnt+1
                        self.table[x][y]=cnt
                        
    #function to assign the tiles
    def assigntiles(self):
        for a in range (self.rows):
            x = []
            for b in range(self.columns):
                if self.table[a][b]=="M":
                    # x.append(Square(a, b, "mine", "covered", "bomb.png"))
                    x.append(Square(a, b, "mine", "covered", 10))
                else:
                    # x.append(Square(a, b,self.table[a][b],"covered", str(self.table[a][b])+'.png'))
                     x.append(Square(a, b,self.table[a][b],"covered", self.table[a][b]))
                    
            self.tiles.append(x)
        
    #function to display the tiles    
    def displaytiles(self):    
        for a in range(self.rows):
            for b in range (self.columns):
                image(self.tiles[a][b].image1, self.tiles[a][b].row*rd,self.tiles[a][b].col*cd)
                if self.tiles[a][b].con == "covered":                                                  
                    image(self.tiles[a][b].image2, self.tiles[a][b].row*rd,self.tiles[a][b].col*cd)
            
    #the recursion function
    def recur(self, a,b):        
        if self.tiles[a][b].val == 0:
            for (d,c) in neighbours:
                if ((a+d) >= 0) and ((a+d) < self.rows) and ((b+c) >= 0) and ((b+c) < self.columns):
                    if self.tiles[a+d][b+c].con == "covered":
                        self.tiles[a+d][b+c].con = "uncovered"                                   
                        self.recur(a+d,b+c)
        else:
            return
    def revealEverything(self):
        for a in range(self.rows):
            for b in range (self.columns):
                image(self.tiles[a][b].image1, self.tiles[a][b].row*rd,self.tiles[a][b].col*cd)
        
    #condition checking function
    def checkcon(self, row, col):
        
        for a in range(self.rows):
            for b in range(self.columns):                                                      
                if self.tiles[a][b].val == "mine" and self.tiles[a][b].con == "notcovered":  
                    self.losing = "losing"
        if self.losing=="losing":
            self.revealEverything()
            image(number[11],300,300)
            noLoop()
        cc=0
        for a in range(self.rows):
            for b in range(self.columns):
                if self.tiles[a][b].con == "covered" and self.tiles[a][b].val != "mine":
                    cc=cc+1
        
        if cc == 0:
            self.wining = "wining"
        if self.wining == "wining":
            image(self.tiles[row][col].image1, row*rd, col*cd)
            image(number[10],300,300)
            
            noLoop()
    #the mouse click function
    def click(self):
        row = mouseX//rd
        col = mouseY//cd 
        for a in range(self.rows):
            for b in range(self.columns):
                if (self.tiles[a][b].row)  == row and self.tiles[a][b].col == col:
                    self.tiles[a][b].con = "notcovered"
                    self.recur(a,b)
        self.checkcon(row, col)
        
                            
y=Game(rowsnumber, columnsnumber, mines)
#processing set up and functions
def setup():
    load_images()
    y.creatingtable()
    y.assignmines()
    y.assignnumbers()
    y.assigntiles()
    print(y.tiles)
    print(y.table)
    size(rd*rowsnumber, cd*columnsnumber)
def draw():
    background(255)
    y.displaytiles()
    

def mouseClicked():
    y.click()

    
    
    
