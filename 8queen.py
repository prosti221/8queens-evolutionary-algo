import numpy as np
from random import * 

DIM = 8 #8x8 
MAX_SCORE = sum([200*n for n in range(1, DIM)])

def init(N):
    boards = []
    for i in range(N):
        points = {(randint(0, DIM-1), randint(0, DIM-1)) for i in range(DIM)}
        while len(points) < 8:
            points |= {(randint(0, DIM-1), randint(0, DIM-1))}
        points = list(list(x) for x in points)
        boards.append(points)
    return boards 

#returns list of fitness for current board
def fitness(board):
    score = 0
    for i in range(len(board) - 1):
        for j in range(i + 1, len(board)):
            if board[i][0] != board[j][0] and board[i][1] != board[j][1]:
                score = score + 100
            if abs(board[i][0] - board[j][0]) != abs(board[i][1] - board[j][1]):
                score = score + 100
    return score

def mutate(child):
    index = randint(0, DIM-1)
    del child[index]
    temp = {(point[0], point[1]) for point in child}
    while len(temp) < DIM:
        temp |= {(randint(0, DIM-1), randint(0, DIM-1))}
    temp = list(list(x) for x in temp)
    return temp 

def select_parents(population, N):
    scores = [(i, fitness(population[i])) for i in range(len(population))]
    scores = sorted(scores, reverse=True, key=lambda x: x[1])
    return [population[board[0]] for board in scores[:N]]

def evolve_population(parents, offspring):
    return parents + offspring


def generate_offspring(parents, N):
    offspring = []
    for i in range(N):
        parent1 = randint(0, len(parents)-1)
        parent2 = randint(0, len(parents)-1)
        child = parents[parent1][:DIM//2] + parents[parent2][DIM//2:]
        if uniform(0.0, 100.0) > 0.0: # This decides the probability of a mutation
            child = mutate(child)
        offspring.append(child)
    return offspring 

def population_stats(population):
    scores = [(i, fitness(population[i])) for i in range(len(population))]
    scores = sorted(scores, reverse=True, key=lambda x: x[1])
    avg_score = sum([x[1] for x in scores]) / len(scores)
    print('\nPopulation size: ' + str(len(scores)))
    print('\nHighest fitness score: ' + str(scores[0][1]))
    print('\nAverage fitness score: ' + str(avg_score))
    print('\n')
    if scores[0][1] == MAX_SCORE:
        print('\nFound an ideal solution:\n')
        print(population[scores[0][0]])
        exit()

if __name__ == '__main__':
    pop_size = 2000
    pop = init(pop_size)
    for i in range(10000):
        population_stats(pop) #This will terminate when a solution is found.
        parents = select_parents(pop, int(pop_size*0.1))
        offspring = generate_offspring(parents, int(pop_size*0.9))
        pop = evolve_population(parents, offspring)
