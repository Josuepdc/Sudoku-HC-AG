import re
import random
import os
from random import randint
from operator import itemgetter
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

# Cria um individuo
def individual(occupied,grid):
	length = 81
	valMin = 1
	valMax = 9

	i=0
	while(i < length):
		if(i in occupied):
			grid[i] = int(float(grid[i]))
			i=i+1
		else:
			grid[i] = randint(valMin,valMax)
			i=i+1

	return grid

# Cria populacao de individuos
def population(count, occupied,grid):
	
	i=0
	pop = []
	while(i < count):   
		cup = individual(occupied, grid)
		pop += [cup[:]]    
		i = i+1

	return pop

#Conta os elementos repetidos para a avaliacao das linhas, colunas e quadrados
def repeated(individual):

	point = 0
	x = []

	for i in individual:
		if i not in x:
			if individual.count(i) == 1:
				x.append(i)
				point = point+10
			if individual.count(i) == 2:
				x.append(i)
				point = point+9
			if individual.count(i) == 3:
				x.append(i)
				point = point+8
			if individual.count(i) == 4:
				x.append(i)
				point = point+7
			if individual.count(i) == 5:
				x.append(i)
				point = point+6
			if individual.count(i) == 6:
				x.append(i)
				point = point+5
			if individual.count(i) == 7:
				x.append(i)
				point = point+4
			if individual.count(i) == 8:
				x.append(i)
				point = point+3
			if individual.count(i) == 9:
				x.append(i)
				point = point+2

	return point

#Avalia as linhas
def avaliation_row(individual):
	
	i=0
	modulo=9
	point=0
	while(i < modulo):
		individualRow = individual[modulo*i:modulo*(i+1)]
		point += repeated(individualRow)
		i = i+1

	return point
		
#Avalia as colunas
def avaliation_column(individual):

	i=0
	j=0
	modulo=9
	listAval = []
	point=0
	finalPoint=0
	while(j < modulo):
		i=0
		listAval = []
		while(i < modulo):
			listAval += [individual[(modulo*i)+j]]
			i = i+1
		point = repeated(listAval)
		j = j+1
		finalPoint += point

	return finalPoint

#Avalia os quadrados
def avaliation_box(individual):

	i=0
	j=0
	k=0
	modulo=9
	lengh=3
	height=72
	point=0
	point2=0
	finalPoint=0
	listAval = []

	while(k < height):
		j=0
		listAval = []
		while(j < modulo):
			listAval = []
			i=0
			while(i < lengh):
				listAval += individual[(modulo*i)+j+k:((modulo*i)+3)+j+k]
				i = i+1
			j=j+3
			point += repeated(listAval)
		k=k+27
		finalPoint = point

	return finalPoint
		
# Avalia a pontuacao para cada individuo
def avaliation(individual):

	point = 0
	point += avaliation_row(individual)
	point += avaliation_column(individual) 
	point += avaliation_box(individual)  

	return point

# Avalia a pontuacao de todos os individuos da populacao, ordena o vetor da melhor para a pior pontuacao, tendo assim o melhor de sua geracao
def avaliation_population(population,sizePopulation,indice):

	i=0
	j=0
	bufferVal = []
	while(i<sizePopulation):
		point = avaliation(population[i])
		bufferVal += [[point, population[i]]] # Cria uma lista com o valor da avaliacao e o grid do individuo
		i = i+1        
	bufferVal.sort(reverse=True)
	bestResult = bufferVal[0]
	print ("Melhor resultado da geracao "+ str(indice)+": "+str(bestResult[0]))

	return bufferVal 

# Responsavel pelo cruzamento entre individuos
def cross(individual1, individual2, occupied):
	
	i=0
	tam=81
	
	j=randint(0,80)
	newIndividual1 = individual1[:j]+individual2[j:] 
	newIndividual2 = individual2[:j]+individual1[j:]   
	
	return [newIndividual1,newIndividual2]

# Roleta para a escolha dos individuos, onde aqueles com maior pontuacao tem uma maior chance de ser escolhidos.
def roleta(population,sizePopulation):
	sumPopulation=0
	i=0
	while(i<sizePopulation):
		sumPopulation += population[i][0]
		i=i+1
	
	j=0
	junda=0
	bufferRoleta = []
	while(j<sizePopulation):
		junda += (float(population[j][0])/sumPopulation)
		bufferRoleta.append(junda)
		j=j+1
	   
	randomVal = random.uniform(0.000000000001,0.99999999999)
	i=0
	while(i<len(bufferRoleta)):
		if(randomVal < bufferRoleta[i]):
			result=population[i][1]
			return result
		i=i+1

	return result

# Responsavel pelo cruzamento, define se tem elitismo, chama a roleta para fornecer os dois individuos para o cruzamento, chama o metodo de cruzamento e o metodo de mutacao, ao final criando uma nova populacao com o mesmo tamanho da anterior  
def crossover(population,probability,probabilityMutation,sizePopulation, occupied, elitism):
	randomVal = random.uniform(0.0000001, 1.0)    
	
	newPopulation = []
	if(elitism == "CE"):
		newPopulation.append(population[0][1])
		newPopulation.append(population[1][1])
		i=1
	
	else:
		i=0

	while(i<(sizePopulation/2)):
		individual1=roleta(population,sizePopulation)
		individual2=roleta(population,sizePopulation)
		if(randomVal < probability):
			newIndividual1 = cross(individual1, individual2,occupied)[0]
			newIndividual2 = cross(individual1, individual2,occupied)[1]
			newIndividual1 = mutation(newIndividual1,probabilityMutation,occupied)
			newIndividual2 = mutation(newIndividual2,probabilityMutation,occupied)
			
			newPopulation.append(newIndividual1)
			newPopulation.append(newIndividual2)
		else:
			newPopulation.append(individual1)
			newPopulation.append(individual2)
		i=i+1 
	return newPopulation

def mutation(individual,probability,occupied):
	randomVal = random.uniform(0.0000001, 1.0)
	  
	if(randomVal < probability):
		i=randint(0,80)
		if(i not in occupied):
			individual[i] = randint(1,9) 
		else:
			mutation(individual,probability,occupied)
	return individual

def main (): 
  sampleGridHard = ['.', '.', '.', '7', '.', '.', '.', '.', '.', '1', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '4', '3', '.', '2', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '6', '.', '.', '.', '5', '.', '9', '.', '.', '.', '.', '.', '.', '.', '.', '.', '4', '1', '8', '.', '.', '.', '.', '8', '1', '.', '.', '.', '.', '.', '2', '.', '.', '.', '.', '5', '.', '.', '4', '.', '.', '.', '.', '3', '.', '.']
  occupiedHard = [3,9,21,22,24,35,39,41,51,52,53,58,59,65,70,73,78] # lembrar que comeca em zero nao em um
  sampleGrid=sampleGridHard
  occupied=occupiedHard
  # exit()
  print ("Gerando populacao inicial . . .")
  print ("\n")
  pop = population(sizePopulation,occupied, sampleGrid)
   
  i=0

  print ("Avaliando populacao inicial . . .")
  print ("\n")
  aval = avaliation_population(pop,sizePopulation,i) 
  i=i+1
  
  print ("Iniciando AG . . .")
  print ("\n")
  
  while(i<generationNumber):
	pop = crossover(aval,crossProb,mutationProb,sizePopulation,occupied,elitism)
	aval = avaliation_population(pop,sizePopulation,i)
	i=i+1
  print("\nTabuleiro da geracao final . . .\n")
  printGrid(aval[0][1],0)
  print aval[0][1]

if len(sys.argv) < 5:
	print("Numero de argumentos insuficientes!")
	print("Por favor executar: game.py #individuos #geracoes crossProb mutationProb elitsm execnum")
	exit(0)
sizePopulation = int(sys.argv[1])
generationNumber = int(sys.argv[2])
crossProb = float(sys.argv[3])
mutationProb = float(sys.argv[4])
elitism = str(sys.argv[5])
execNum = str(sys.argv[6])
main()  
