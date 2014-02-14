import time

class Error(Exception):
	def __init__(self,errormsg):
		print errormsg

class Game(object):
	def __init__(self,GameState,PlayerList,ifprintgame=False,ifwait=False):
		self.State = GameState
		self.State.activePlayerList = PlayerList
		self.ifprintgame = ifprintgame
		self.ifwait = ifwait

	def printgame(self):
		pass

	def run(self):
		while True:
			for player in self.State.activePlayerList:
				ifEliminate = True
				for _ in xrange(3):
					if self.ifprintgame:
						move = self.State.nextMove(player,True) 
					else:
						move = self.State.nextMove(player) 
					if move is not False:
						if self.ifprintgame:
							# a = raw_input()
							self.printgame()
							print "------------------------------------------------------"
						if self.ifwait:
							a = raw_input("Enter to continue.")
						ifEliminate = False
						break
				if ifEliminate:
					self.State.activePlayerList.remove(player)
				if len(self.State.activePlayerList)==0:
					pass
					raise Error("You made a lot of invalid moves.")
				if self.State.checkState():
					if not self.ifprintgame:
						print self.printgame()
					print self.State.result
					return


class Player(object):
	def __init__(self,id):
		self.id = id

	def getMove(self,State,PlayerList=[]):
		# Return a state 
		pass

class State(object):

	def __init__(self,PlayerList,NumPlayers=0):
		self.numPlayers, self.StateRepresentation = self.init(NumPlayers) 
		if (len(PlayerList)!=self.numPlayers):
			raise Error("Desired number of players not supported.")
		self.PlayerList = PlayerList
		self.activePlayerList = []
		self.numMoves = 0
		self.result = "In Progress"
		self.winner = None

	def init(self,NumPlayers):
		# Set up the current state here
		# Return numPlayers, StateRepresentation
		pass

	def getState(self):
		return self.StateRepresentation

	def validMove(self,Move,Player):
		# Returns state if move valid, otherwise false
		pass

	def nextMove(self,Player,ifPrint=False):
		move = Player.getMove(self.StateRepresentation,self.PlayerList)
		nextState = self.validMove(move,Player)
		if nextState!=False:
			if ifPrint:
				print move
			self.StateRepresentation = nextState[0],nextState[1]
			self.numMoves += 1
			return True
		else :
			return False

	def checkState(self):
		# Returns true if game over, else return false
		pass

	def generateResult(self):
		# Generate a result at the end of the game
		return self.StateRepresentation