#Imports
import numpy as np
from copy import deepcopy

## Best way to find difference in genes is square all numbers first, then summing all values.
def get_diff_in_genes(gene):
    total = 0

    for i in gene:
        total += i*i

    return total


#Create problem
class problem:
    def __init__(self):
        self.number_of_genes = 8
        self.min_value = -10
        self.max_value = 10
        self.cost_function = get_diff_in_genes
        self.acceptable_cost = 0.000001
        pass


#Get Chromosome
class individual:
    def __init__(self, prob):
        self.chromosome = np.random.uniform(prob.min_value, prob.max_value, prob.number_of_genes)
        self.cost = prob.cost_function(self.chromosome)

    def mutate(self, rate_of_mutation, range_of_mutation):
        for index in range(len(self.chromosome)):
            if np.random.uniform() < rate_of_mutation:
                self.chromosome[index] += (np.random.randn() * range_of_mutation)

    def crossover(self, parent2, explore_crossover):
        alpha = np.random.uniform(-explore_crossover, 1+explore_crossover)
        child1 = deepcopy(self)
        child2 = deepcopy(parent2)

        child1.chromosome = alpha * self.chromosome + (1-alpha)*parent2.chromosome
        child2.chromosome = alpha * parent2.chromosome + (1-alpha)*self.chromosome
        
        return child1, child2


class parameters:
    def __init__(self):
        self.population = 1000
        self.explore_crossover_range = 0.2
        self.rate_of_gene_mutation = 0.2
        self.range_of_gene_mutation = 1
        self.birthrate_per_generation = 1
        self.max_num_of_generations = 1000

    def choose_parents(self, population_size):
        index1 = np.random.randint(0, population_size)
        index2 = np.random.randint(0, population_size)

        if index1 == index2:
            return parameters.choose_parents(self, population_size)

        return index1, index2


##Run problem and create 2 chromosomes
prob = problem()
params = parameters()

i1 = individual(prob)
print("Parent 1: \nChromosome -", i1.chromosome, "\nCost -", i1.cost)
print()

i2 = individual(prob)
print("Parent 2: \nChromosome -", i2.chromosome, "\nCost -", i2.cost)
print()


def run_genetic(prob, params):
    #Read variables
    population_size = params.population
    explore_crossover = params.explore_crossover_range
    gene_mutate_rate = params.rate_of_gene_mutation
    gene_mutate_range = params.range_of_gene_mutation
    cost_function = prob.cost_function
    num_of_children_per_generation = population_size * params.birthrate_per_generation
    max_num_of_generations = params.max_num_of_generations
    acceptable_cost = prob.acceptable_cost

    #Create population
    population = []
    best_solution = individual(prob)
    best_solution.cost = np.inf

    for i in range(population_size):
        new_individual = individual(prob)

        if new_individual.cost < best_solution.cost:
            best_solution = deepcopy(new_individual)

        population.append(new_individual)

    #Start loop
    for i in range(max_num_of_generations):

        children = []

        while (len(children) < num_of_children_per_generation):
            #Choose parents
            parent1_index, parent2_index = params.choose_parents(population_size)

            parent1 = population[parent1_index]
            parent2 = population[parent2_index]


            #Create children
            child1, child2 = parent1.crossover(parent2, explore_crossover)

            child1.mutate(gene_mutate_rate, gene_mutate_range)
            child2.mutate(gene_mutate_rate, gene_mutate_range)

            child1.cost = cost_function(child1.chromosome)
            child2.cost = cost_function(child2.chromosome)

            children.append(child1)
            children.append(child2)

        population += children


        #Sort population
        population = sorted(population, key=lambda x:x.cost)


        #Cull population
        population = population[:population_size]


        #Check solution
        if population[i].cost < best_solution.cost:
            best_solution = deepcopy(population[i])
            print(best_solution.cost)

        if (best_solution.cost <= acceptable_cost):
            return best_solution.cost, i

    return best_solution.cost, max_num_of_generations


best, num_iterations = run_genetic(prob, params)
print("Best Solution Cost: ", best)
print("Num of iterations: ", num_iterations)