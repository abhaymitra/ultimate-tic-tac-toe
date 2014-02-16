import random
import game
import time
from timeout import timeout,timer
import argparse
import os

# Not to be included in the distribution
parser = argparse.ArgumentParser()
parser.add_argument("outfile",help="File where the output needs to be stored.")
args = parser.parse_args()

timeP2 = [300,0]

# Returns true if Player has won the smaller Tic-Tac-Toe board at I,J.
def ifSmallWin(State,I,J,Player):
	def orfunc(x,y):	return x or y
	def andfunc(x,y):	return x and y
	horizontalwin = reduce(orfunc, [True if reduce(andfunc,[True if State[0][I][J][i][j]==Player else False for j in xrange(3)]) else False for i in xrange(3)])
	verticalwin = reduce(orfunc, [True if reduce(andfunc,[True if State[0][I][J][j][i]==Player else False for j in xrange(3)]) else False for i in xrange(3)])
	diagonal1win = reduce(andfunc, [ True if State[0][I][J][i][i]==Player else False for i in xrange(3)])
	diagonal2win = reduce(andfunc, [ True if State[0][I][J][2-i][i]==Player else False for i in xrange(3)])
	return horizontalwin or diagonal1win or verticalwin or diagonal2win


# Returns true if there exists empty positions on the smaller board at I,J.
def checkEmpty(State,I,J):
	return reduce((lambda x,y : x or y), [True if (State[0][I][J][i][j]==None) else False for i in xrange(3) for j in xrange(3)])


class AIPlayer(game.Player):
	def __init__(self,id):
		super(AIPlayer, self).__init__(id)


	# Code your solution here. Your function should return a tuple I,J,i,j. 
	# Here, I,J are the row and column number of the bigger Tic Tac Toe board and i,j of the smaller board at position I,J.
	# State[0][I][J][i][j] stores the Player at that board position if any, else None.
	# State[1] is a 2-tuple (I,J) indicating the board position the last player sent the current player to.
	# @timeout(timeP2)
	def getMove(self,State,PlayerList=[]):
		pass



class ManualPlayer(game.Player):
	def __init__(self,id):
		super(ManualPlayer, self).__init__(id)

	
	def getMove(self,State,PlayerList=[]):
		move = input()
		if len(move) == 4:
			return move
		else:
			raise Error("Move should be of type I,J,i,j.")	

class RandomPlayer(game.Player):
	def __init__(self,id):
		super(RandomPlayer, self).__init__(id)

	def getMove(self,State,PlayerList=[]):
		I,J = State[1]
		if not reduce(lambda x,y : x or y, [True if ifSmallWin(State,I,J,player) else False for player in PlayerList]) and checkEmpty(State,I,J):
			while True:
				i,j  = random.randint(0,2), random.randint(0,2)
				if State[0][I][J][i][j] == None:
					return I,J,i,j
		else:
			for x,y in [(I,J) for I in xrange(3) for J in xrange(3)]:
				if not reduce(lambda x,y : x or y, [True if ifSmallWin(State,x,y,player) else False for player in PlayerList]) and checkEmpty(State,x,y):
					while True:
						i,j  = random.randint(0,2), random.randint(0,2)
						if State[0][x][y][i][j] == None:
							return x,y,i,j				



class TicTacToeGame(game.Game):
	def __init__(self,GameState,PlayerList,ifprintgame=False,ifWait=False):
		super(TicTacToeGame,self).__init__(GameState,PlayerList,ifprintgame,ifWait)

	def printgame(self):
		def getname(list):
			def getid(x):
				if x==None:
					return "N"
				else:
					return str(x.id)
			return str(map(getid, list))

		for i in xrange(3):
			for k in xrange(3):
				print getname(self.State.StateRepresentation[0][i][0][k]) + "\t" + getname(self.State.StateRepresentation[0][i][1][k]) + "\t" + getname(self.State.StateRepresentation[0][i][2][k])
			print ""


class State(game.State):
	def __init__(self,PlayerList,NumPlayers=0):
		super(State,self).__init__(PlayerList,NumPlayers)
		self.won = [[None for _ in xrange(3)] for _ in xrange(3)]
		self.moves = []


	def init(self,NumPlayers):
		# [I][J] gives the smaller tic tac toe. [_][_][i][j] gives the player at i,j. None if none present.
		gameBoard,currentTicTacToe = [[[[None,None,None] for _ in xrange(3)] for _ in xrange(3) ] for _ in xrange(3)],(0,0)
		if(NumPlayers==2):
			return 2,(gameBoard,currentTicTacToe)
		else:
			return -1,(gameBoard,currentTicTacToe)


	def checkEmpty(self,I,J):
		return reduce((lambda x,y : x or y), [True if (self.StateRepresentation[0][I][J][i][j]==None) else False for i in xrange(3) for j in xrange(3)])
		
	# Returns true if game over, else return false
	def ifSmallWin(self,I,J,Player):
		def orfunc(x,y):	return x or y
		def andfunc(x,y):	return x and y
		horizontalwin = reduce(orfunc, [True if reduce(andfunc,[True if self.StateRepresentation[0][I][J][i][j]==Player else False for j in xrange(3)]) else False for i in xrange(3)])
		verticalwin = reduce(orfunc, [True if reduce(andfunc,[True if self.StateRepresentation[0][I][J][j][i]==Player else False for j in xrange(3)]) else False for i in xrange(3)])
		diagonal1win = reduce(andfunc, [ True if self.StateRepresentation[0][I][J][i][i]==Player else False for i in xrange(3)])
		diagonal2win = reduce(andfunc, [ True if self.StateRepresentation[0][I][J][2-i][i]==Player else False for i in xrange(3)])
		return horizontalwin or diagonal1win or verticalwin or diagonal2win


	# Returns true if move valid, otherwise false
	def validMove(self,Move,Player):
		if Move is None:
			return False

		
		for index in Move:
			if (index<0 or index>2):
				return False
		
		I,J,i,j = Move
		
		def constructState(self):
			self.StateRepresentation[0][I][J][i][j] = Player
			# print str(i) + "," + str(j) + "\t" + str(I) + "," + str(J) 
			return (self.StateRepresentation[0],(i,j))
		
		if (self.numMoves==0):
			self.moves.append(str(I) +str(J) + str(i) + str(j))
			return constructState(self)
		else:
			if self.StateRepresentation[1] != (I,J) :	
				if reduce(lambda x,y : x or y, [True if self.ifSmallWin(self.StateRepresentation[1][0],self.StateRepresentation[1][1],player) else False for player in self.PlayerList]) or not checkEmpty(self.StateRepresentation,self.StateRepresentation[1][0],self.StateRepresentation[1][1]):
					if self.StateRepresentation[0][I][J][i][j] == None  :
						self.moves.append(str(I) +str(J) + str(i) + str(j))
						return constructState(self)
					else:
						return False
				else:
					return False
			else:
				if self.StateRepresentation[0][I][J][i][j] == None :
					self.moves.append(str(I) +str(J) + str(i) + str(j))
					return constructState(self)
				else:
					return False


	def checkState(self):
		
		for I,J in [(x,y) for x in xrange(3) for y in xrange(3)]:
			for player in self.PlayerList:
				if ifSmallWin(self.StateRepresentation, I, J, player) and self.won[I][J]==None:
					self.won[I][J] = player
					if player.id == 1 :
						self.moves.append(str(I) + str(J) + "XX")
					elif player.id == 2:
						self.moves.append(str(I) + str(J) + "00")

		for I in xrange(3):
			if reduce(lambda x,y:x and y,[True if self.won[I][J]==self.won[I][0] else False for J in xrange(3)]) == True and self.won[I][0]!=None:
				self.result = "Player " + str(self.won[I][0].id) + " won by completing row number " + str(I)
				self.winner = self.won[I][0]
				return True

		for I in xrange(3):
			if reduce(lambda x,y:x and y,[True if self.won[J][I]==self.won[0][I] else False for J in xrange(3)]) == True and self.won[0][I]!=None:
				self.result = "Player " + str(self.won[0][I].id) + " won by completing column number " + str(I)
				self.won[0][I]
				return True		


		if self.won[0][0] == self.won[1][1] == self.won[2][2] and self.won[0][0] != None:
			self.result = "Player " + str(self.won[0][0].id) + " won by completing the major diagonal"
			self.winner = self.won[0][0].id
			return True
		elif self.won[2][0] == self.won[1][1] == self.won[0][2] and self.won[1][1] != None:
			self.result = "Player " + str(self.won[1][1].id) + " won by completing the minor diagonal"
			self.winner = self.won[1][1].id
			return True


		if (reduce(lambda x,y:x and y, [True if reduce(lambda x,y : x or y, [True if self.ifSmallWin(I,J,player) else False for player in self.PlayerList]) or not checkEmpty(self.StateRepresentation,I,J) else False for I in xrange(3) for J in xrange(3)])):
			self.result =  "Its a tie."
			return True

		return False




P1 = RandomPlayer(1)
P2 = RandomPlayer(2)

P3 = ManualPlayer(2)

P4 = AIPlayer(2)

State = State([P1,P2],2)

# Change the third argument to True to print the gamestate after every move.
# Change the fourth argument to True to wait for keyboard input to move to the next state.
# Press enter to advance the game by two moves.
Game = TicTacToeGame(State, [P1,P2],False,False)

Game.run()

with open(os.getcwd() + "/"+ args.outfile,'w') as outfile:
	for i in xrange(len(Game.State.moves) - 1):
		outfile.write(Game.State.moves[i] + ",")
	outfile.write(Game.State.moves[len(Game.State.moves)-1])

