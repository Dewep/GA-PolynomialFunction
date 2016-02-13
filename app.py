import random
import math
import plotly
import plotly.graph_objs as go

pop_size = 500
min_coefficient = -1000.0
max_coefficient = min_coefficient * -1
coefs_size = 6
proba_crossover = 0.85
proba_mutation = 0.0001
mutation_rate = 0.00001
nb_turns = 3000


tab_x = list()
tab_y = list()
real_tab_x = list()
real_tab_y = list()

with open("data.in") as input_file:
    for line in input_file:
        line = line.strip()
        numbers = line.split()
        if len(numbers) == 2:
            real_tab_x.append(float(numbers[0]))
            real_tab_y.append(float(numbers[1]))

tab_x = real_tab_x
tab_y = real_tab_y

"""
def find_average_y_value(x):
    for index in range(len(real_tab_x)):
        if real_tab_x[index] > x:
            if index > 0:
                return (real_tab_y[index - 1] + real_tab_y[index]) / 2
            return real_tab_y[index]
    return real_tab_y[-1]

x = -20
while x <= 900:
    tab_x.append(float(x))
    tab_y.append(float(find_average_y_value(x)))
    if x >= 650 and x <= 850:
        x += 3
    elif x >= 800:
        x += 7
    else:
        x += 50
"""

def compute_value(coefs, x):
    return coefs[0] + coefs[1] * x + coefs[2] * x * x + coefs[3] * x * x * x + coefs[4] * x * x * x * x + coefs[5] * x * x * x * x * x


class solutionIndividual:
    def __init__(self, coefs):
        self.coefs = coefs
        self._fitness = 0
        self._compute_fitness()

    @property
    def fitness(self):
        return self._fitness

    def _compute_fitness(self):
        self._fitness = 0
        for index in range(len(tab_x)):
            tmp = tab_y[index] - compute_value(self.coefs, tab_x[index])
            self._fitness += tmp * tmp
        self._fitness = math.sqrt(self._fitness)

    def mutation(self):
        index = random.randint(0, len(self.coefs) - 1)
        mutation_value = abs(mutation_rate * self.coefs[index])
        if random.random() < 0.5:
            mutation_value *= -1
        self.coefs[index] += mutation_value

    def crossover(self, other):
        coefs1 = list(self.coefs)
        coefs2 = list(self.coefs)
        coefs3 = list(self.coefs)
        for index in range(len(self.coefs)):
            coefs1[index] = 0.5 * self.coefs[index] + 0.5 * other.coefs[index]
            coefs2[index] = 1.5 * self.coefs[index] - 0.5 * other.coefs[index]
            coefs3[index] = -0.5 * self.coefs[index] + 1.5 * other.coefs[index]
        childs = [solutionIndividual(coefs1), solutionIndividual(coefs2), solutionIndividual(coefs3)]
        return sorted(childs, key=lambda x: x.fitness)[:2]

def breeding(ind1, ind2):
    if random.random() < proba_crossover:
        ind1, ind2 = ind1.crossover(ind2)
    if random.random() < proba_mutation:
        ind1.mutation()
    if random.random() < proba_mutation:
        ind2.mutation()
    return ind1, ind2

def next_pop(pop):
    pop = sorted(pop, key=lambda x: x.fitness)
    new_pop = list()
    new_pop.append(pop[0])
    for i in range(math.floor(pop_size / 2)):
        new_pop.extend(breeding(pop[i * 2], pop[i * 2 + 1]))
    return new_pop

def random_solution():
    s = list()
    for _ in range(coefs_size):
        s.append(random.uniform(min_coefficient, max_coefficient))
    return s

pop = [solutionIndividual(random_solution()) for _ in range(pop_size)]
for turn in range(nb_turns):
    if turn % (math.floor(nb_turns / 100)) == 0:
        print("%3d%%: %s %f" % (math.floor(turn / nb_turns * 100), str(pop[0].coefs), pop[0].fitness))
    pop = next_pop(pop)

best = pop[0]
print(best.coefs)
print(best.fitness)

tab_x2 = list()
tab_y2 = list()
for index in range(len(tab_x)):
    tab_x2.append(tab_x[index])
    tab_y2.append(compute_value(best.coefs, tab_x[index]))

plotly.offline.plot([go.Scatter(x=tab_x, y=tab_y), go.Scatter(x=tab_x2, y=tab_y2)], filename='compare-results.html')
