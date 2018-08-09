#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
from random import randint, random, shuffle
from prettytable import PrettyTable
import requests


class Gene:

    def __init__(self, value, min_, max_):
        self.__value = value
        self.__min = min_
        self.__max = max_

    @property
    def value(self):
        return self.__value

    def mutate(self):
        self.__value = randint(self.__min, self.__max)


class Chromosome:

    def __init__(self):
        self.__genes = [Gene(None, 0, 359), Gene(None, 0, 359), Gene(None, 0, 359), Gene(None, 0, 359),
                        Gene(None, 0, 359), Gene(None, 0, 359)]
        self.fitness = 0
        for gene in self.__genes:
            gene.mutate()

    @property
    def genes(self):
        return self.__genes

    def get_gene(self, index):
        return self.__genes[index]

    def set_gene(self, index, value):
        self.__genes[index] = value

    @staticmethod
    def get_att_names():
        return ['fitness', 'phi1', 'theta1', 'phi2', 'theta2', 'phi3', 'theta3']

    def crossover(self, other):
        child1 = Chromosome()
        child1.__genes = self.__genes.copy()

        child2 = Chromosome()
        child2.__genes = other.__genes.copy()

        point1 = randint(0, 5)
        point2 = randint(1, 6)
        while point2 == point1:
            point2 = randint(1, 6)

        child1_genes = child1.__genes[point1:point2].copy()
        child2_genes = child2.genes[point1:point2].copy()

        child1.__genes[point1:point2] = child2_genes.copy()
        child2.__genes[point1:point2] = child1_genes.copy()

        return child1, child2


class Antenna:

    def __init__(self, population_size, mutation_factor, max_generations):
        self.population_size = population_size
        self.mutation_factor = mutation_factor
        self.max_generations = max_generations

    def get_best_antenna(self, fitness_desired, population_=None):
        population = population_
        if population is None:
            population = self.get_random_population().copy()
        best_chromosome = self.get_max_fitness(population)
        is_empty = False

        generation = 0
        while best_chromosome.fitness < fitness_desired and len(population) > 1:
            if 0 < self.max_generations < generation:
                break
            self.print_generation(population, generation)
            parents = self.parents_selection(population)
            population = self.reproduce(parents)
            candidate_chromosome = self.get_max_fitness(population)
            if candidate_chromosome is not None:
                best_chromosome = candidate_chromosome
            generation += 1

        if len(population) <= 1:
            print('IsEmpty')
            is_empty = True

        return best_chromosome, is_empty

    @staticmethod
    def print_generation(population, generation):
        if len(population) <= 0:
            print('Population empty')
            return

        t = PrettyTable(population[0].get_att_names())
        for chromosome in population:
            genes = []
            for gene in chromosome.genes:
                genes.append(gene.value)
            t.add_row([chromosome.fitness] + genes)
        print('----- GENERATION {} -----'.format(generation))
        print(t)

    def get_random_population(self):
        pop = []
        for x in range(0, self.population_size):
            pop.append(Chromosome())
        return pop

    def get_max_fitness(self, population):
        if len(population) <= 0:
            return

        best_chromosome = population[0]
        max_fitness = best_chromosome.fitness

        for chromosome in population:
            chromosome.fitness = self.get_fitness(chromosome)
            if chromosome.fitness > max_fitness:
                max_fitness = chromosome.fitness
                best_chromosome = chromosome

        return best_chromosome

    @staticmethod
    def get_fitness(chromosome: Chromosome):
        URL = 'http://localhost:8080/antenna/simulate?'

        URL += 'phi1={}&theta1={}&phi2={}&theta2={}&phi3={}&theta3={}'.format(chromosome.get_gene(0).value,
                                                                              chromosome.get_gene(1).value,
                                                                              chromosome.get_gene(2).value,
                                                                              chromosome.get_gene(3).value,
                                                                              chromosome.get_gene(4).value,
                                                                              chromosome.get_gene(5).value)
        r = requests.post(url=URL)
        return float(r.text.splitlines()[0])

    def parents_selection(self, population):
        sorted_population = sorted(population, key=lambda c: c.fitness)
        sorted_fitness = list(c.fitness for c in sorted_population)
        sorted_probabilities = []

        # calc probabilities
        min_fitness = abs(min(sorted_fitness))
        for x in range(0, len(sorted_fitness)):
            sorted_fitness[x] += min_fitness

        sum_fitness = sum(sorted_fitness)
        for x in range(0, len(sorted_fitness)):
            p = sum(sorted_probabilities[:x])
            if sum_fitness != 0:
                p += sorted_fitness[x]/sum_fitness
            sorted_probabilities.append(p)

        # selecting parents
        parents = []
        for x in range(0, len(sorted_population)):
            chromosome = sorted_population[x]
            p = sorted_probabilities[x]
            dice = random()

            if dice <= p:
                parents.append(chromosome)

        return parents[0:self.population_size]

    def reproduce(self, parents_):
        parents = parents_.copy()
        couples = self.define_couples(parents)

        childs = []
        for couple in couples:
            child1, child2 = couple[0].crossover(couple[1])
            childs.append(child1)
            childs.append(child2)

        # mutate
        population = childs + parents_
        p = self.mutation_factor
        for chromosome in population:
            for gene in chromosome.genes:
                if random() <= p:
                    gene.mutate()

        return population

    def define_couples(self, parents_):
        parents = parents_.copy()
        couples = []
        for x in range(0, int(len(parents)/2)):
            first = parents[randint(0, len(parents)-1)]
            parents.remove(first)
            second = parents[randint(0, len(parents)-1)]
            parents.remove(second)

            couples.append((first, second))

        return couples


# ----- TEST -----
antenna = Antenna(10, 1e-2, 50)
is_empty_ = True
best_antenna = None

while is_empty_:
    best_antenna, is_empty_ = antenna.get_best_antenna(20)

t = PrettyTable(best_antenna.get_att_names())
genes = []
for gene in best_antenna.genes:
    genes.append(gene.value)
t.add_row([best_antenna.fitness] + genes)

print('----- BEST ANTENNA -----')
print(t)
