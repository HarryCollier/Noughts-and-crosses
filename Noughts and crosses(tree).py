import random
#-----------------------------
#Create node class
class node:
  def __init__(self, board, history):
    self.board = board
    self.history = history

  def printBoard(self):
    self.board.printBoard(self.board.board)


  def getChildren(self, player):
    children = []
    if player == 1:
      piece = "X"
    else:
      piece = "O"
    #Gets the children made when a moves are done on a node
    for action in self.board.getActions():
      tempB = self.board.decompBoard()
      for i in range(len(tempB)):
        if tempB[i][0] == action[0] and tempB[i][1] == action[1]:
          tempB[i][2] = piece

      b = board()
      b.recompBoard(tempB)
      if player == 2:
        children.append(node(b, self.history + [action]))
      else:
        children.append(node(b, self.history))
    return children








#-----------------------------
#Create frotier
class frontier:
  def __init__(self):
    self.frontier = []
    self.actions = []
    self.WLD = []

  def add(self, node):
    self.frontier.append(node)

  def addResultToRecord(self, node, result):
    if node.board.checkWin() != None:
      if node.history not in self.actions:
        self.actions.append(node.history)
        self.WLD.append([0, 0, 0])
      for i in range(len(self.actions)):
        if self.actions[i] == node.history:
            if result == 2:
              self.WLD[i][0] +=1
            elif result == 1:
              self.WLD[i][1] +=1
            else:
              self.WLD[i][2] +=1

  def remove(self):
    n = self.frontier[-1]
    self.frontier.pop(-1)
    return n

  def getBestMoveFromActions(self):
    moves = []
    WLDs = []
    for i in range(len(self.actions)):
      if self.actions[i][0] not in moves:
        moves.append(self.actions[i][0])
        WLDs.append(self.WLD[i])
      else:
        for j in range(len(moves)):
          if moves[j] == self.actions[i][0]:
            for k in range(3):
              WLDs[j][k] += self.WLD[i][k]

    bestM = moves[0]
    bestWLD = WLDs[0]
    for i in range(1, len(moves)):
      if WLDs[i][1] < bestWLD[1]:
        bestM = moves[i]
        bestWLD = WLDs[i]
      elif WLDs[i][1] == bestWLD[1]:
        if WLDs[i][2] < bestWLD[2]:
          bestM = moves[i]
          bestWLD = WLDs[i]
        elif WLDs[i][2] == bestWLD[2]:
          if WLDs[i][0] < bestWLD[0]:
            bestM = moves[i]
            bestWLD = WLDs[i]

    return bestM




  def solve(self):
    while len(self.frontier) != 0:
      node = self.remove()
      if node.board.checkWin() != None:
        result = node.board.checkWin()
        self.addResultToRecord(node, result)
      else:
        tempChildren = node.getChildren(2)
        for child in tempChildren:
          if child.board.checkWin() != None:
            self.add(child)
          else:
            tempChildren2 = child.getChildren(1)
            for child2 in tempChildren2:
              self.add(child2)
    return self.getBestMoveFromActions()




#------------------------------------------------------------
#Code to create a board class
class board:
  def __init__(self):
    self.board = [[" "," "," "],[" "," "," "],[" "," "," "]]

  def printBoard(self, board):
    for i in board:
      print(i[0] + "|" + i[1] + "|" + i[2])
    print("\n")

  def checkFull(self):
    valid = True
    for i in self.board:
      for j in i:
        if j == " ":
          valid = False
    return valid

  def makeMove(self, move, player):
    if player == 1:
      self.board[move[0]][move[1]] = "X"
    else:
      self.board[move[0]][move[1]] = "O"


  def checkPlayer(self, position):
    if self.board[position[0]][position[1]] == " ":
      return "False"
    elif self.board[position[0]][position[1]] == "X":
      return 1
    else:
      return 2

  def decompBoard(self):
    b = []
    for i in range(3):
      for j in range(3):
        b.append([i, j, self.board[i][j]])
    return b


  def recompBoard(self, board):
    for i in board:
        self.board[int(i[0])][int(i[1])] = i[2]

  def getActions(self):
    actions = []
    for i in range(3):
      for j in range(3):
        if self.board[i][j] == " ":
          actions.append([i, j])
    return actions

  def checkWin(self):

    for i in range(3):
      if self.board[i][0] == self.board[i][1] and self.board[i][0] == self.board[i][2] and self.board[i][0] != " ":
        return self.checkPlayer([i, 0])
      elif self.board[0][i] == self.board[1][i] and self.board[0][i] == self.board[2][i] and self.board[0][i] != " ":
        return self.checkPlayer([0, i])


    if self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2] and self.board[0][0] != " ":
      return self.checkPlayer([0,0])
    elif self.board[2][0] == self.board[1][1] and self.board[0][2] == self.board[2][0] and self.board[0][2] != " ":
      return self.checkPlayer([2,0])

    if self.checkFull():
      return "draw"


  def checkWinningMove(self, player):
    piece = ""
    if player == 1:
      piece = "X"
    else:
      piece = "O"
    for i in range(3):
      if self.board[i][0] == self.board[i][1] and self.board[i][0] == piece and self.board[i][2] == " ":
        return [i, 2]
      if self.board[i][0] == self.board[i][2] and self.board[i][0] == piece and self.board[i][1] == " ":
        return [i, 1]
      if self.board[i][1] == self.board[i][2] and self.board[i][1] == piece and self.board[i][0] == " ":
        return [i, 0]

    for j in range(3):
      if self.board[0][j] == self.board[1][j] and self.board[0][j] == piece and self.board[2][j] == " ":
        return [2, j]
      elif self.board[0][j] == self.board[2][j] and self.board[0][j] == piece and self.board[1][j] == " ":
        return [2, j]
      elif self.board[1][j] == self.board[2][j] and self.board[1][j] == piece and self.board[0][j] == " ":
        return [0, j]

    if self.board[0][0] == self.board[1][1] and self.board[0][0] == piece and self.board[2][2] == " ":
      return [2, 2]
    elif self.board[0][0] == self.board[2][2] and self.board[0][0] == piece and self.board[1][1] == " ":
      return [1, 1]
    elif self.board[1][1] == self.board[2][2] and self.board[2][2] == piece and self.board[0][0] == " ":
      return [0, 0]
    elif self.board[0][2] == self.board[1][1] and self.board[0][2] == piece and self.board[2][0] == " ":
      return [2, 0]
    elif self.board[0][2] == self.board[2][0] and self.board[0][2] == piece and self.board[1][1] == " ":
      return [1, 1]
    elif self.board[1][1] == self.board[2][0] and self.board[2][0] == piece and self.board[0][2] == " ":
      return [0, 2]


#-------------------------------------------------------
#Code to get moves
def getComputerMove(b):
  move = b.checkWinningMove(2)
  if move == None:
    move = b.checkWinningMove(1)
    if move == None:
      move = [0, -1]


  while move[1] == -1 or b.checkPlayer(move) != "False":
    b.printBoard(b.board)
    n = node(b, [])
    f = frontier()
    f.add(n)
    print("calculating move...")
    move = f.solve()
    print(move)
  return move



def getPlayerMove(b):
  pos1 = int(input("Enter the row you want to move to (1-3): ")) -1
  pos2 = int(input("Enter the column you want to move to (1-3): ")) -1
  while pos1 < 0 or pos1 > 2 or pos2 < 0 or pos2 > 2 or b.checkPlayer([pos1, pos2]) != "False":
    print("thats not a valid move")
    pos1 = int(input("Enter the row you want to move to (1-3): ")) -1
    pos2 = int(input("Enter the column you want to move to (1-3): ")) -1
  return [pos1, pos2]


#-------------------------------------------
#Actual code that runs
b = board()

while True:
  print("Starting")
  b.printBoard(b.board)

  b.makeMove(getPlayerMove(b), 1)
  if b.checkWin() == 1:
    b.printBoard(b.board)
    print("Player 1 wins!")
    break
  elif b.checkWin() == "draw":
    print("its a draw")
    break

  b.makeMove(getComputerMove(b), 2)
  if b.checkWin() == 2:
    b.printBoard(b.board)
    print("player 2 wins!")
    break
  elif b.checkWin() == "draw":
    print("its a draw")
    break