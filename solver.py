import numpy as np
from random import random, randint, sample

# ###################Pramaters##############################
target = 'x*(5-x)=0'
mutation_rate = 0.2
cross_over_rate = 1
elitism = True
elitism_group = 8
if elitism_group % 2 != 0:
    print("elitism_group must be an even number")
    exit(0)
tournament_group = 8
# population must be an even number
population = 200
if population % 2 != 0:
    print("Population must be an even number")
    exit(0)
gen_num = 0
current_gen = []
next_gen = []
fitness_lst = []
distance_from_target = 1000
genome_length = 32
iterations = 500
counter = 0
# ###################Pramaters##############################


# selecting the best offspring from a group of tournament_group
def tournament_selection():
    random_offsprings = sample(range(len(current_gen)), tournament_group)
    offsprings_fitness = [fitness_lst[g] for g in random_offsprings]
    return current_gen[random_offsprings[np.argmax(offsprings_fitness)]]


# cross overing some of the genes by a random cut
def cross_over(genome_1, genome_2):
    if random() < cross_over_rate:
        random_slice = randint(1, genome_length - 1)
        genome_1_out = genome_1[:random_slice] + genome_2[random_slice:]
        genome_2_out = genome_2[:random_slice] + genome_1[random_slice:]
        return genome_1_out, genome_2_out
    else:
        return genome_1, genome_2


# mutating a random bit of a given genome by a crossing rate
def mutate(genome):
    genome = list(genome)
    for g in range(len(genome)):
        if random() < mutation_rate:
            genome[g] = str((int(genome[g]) + 1) % 2)
    return "".join(genome)


# transfer the best x offsprings of the previous generation to the next, x = elitism_group
def elitism_func():
    global fitness_lst, current_gen, next_gen
    best_offsprings = np.argsort(fitness_lst)[-elitism_group:]
    indx = elitism_group - 1
    for i in best_offsprings:
        if len(next_gen) < elitism_group:
            next_gen.append(current_gen[i])
        else:
            indx -= 1
            next_gen[indx] = current_gen[i]
            next_gen[population - elitism_group + indx] = mutate(current_gen[i])
    for p in range(elitism_group - 1):
        for g in range(p + 1, elitism_group):
            try:
                if abs(binary32bit_to_float(next_gen[p]) - binary32bit_to_float(next_gen[g])) < 0.05:
                    next_gen[g] = create_rand_genome()
            except OverflowError:
                pass


# evaluating the fitness/accuracy of a given genome
def fitness_evaluate(genome):
    global counter
    counter += 1
    input_num = binary32bit_to_float(genome)
    splited_eq = target.replace('x', str(input_num)).split('=')
    left_side, right_side = splited_eq[0], splited_eq[1]
    try:
        distance = abs(eval(left_side) - eval(right_side))
    except Exception:
        return 0
    if distance > distance_from_target or ((distance_from_target - distance) * 100 / distance_from_target > 99.9 and abs(input_num - 0) < 0.001):
        return 0
    else:
        return (distance_from_target - distance) * 100 / distance_from_target


# creating a new generation
def create_new_gen():
    global current_gen, next_gen
    if not elitism:
        if len(next_gen) == 0:
            for pop in range(int(population / 2)):
                offspring_1, offspring_2 = cross_over(tournament_selection(), tournament_selection())
                offspring_1, offspring_2 = mutate(offspring_1), mutate(offspring_2)
                next_gen.append(offspring_1)
                next_gen.append(offspring_2)
        else:
            for pop in range(int(population / 2)):
                offspring_1, offspring_2 = cross_over(tournament_selection(), tournament_selection())
                offspring_1, offspring_2 = mutate(offspring_1), mutate(offspring_2)
                next_gen[pop * 2] = offspring_1
                next_gen[pop * 2 + 1] = offspring_2
    else:
        # elitism function
        elitism_func()
        if len(next_gen) == elitism_group:
            for pop in range(int(elitism_group/2), int(population / 2)):
                offspring_1, offspring_2 = cross_over(tournament_selection(), tournament_selection())
                offspring_1, offspring_2 = mutate(offspring_1), mutate(offspring_2)
                next_gen.append(offspring_1)
                next_gen.append(offspring_2)
        else:
            for pop in range(elitism_group, int(population / 2)):
                offspring_1, offspring_2 = cross_over(tournament_selection(), tournament_selection())
                offspring_1, offspring_2 = mutate(offspring_1), mutate(offspring_2)
                next_gen[pop * 2 - elitism_group] = offspring_1
                next_gen[pop * 2 + 1 - elitism_group] = offspring_2
    # for offspring in range(elitism_group + 1, population):
    #     try:
    #         if abs(binary32bit_to_float(next_gen[0]) - binary32bit_to_float(next_gen[offspring])) < 0.000000000000001:
    #             next_gen[offspring] = create_rand_genome()
    #     except OverflowError:
    #         pass
    current_gen = next_gen.copy()


# updating the fitness
def fitness_update():
    if len(fitness_lst) == 0:
        for pop in range(population):
            fitness_lst.append(fitness_evaluate(current_gen[pop]))
    else:
        for pop in range(population):
            fitness_lst[pop] = fitness_evaluate(current_gen[pop])


# creating generation 0 with random offsprings
def init_gen_0():
    for pop in range(population):
        current_gen.append(create_rand_genome())


# create random genome of length: genome_length=32
def create_rand_genome():
    out = ''
    for g in range(genome_length):
        rand_num = randint(0, 1)
        out += str(rand_num)
    return out


# translate a binary 32 bit binary to float number
def binary32bit_to_float(genome):
    sign = genome[0]
    exponent = genome[1:11]
    mantissa = genome[11:]
    exponent = int(exponent, 2) - 255
    mantissa = int(mantissa, 2)
    result = mantissa * 10 ** exponent
    if sign == '1':
        result = -1 * result
    return result


if __name__ == '__main__':
    init_gen_0()
    fitness_update()
    # print(binary32bit_to_float(current_gen[np.argmax(fitness_lst)]), max(fitness_lst))
    print(list(map(binary32bit_to_float, [current_gen[g] for g in np.argsort(fitness_lst)[-2:]])), max(fitness_lst))
    # Record achievements
    create_new_gen()
    for i in range(iterations):
        fitness_update()
        # print(binary32bit_to_float(current_gen[np.argmax(fitness_lst)]), max(fitness_lst))
        print(list(map(binary32bit_to_float, [current_gen[g] for g in np.argsort(fitness_lst)[-2:]])), max(fitness_lst))
        create_new_gen()
