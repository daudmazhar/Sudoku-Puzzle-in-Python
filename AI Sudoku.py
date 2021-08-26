#!/usr/bin/env python
# coding: utf-8

# In[8]:


import random
import copy
#Reading File
reader = open("board.txt", "r")
board = []
fixed = [] # has a 1 at the index of fixed numbers which should not be changed, other indexes are 0.

for x in reader:
    for y in x:
        if y != '\n':
            board.append(int(y))
            if y == '0':
                fixed.append(0)
            else:
                fixed.append(1)


# In[9]:


#Generate random population.
population = ([])
popSize = 1000

for total in range(popSize):
    temp = []
    for x in range(81):
        if board[x] == 0:
            temp.append(random.randint(1,9))
        else:
            temp.append(board[x])
    population.append(temp)


# In[10]:


#print board (prints a 1d board into 2d just for testing)
def printBoard(state):
    for x in range(9):
        for y in range(9):
            print(state[x*9 + y], end = " ")
        print(" ")


# In[11]:


#Fitness function.
def fitness(state):
    score = 0
    #count uniqe elements in rows(max = 81)
    for x in range(9):
        unique = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for y in range(9):
            index = state[x*9 + y] - 1
            if unique[index] == 0:
                score += 1
                unique[index] = 1
    #count unique elements in cols(max = 81)
    for x in range(9):
        unique = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for y in range(9):
            index = state[x + y*9] - 1
            if unique[index] == 0:
                score += 1
                unique[index] = 1
    #count unique elements in the 9 boxes(max = 81)
    for r in range (0, 7, 3):
        for z in range(0, 7, 3):
            unique = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for x in range(3):
                for y in range(3):
                    index = state[(x + r)*9 + y + z] - 1
                    if unique[index] == 0:
                        score += 1
                        unique[index] = 1
    return score
#Max score or score of solution = 243


# In[12]:


#Crossover function, switches 1 to 3 random squares between two parents. Suduko board has 9 squares. We dont need to care
#about fixed values here as only similarly positioned squares would be swapped.
squares = [0, 3, 6, 27, 30, 33, 54, 57, 60]
def Crossover(parents):
    for x in range(random.randint(1, 3)):
        chosenSquare = squares[random.randint(0, 8)]
        for x in range(3):
                for y in range(3):
                    temp = parents[0][chosenSquare + y + x*9]
                    parents[0][chosenSquare + y + x*9] = parents[1][chosenSquare + y + x*9]
                    parents[1][chosenSquare + y + x*9] = temp
    return parents


# In[13]:


def Crossover2(parents):
    for x in range(random.randint(1, 3)):
        index = random.randint(0, 80)
        temp = parents[0][index]
        parents[0][index] = parents[1][index]
        parents[1][index] = temp
    return parents


# In[14]:


#Making new population.
for generations in range(10000):
    newPopulation = ([])
    scores = []
   
    for x in population:
        scores.append((fitness(x), x))

    scores.sort()
    scores.reverse()
    
    print(f"=== Generation {generations} best solution score ====")
    print(scores[0][0])
    
    if scores[0][0] == 243:
        printBoard(scores[0][1])
        break
        
    #Selection of best 20% population (Start of making the new generation)
    #No randomness needed in this step, randomness will be applied in crossover and mutation.
    selectionRate = int(popSize * 0.20)
    for x in range(selectionRate):
        newPopulation.append(copy.deepcopy(scores[x][1]))
        
   
    #Crossover, Two random parents chosen from the old population to cross over and make children. 25%
    crossOverRate = int(popSize * 0.25) #we are adding two babies per iteration so 25% * 2 = 50%
    for x in range(crossOverRate):
        parents = ([])
        parents.append(scores[random.randint(0, 99)][1])# 1 parent is a top 100 parent
       # parents.append(population[random.randint(0, (popSize - 1))])
        parents.append(population[random.randint(0, (popSize - 1))]) # 1 parent is randomly selected from the entire population
        
        # here we have 2 options for crossOver function. Crossover swaps submatrices b/w parents & Crossover2 swaps single
        # random values b/w the 2 parents 
        
        babies = Crossover(parents)
        #babies = Crossover2(parents) 
        newPopulation.append(copy.deepcopy(babies[0]))
        newPopulation.append(copy.deepcopy(babies[1]))
   

    #Mutation, Randomly change the changeable values. 30%
    mutationRate = int(popSize * 0.30)  
    for x in range(mutationRate):
        abomination = population[random.randint(0, (popSize - 1))]
        for y in range(random.randint(1, 5)):  #upto 5 genes can mutate for each sample in the 30% of chosen population
            index = random.randint(0, 80) # random selection from the entire population
            if fixed[index] != 1: #if value is not fixed
                abomination[index] = random.randint(1, 9) 
        newPopulation.append(copy.deepcopy(abomination))
    
    population = newPopulation
    


# In[17]:


printBoard(population[0])


# In[18]:


print(fitness(population[0]))


# In[ ]:





# In[ ]:




