from random import randint
import copy
import sys


def printGrid (grid, add_zeros):
  i = 0
  print '\n------+-------+-------+'
  for val in grid:
	if add_zeros == 1:
	  if int(val) < 10: 
		print '0'+str(val),
	  else:
		print val,
	else:
		print val,
	i +=1
	if i in [ (x*9)+3 for x in range(81)] +[ (x*9)+6 for x in range(81)] +[ (x*9)+9 for x in range(81)] :
		print '|',
	if add_zeros == 1:
	  if i in [ 27, 54, 81]:
		print '\n---------+----------+----------+'
	  elif i in [ (x*9) for x in range(81)]:
		print '\n'
	else:
	  if i in [ 27, 54, 81]:
		print '\n------+-------+-------+'
	  elif i in [ (x*9) for x in range(81)]:
		print '\n'
  print "\n"

def convertArrayToMatrix(array):
	matrix = [None]*9
	for i in xrange(0,9):
		matrix[i] = array[i*9:(i+1)*9]
	return matrix

def convertMatrixToArray(matrix):
	array = []
	for i in matrix:
		array += i
	return array	

def initial_state(problem):
	matrixOri = problem
	matrix = copy.deepcopy(matrixOri)

	for i in xrange(0,9):
		valuesToInsert = [1,2,3,4,5,6,7,8,9]
		for j in xrange(0,9):
			if matrixOri[j][i].isdigit():
				valuesToInsert.remove(int(matrixOri[j][i]))
		
		for j in xrange(0,9):
			if matrixOri[j][i] == '.':
				matrix[j][i] = valuesToInsert.pop(0)

	return matrix	

def max_neighbor(matrix, fixedposition):
	global coluna_ant

	maxneighbor = []
	matrixNei = copy.deepcopy(matrix)
	coluna = randint(0,8)
	
	while coluna_ant == coluna:
		coluna = randint(0,8)		
	coluna_ant = coluna	

	maxvalue = 0
	newvalue = 0

	for i in xrange(0,9):
		for j in xrange(i+1,9):
			if fixedposition.count((i*9)+coluna) == 0 and fixedposition.count((j*9)+coluna) == 0:		
				aux = matrixNei[i][coluna]
				matrixNei[i][coluna] = matrixNei[j][coluna]
				matrixNei[j][coluna] = aux
				newvalue = calculate(matrixNei)
				if maxvalue < newvalue:
					maxneighbor = copy.deepcopy(matrixNei)
					maxvalue = newvalue

				aux = matrixNei[i][coluna]
				matrixNei[i][coluna] = matrixNei[j][coluna]
				matrixNei[j][coluna] = aux

	return [maxneighbor, maxvalue]

def repeated(candidate):

	value = 0
	x = []

	for i in candidate:
		if i not in x:
			if candidate.count(i) == 1:
				x.append(i)
				value = value+10
			if candidate.count(i) == 2:
				x.append(i)
				value = value+9
			if candidate.count(i) == 3:
				x.append(i)
				value = value+8
			if candidate.count(i) == 4:
				x.append(i)
				value = value+7
			if candidate.count(i) == 5:
				x.append(i)
				value = value+6
			if candidate.count(i) == 6:
				x.append(i)
				value = value+5
			if candidate.count(i) == 7:
				x.append(i)
				value = value+4
			if candidate.count(i) == 8:
				x.append(i)
				value = value+3
			if candidate.count(i) == 9:
				x.append(i)
				value = value+2

	return value

#Avalia as linhas
def calculate_row(candidate):	
	value=0
	for i in range(0,9):
			box = []
			box += candidate[i][0:9] 
			value += repeated(box)
	return value
		
#Avalia os quadrados
def calculate_box(candidate):	
	value = 0
	for x in xrange(0,3):
		for i in range(0,3):
			box = []
			for j in range(0,3):
				linha = (3*x) + j
				coluna = (3*i)
				box += candidate[linha][coluna:coluna+3] 
			value += repeated(box)
	return value

# Avalia a pontuacao para cada individuo
def calculate(candidate):

	value = 0
	value += calculate_row(candidate)
	value += calculate_box(candidate)  

	return value


def hill_climbing(problem, fixedposition):
	global limit
	current = []
	neighbor = []
	current = initial_state(problem)
	count = 0

	while count < limit:
		[neighbor, neigvalue] = max_neighbor(current, fixedposition)

		if calculate(current) < neigvalue:
			current = neighbor

		count += 1

	print "=============="
	print "# iteracoes:"
	print limit
	print ""
	print "Melhor valor:"
	print calculate(current)
	print ""
	print "Tabuleiro:"
	printGrid(convertMatrixToArray(current),0)

	return current


coluna_ant = None
limit = int(sys.argv[1])

sampleGrid = [['.', '.', '.', '7', '.', '.', '.', '.', '.'], 
['1', '.', '.', '.', '.', '.', '.', '.', '.'], 
['.', '.', '.', '4', '3', '.', '2', '.', '.'], 
['.', '.', '.', '.', '.', '.', '.', '.', '6'], 
['.', '.', '.', '5', '.', '9', '.', '.', '.'], 
['.', '.', '.', '.', '.', '.', '4', '1', '8'], 
['.', '.', '.', '.', '8', '1', '.', '.', '.'], 
['.', '.', '2', '.', '.', '.', '.', '5', '.'], 
['.', '4', '.', '.', '.', '.', '3', '.', '.']]

occupied = [3,9,21,22,24,35,39,41,51,52,53,58,59,65,70,73,78] # lembrar que comeca em zero nao em um
hill_climbing(sampleGrid,occupied)
