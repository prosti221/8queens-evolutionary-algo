import numpy as np
from random import * 

#8x8 checkerboard grid.
DIM = 8

#8 queens, array of points for position of each queen
ideal_board = [[1, 2],
         [2, 4],
         [3, 6],
         [4, 8],
         [5, 3],
         [6, 1],
         [7, 7],
         [8, 5]]

#Place 8 queens so that none of them can threaten each other.
#no two queens can have the same x or y value, therby no linear threat.
#check there is no diagonal threat, such that abs(x_1 - x_2) = abs(y_1 - y_2)

#Define fitness as +100 for no linear threat for each queen
#                  +100 for no diagonal threat for each queen
#such that the optimal fitness is 5600 for when no queens threaten each other.

#returns a list of board states with 8 queens in them
def init(N):
    boards = []
    for i in range(N):
        points = {(randint(0, 7), randint(0, 7)) for i in range(8)}
        while len(points) < 8:
            points |= {(randint(0, 7), randint(0, 7))}
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
    index = randint(0, 7)
    del child[index]
    temp = {(point[0], point[1]) for point in child}
    while len(temp) < 8:
        temp |= {(randint(0, 7), randint(0, 7))}
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
        child = parents[parent1][:4] + parents[parent2][4:]
        if uniform(0.0, 100.0) > 95.0:
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
    if scores[0][1] == 5600:
        print('\nFound an ideal solution:\n')
        print(population[scores[0][0]])
        exit()



if __name__ == '__main__':
    pop = init(10000)
    for i in range(10000):
        population_stats(pop)
        parents = select_parents(pop, 1000)
        offspring = generate_offspring(parents, 9000)
        pop = evolve_population(parents, offspring)


