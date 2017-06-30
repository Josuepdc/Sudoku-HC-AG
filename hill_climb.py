from random import randint
import copy

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
	matrix = problem
	for i in xrange(0,9):
		x = 1
		for j in xrange(0,9):
			if matrix[j][i] == '.':
				matrix[j][i] = x
			else:
				a = int(matrix[j][i]) - 1
				matrix[j][i] = a + 1
				matrix[a][i] = x
			x+=1
	return matrix	
						

def getNeighbor(matrix, fixedposition):
	matrixNei = copy.deepcopy(matrix)
	coluna = randint(0,8)
	x1 = randint(0,8)
	x2 = randint(0,8)
	while x1 == x2:
		x1 = randint(0,8)
		x2 = randint(0,8)
	aux = matrixNei[x1][coluna]
	matrixNei[x1][coluna] = matrixNei[x2][coluna]
	matrixNei[x2][coluna] = aux
	return matrixNei

def neighbors(matrix, fixedposition):
	neighbors = []

	for i in xrange(0,9):
		for j in xrange(0,9):
			if matrix[j][i] == '.':
				x+=1

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
def calculate_row2(candidate):
	
	i=0
	modulo=9
	value=0
	while(i < modulo):
		candidateRow = candidate[modulo*i:modulo*(i+1)]
		value += repeated(candidateRow)
		i = i+1

	return value

def calculate_row(candidate):	
	value=0
	for i in range(0,9):
			box = []
			box += m[i][0:9] 
			value += repeated(box)
	return value
		
#Avalia os quadrados
def calculate_box2(candidate):

	i=0
	j=0
	k=0
	modulo=9
	lengh=3
	height=72
	value=0
	value2=0
	finalPoint=0
	listAval = []

	while(k < height):
		j=0
		listAval = []
		while(j < modulo):
			listAval = []
			i=0
			while(i < lengh):
				listAval += candidate[(modulo*i)+j+k:((modulo*i)+3)+j+k]
				i = i+1
			j=j+3
			value += repeated(listAval)
		k=k+27
		finalPoint = value

	return finalPoint

def calculate_box(candidate):	
	value = 0
	for x in xrange(0,3):
		for i in range(0,3):
			box = []
			for j in range(0,3):
				linha = (3*x) + j
				coluna = (3*i)
				box += m[linha][coluna:coluna+3] 
			value += repeated(box)
	return value

# Avalia a pontuacao para cada individuo
def calculate(candidate):

	value = 0
	value += calculate_row(candidate)
	value += calculate_box(candidate)  

	return value


def hill_climbing(problem):
	current = []
	neighbor = []
	current = initial_state(problem)
	count = 0

	while count < 1000:
		neighbor = getNeighbor(current)
		count2 = 0
		while calculate(convertMatrixToArray(current)) >= calculate(convertMatrixToArray(neighbor)) and count2 < 5000:
			neighbor = getNeighbor(current)
			count2 += 1

		current = neighbor
		count += 1

	return current

# sampleGrid = ['.', '.', '.', '7', '.', '.', '.', '.', '.', '1', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '4', '3', '.', '2', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '6', '.', '.', '.', '5', '.', '9', '.', '.', '.', '.', '.', '.', '.', '.', '.', '4', '1', '8', '.', '.', '.', '.', '8', '1', '.', '.', '.', '.', '.', '2', '.', '.', '.', '.', '5', '.', '.', '4', '.', '.', '.', '.', '3', '.', '.']
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
# print convertMatrixToArray(hill_climbing(sampleGrid))
# printGrid(convertMatrixToArray(hill_climbing(sampleGrid)),0)
m = initial_state(sampleGrid)
# printGrid(convertMatrixToArray(m),0)
print calculate_row(m)
print calculate_row2(convertMatrixToArray(m))