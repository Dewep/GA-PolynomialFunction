import random
import math
import plotly

# Best solution: [0.0007955062831871234, 5000.000066724238, 4.999999134503437, -61.999999996548524, 0.9999999999948588, -0.000999999999997464]  Fitness: 1.508722

# Polynomial Function settings
DATA_FILENAME    = "data.in"
SIZE_COEFFICIENT = 6
MIN_COEFFICIENT  = -1000.0
MAX_COEFFICIENT  = 1000.0

# Genetic Algorithm settings
POP_SIZE         = 500
NUMBER_OF_TURNS  = 2000
PROBA_CROSSOVER  = 0.90
PROBA_MUTATION   = 0.01
RATE_MUTATION    = 0.00001


# Fetching data
target_x = list()
target_y = list()

with open(DATA_FILENAME) as input_file:
    for line in input_file:
        numbers = line.strip().split()
        if len(numbers) == 2:
            target_x.append(float(numbers[0]))
            target_y.append(float(numbers[1]))


# Compute value from a X and a coefficients list
def compute_value(coefs, x):
    # In order to have faster computations, we preferred not to use our original function (which is 3 times slower).
    # -------------------
    # value = 0
    # for coef in range(SIZE_COEFFICIENT):
    #     value += coefs[coef] * x**coef
    # return value
    return coefs[0] + coefs[1] * x + coefs[2] * x**2 + coefs[3] * x**3 + coefs[4] * x**4 + coefs[5] * x**5


# Class for each Individual Solution
class IndividualSolution:
    def __init__(self, coefs):
        self.coefs = coefs
        self.fitness = 0
        for index in range(len(target_x)):
            self.fitness += abs(target_y[index] - compute_value(self.coefs, target_x[index]))

    def mutation(self):
        index = random.randint(0, SIZE_COEFFICIENT - 1)
        mutation_value = abs(RATE_MUTATION * self.coefs[index])
        if random.random() < 0.5:
            mutation_value *= -1
        self.coefs[index] += mutation_value

    def crossover(self, other): # linear crossover - Wright 1991
        coefs1, coefs2, coefs3 = [], [], []
        for index in range(SIZE_COEFFICIENT):
            coefs1.append(0.5 * self.coefs[index] + 0.5 * other.coefs[index])
            coefs2.append(1.5 * self.coefs[index] - 0.5 * other.coefs[index])
            coefs3.append(-0.5 * self.coefs[index] + 1.5 * other.coefs[index])
        childs = [IndividualSolution(coefs1), IndividualSolution(coefs2), IndividualSolution(coefs3)]
        return sorted(childs, key=lambda x: x.fitness)[:2]


# Breeding (Crossover + Mutation on 2 individuals)
def breeding(ind1, ind2):
    if random.random() < PROBA_CROSSOVER:
        ind1, ind2 = ind1.crossover(ind2)
    if random.random() < PROBA_MUTATION:
        ind1.mutation()
    if random.random() < PROBA_MUTATION:
        ind2.mutation()
    return ind1, ind2


# Generate the next population
def next_pop(pop):
    pop = sorted(pop, key=lambda x: x.fitness)
    new_pop = list()
    new_pop.append(pop[0])
    for i in range(math.floor(POP_SIZE / 2)):
        new_pop.extend(breeding(pop[i * 2], pop[i * 2 + 1]))
    return new_pop[:POP_SIZE]


# Generate a random solution
def random_solution():
    solution = list()
    for _ in range(SIZE_COEFFICIENT):
        solution.append(random.uniform(MIN_COEFFICIENT, MAX_COEFFICIENT))
    return solution


# Generate an initial random population
pop = [IndividualSolution(random_solution()) for _ in range(POP_SIZE)]

for turn in range(NUMBER_OF_TURNS):
    # Generate the next population
    pop = next_pop(pop)

    # Compute the fitness evolution
    # ...

    # ------------- DEBUG MESSAGE -------------
    if turn % (math.floor(NUMBER_OF_TURNS / 100)) == 0:
        print("%3d%%: %s  Fitness:%f" % (math.floor(turn / NUMBER_OF_TURNS * 100), str(pop[0].coefs), pop[0].fitness))
    # -----------------------------------------


# Selection of the best solution
best = pop[0]
print("\nBest solution: %s  Fitness: %f" % (best.coefs, best.fitness))


# Generation of the graphs

generated_x = list()
generated_y = list()
for index in range(len(target_x)):
    generated_x.append(target_x[index])
    generated_y.append(compute_value(best.coefs, target_x[index]))

plotly.offline.plot({
        "data": [
            plotly.graph_objs.Scatter(x=target_x, y=target_y, name='Target curve'),
            plotly.graph_objs.Scatter(x=generated_x, y=generated_y, name='Generated curve')
        ],
        "layout": {
            "title": "Reproduce a curve using a Genetic Algorithm",
            "xaxis": { "title": "x" },
            "yaxis": { "title": "y" }
        }
    },
    filename='compare-results.html')
