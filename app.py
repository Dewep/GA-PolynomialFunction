import random
import plotly
import plotly.graph_objs as go

tab_x = list()
tab_y = list()
real_tab_x = list()
real_tab_y = list()
level = 1
nb_turns = 100000000

with open("data.in") as input_file:
    for line in input_file:
        line = line.strip()
        numbers = line.split()
        if len(numbers) == 2:
            real_tab_x.append(float(numbers[0]))
            real_tab_y.append(float(numbers[1]))

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

def compute_value(coefs, x):
    return coefs[0] + coefs[1] * x + coefs[2] * x * x + coefs[3] * x * x * x + coefs[4] * x * x * x * x + coefs[5] * x * x * x * x * x


class solutionIndividual:
    def __init__(self, coefs):
        self.coefs = coefs
        self._fitness = 0
        self._mutation()
        self._compute_fitness()

    @property
    def fitness(self):
        return self._fitness

    def _compute_fitness(self):
        for index in range(len(tab_x)):
            self._fitness += abs(tab_y[index] - compute_value(self.coefs, tab_x[index]))

    def _mutation(self):
        if random.random() < 0.4:
            for index in range(len(self.coefs)):
                if random.random() < 0.4:
                    level_max = level * (len(self.coefs) - index)
                    self.coefs[index] += random.randint(-level, level)
                elif random.random() < 0.4:
                    self.coefs[index] *= -1

    def crossover(self, other):
        point = random.randint(0, len(self.coefs) - 1)
        genome1 = self.coefs[:point] + other.coefs[point:]
        genome2 = other.coefs[:point] + self.coefs[point:]
        child1 = solutionIndividual(genome1)
        child2 = solutionIndividual(genome2)
        return child1, child2

def next_pop(pop):
    pos = int(len(pop) / 2)
    pop = sorted(pop, key=lambda x: x.fitness)[:pos]
    best = pop[0]
    i = 0
    while i + 1 < pos:
        pop.extend(pop[i].crossover(pop[i + 1]))
        i += 2
    return best, pop


def random_solution():
    s = [0, 0, 0, 0, 0, 0]
    for index in range(len(s)):
        s[index] = random.randint(-level, level)
    return s

best = None
pop = [solutionIndividual(random_solution()) for _ in range(20)]
for _ in range(nb_turns):
    best, pop = next_pop(pop)

print(best.coefs)
print(best.fitness)

tab_x2 = list()
tab_y2 = list()
for index in range(len(tab_x)):
    tab_x2.append(tab_x[index])
    tab_y2.append(compute_value(best.coefs, tab_x[index]))

plotly.offline.plot([go.Scatter(x=tab_x, y=tab_y), go.Scatter(x=tab_x2, y=tab_y2)], filename='compare-results.html')
