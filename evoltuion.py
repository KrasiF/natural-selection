##################################
# 
# Temperature stat:
# max tmax - 6
# min tmax - 3
# max tmin - -3
# min tmin - -6 
#
# Humidity stat:
# max hummax - 8
# min hummax - 3
# max hummin - 3
# min hummin - 0.2
#
# Biome stat:
# For any biome:
# max - 5
# min - 0
#
# For any food stat:
# max - 8.8
# min - 0.375
#
##################################

import random
import copy

GENES_SET = {"TMAX","TMIN","H1","H2","BIOME1","BIOME2","BIOME3","VFS1","VFS2","AFS1","AFS2","FOODGEN1","FOODGEN2","MUTATIONGENE"}

class Environment:
    def __init__(self,temp,hum,biome,vfs_small,vfs_big,afs_small,afs_big,population_max = 40, population_start = 20):
        self.temp = temp
        self.hum = hum
        self.biome = biome
        self.vfs_small = vfs_small
        self.vfs_big = vfs_big
        self.afs_small = afs_small
        self.afs_big = afs_big
        self.population_max = population_max

        self.population = [Organism(create_random_genepool()) for x in range(population_start)]
    
    def evolution_step(self):
        age_population(self.population)
        procreate_until_limit(self.population,self.population_max)
        average_score = get_average_score(self)
        print("Average score: " + str(round(average_score,2)))
        print_lowest_and_highest_score(self.population)
        print_average_scores(self)
        kill_population(average_score,self.population)

    def show_population_genes(self):
        for i in range(len(self.population)):
            print()
            print(self.population[i].genepool)

    


def age_population(population):
    for i in range(len(population)):
        population[i].age += 1

def kill_population(average_score,population,at_age = 3, score_chance_multiplier = 1):
    died_ofage = 0
    died_ofunfitness = 0
    for i in range(len(population)-1,-1,-1):        
        if population[i].age >= at_age:
            died_ofage += 1
            del population[i]
            continue
        if population[i].score < average_score:
            score_percentage = population[i].score / average_score * 100
            random_int = random.randint(1,100)
            if random_int * score_chance_multiplier > score_percentage:
                died_ofunfitness += 1
                del population[i]
    print("Died of age: " + str(died_ofage))
    print("Died of unfitness: " + str(died_ofunfitness))

def print_gene_rarity(gene,population):
    homozygot_dominant = 0
    homozygot_recessive = 0
    heterozygot = 0

    for i in range(len(population)):
        searched_gene = population[i].genepool[gene]
        if(searched_gene[0] != searched_gene[1]):
            heterozygot += 1
        elif(searched_gene[0] == True):
            homozygot_dominant += 1  
        else:
            homozygot_recessive += 1
    print(gene + ": AA: " + str(homozygot_dominant) + " Aa: " + str(heterozygot) + " aa: " + str(homozygot_recessive))

def print_lowest_and_highest_score(population):
    lowest_score = 1000
    highest_score = -1000    
    worst_guy = None
    best_guy = None

    for i in range(len(population)):
        if(population[i].score < lowest_score):
            lowest_score = population[i].score
            worst_guy = population[i]
        if(population[i].score > highest_score):
            highest_score = population[i].score
            best_guy = population[i]

    print("Highest score: " + str(round(highest_score,2)))    
    print("Lowest score: " + str(round(lowest_score,2)))



def procreate_until_limit(population,limit):
    random.shuffle(population)
    pop_len = len(population)
    for i in range(int(pop_len/2)):
        if len(population) >= limit:
            break

        o_a = population[i*2]
        o_b = population[i*2+1]
    
        population.append(Organism.procreate(o_a,o_b))

def get_average_score(environment):
    score_total = 0
    i = 0

    for i in range(len(environment.population)):
        score = get_organism_score(environment,environment.population[i])
        environment.population[i].score = score
        score_total += score
    
    return score_total / len(environment.population)        

def print_average_scores(environment):
    avg_scores = get_average_stats_scores(environment)
    print("Average scores by stat:")
    print(f'Temp.: {avg_scores["temp"]} Humidity: {str(avg_scores["hum"])} Biome: {str(avg_scores["biome"])} AnimalsFS: {str(avg_scores["afs"])} VegetationFS: {str(avg_scores["vfs"])}')

def get_average_stats_scores(environment):
    temp_total = 0
    hum_total = 0
    biome_total = 0
    afs_total = 0
    vfs_total = 0
    i = 0
    for i in range(len(environment.population)):

        temp_total += get_temp_score(environment, environment.population[i])
        hum_total += get_hum_score(environment, environment.population[i])
        biome_total += get_biome_score(environment, environment.population[i])
        afs_total += get_afs_score(environment, environment.population[i])
        vfs_total += get_vfs_score(environment, environment.population[i])
    
    pop_len = len(environment.population)

    avg_scores = {"temp": round(temp_total/pop_len,2),
                  "hum": round(hum_total/pop_len,2),
                  "biome": round(biome_total/pop_len,2),
                  "afs": round(afs_total/pop_len,2),
                  "vfs": round(vfs_total/pop_len,2)}

    return avg_scores
    

def get_organism_score(environment, organism):
    temp_score = get_temp_score(environment,organism)
    hum_score = get_hum_score(environment,organism)
    biome_score = get_biome_score(environment,organism)
    afs_score = get_afs_score(environment, organism)
    vfs_score = get_vfs_score(environment, organism)

    organism.score_types["temp_score"] = temp_score
    organism.score_types["hum_score"] = hum_score
    organism.score_types["biome_score"] = biome_score
    organism.score_types["afs_score"] = afs_score
    organism.score_types["vfs_score"] = vfs_score

    return temp_score + hum_score + biome_score + afs_score + vfs_score


def get_afs_score(environment, organism):
    afs_big_score = 0

    afs_big_difference = environment.afs_big - organism.fitness["afs_big"]

    if(afs_big_difference > 0.5):
        if afs_big_difference < 1.5:
            afs_big_score = 80
        elif afs_big_difference < 2.5:
            afs_big_score = 60
        elif afs_big_difference < 3.5:
            afs_big_score = 30
        elif afs_big_difference < 4.5:
            afs_big_score = 10
        else:
            afs_big_score = 0
    else:
        afs_big_score = 100

    afs_big_score *= environment.afs_big/8.8

    afs_small_score = 0

    afs_small_difference = environment.afs_small - organism.fitness["afs_small"]

    if(afs_small_difference > 0.5):
        if afs_small_difference < 1:
            afs_small_score = 80
        elif afs_small_difference < 2:
            afs_small_score = 60
        elif afs_small_difference < 3:
            afs_small_score = 30
        elif afs_small_difference < 4:
            afs_small_score = 10
        else:
            afs_small_score = 0
    else:
        afs_small_score = 100
    
    afs_small_score *= environment.afs_small/8.8

    return afs_big_score + afs_small_score

def get_vfs_score(environment, organism):
    vfs_big_score = 0

    vfs_big_difference = environment.vfs_big - organism.fitness["vfs_big"]

    if(vfs_big_difference > 0.5):
        if vfs_big_difference < 1:
            vfs_big_score = 80
        elif vfs_big_difference < 2:
            vfs_big_score = 60
        elif vfs_big_difference < 3:
            vfs_big_score = 30
        elif vfs_big_difference < 4:
            vfs_big_score = 10
        else:
            vfs_big_score = 0
    else:
        vfs_big_score = 100

    vfs_big_score *= environment.vfs_big/8.8

    vfs_small_score = 0

    vfs_small_difference = environment.vfs_small - organism.fitness["vfs_small"]

    if(vfs_small_difference > 0.5):
        if vfs_small_difference < 1:
            vfs_small_score = 80
        elif vfs_small_difference < 2:
            vfs_small_score = 60
        elif vfs_small_difference < 3:
            vfs_small_score = 30
        elif vfs_small_difference < 4:
            vfs_small_score = 10
        else:
            vfs_small_score = 0
    else:
        vfs_small_score = 100
    
    vfs_small_score *= environment.vfs_small/8.8

    return vfs_big_score + vfs_small_score

def get_biome_score(environment,organism):
    biomefitness = organism.fitness[environment.biome]
    score = 0 
    if biomefitness == 5:
        score = 100
    elif biomefitness == 4:
        score = 95
    elif biomefitness == 3:
        score = 75
    elif biomefitness == 2:
        score = 45
    elif biomefitness == 1:
        score = 15
    else:
        score = 0
    return score
    

    
def get_temp_score(environment,organism):
    tmax_difference = environment.temp - organism.fitness["tmax"]
    tmin_difference = organism.fitness["tmin"] - environment.temp
    biggest_difference = tmax_difference if tmax_difference > tmin_difference else tmin_difference
    score = 0

    if(biggest_difference > 0):
        if(biggest_difference < 1):
            score = 80
        elif(biggest_difference < 2):
            score = 60
        elif(biggest_difference < 3):
            score = 40
        else:
            score = 0
    else:
        score = 100
    return score

def get_hum_score(environment, organism):
    hummax_difference = environment.hum - organism.fitness["hummax"]
    hummin_difference = organism.fitness["hummin"] - environment.hum
    biggest_difference = hummax_difference if hummax_difference > hummin_difference else hummin_difference

    if(biggest_difference > 0):
        if(biggest_difference <= 10):
            return 80
        elif(biggest_difference <= 20):
            return 65
        elif(biggest_difference <= 30):
            return 50
        else:
            return 0
    else:
        return 100




def create_genepool():    
    genepool = { 
        "TMAX": (True,False),
        "TMIN": (True,False),
        "H1": (True,False),
        "H2": (True,False),
        "BIOME1": (True,False),
        "BIOME2": (True,False),
        "BIOME3": (True,False),
        "VFS1": (True,False),
        "VFS2": (True,False),
        "AFS1": (True,False),
        "AFS2": (True,False),
        "FOODGEN1": (True,False),
        "FOODGEN2": (True,False),
        "MUTATIONGENE": (True,False)
    }
    return copy.deepcopy(genepool)

def create_random_genepool():
    genepool = { 
        "TMAX": get_random_allels(),
        "TMIN": get_random_allels(),
        "H1": get_random_allels(),
        "H2": get_random_allels(),
        "BIOME1": get_random_allels(),
        "BIOME2": get_random_allels(),
        "BIOME3": get_random_allels(),
        "VFS1": get_random_allels(),
        "VFS2": get_random_allels(),
        "AFS1": get_random_allels(),
        "AFS2": get_random_allels(),
        "FOODGEN1": get_random_allels(),
        "FOODGEN2": get_random_allels(),
        "MUTATIONGENE": get_random_allels()
    }
    return copy.deepcopy(genepool)



def create_fitness_stats():
    fitness = {
        "tmax": 0,
        "tmin": 0,
        "hummax": 0,
        "hummin": 0,
        "desert": 0,
        "plains": 0,
        "mountains": 0,
        "vfs_big": 0,
        "vfs_small": 0,
        "afs_big": 0,
        "afs_small": 0
    }
    return fitness

def get_random_allels(A_mod = 50,a_mod = 50):
    A_value = random.randint(1,100)
    A = A_value < A_mod
    a_value = random.randint(1,100)
    a = a_value < a_mod
    return (A,a)

class Organism:   
    
    GEN_AMOUNT = 13

    def __init__(self,genepool = create_genepool()):
        self.genepool = copy.deepcopy(genepool)
        self.fitness = create_fitness_stats()
        self.calculate_fitness()
        self.age = 0
        self.score = 0
        self.score_types = {"afs_score":0, "vfs_score": 0, "temp_score": 0, "hum_score": 0, "biome_score": 0}

    def calculate_fitness(self):
        tmax = self.genepool["TMAX"][0] or self.genepool["TMAX"][1]
        tmin = self.genepool["TMIN"][0] or self.genepool["TMIN"][1]
        h1 = self.genepool["H1"][0] or self.genepool["H1"][1]
        h2 = self.genepool["H2"][0] or self.genepool["H2"][1]
        biome1 = self.genepool["BIOME1"][0] or self.genepool["BIOME1"][1]
        biome2 = self.genepool["BIOME2"][0] or self.genepool["BIOME2"][1]
        biome3 = self.genepool["BIOME3"][0] or self.genepool["BIOME3"][1]
        vfs1 = self.genepool["VFS1"][0] or self.genepool["VFS1"][1]
        vfs2 = self.genepool["VFS2"][0] or self.genepool["VFS2"][1]
        afs1 = self.genepool["AFS1"][0] or self.genepool["AFS1"][1]
        afs2 = self.genepool["AFS2"][0] or self.genepool["AFS2"][1]
        foodgen1 = self.genepool["FOODGEN1"][0] or self.genepool["FOODGEN1"][1]
        foodgen2 = self.genepool["FOODGEN2"][0] or self.genepool["FOODGEN2"][1]

        self.fitness["tmax"] = (5 if tmax else 3) + (0 if tmin else 1)
        self.fitness["tmin"] = (-5 if tmin else -3) + (0 if tmax else -1)
        self.fitness["hummax"] = (8 if h1 else 6) * (1 if h2 else 0.5)
        self.fitness["hummin"] = (3 if h1 else 1) * (1 if h2 else 0.2)
        self.fitness["desert"] = (3 if biome1 else 0) + (1 if not biome2 else 0) + (1 if not biome3 else 0)
        self.fitness["plains"] = (3 if biome2 else 0) + (1 if not biome1 else 0) + (1 if not biome3 else 0)
        self.fitness["mountains"] = (3 if biome3 else 0) + (1 if not biome1 else 0) + (1 if not biome2 else 0)
        self.fitness["vfs_big"] = ((5 if vfs1 else 2) + (1 if vfs2 else 3) + (-2 if afs1 or afs2 else 0)) * (1 if foodgen1 else 0.5) * (0.75 if foodgen2 else 1.10)
        self.fitness["vfs_small"] = ((5 if vfs2 else 2) + (1 if vfs1 else 3) + (-2 if afs1 or afs2 else 0)) * (1 if foodgen1 else 0.5) * (0.75 if foodgen2 else 1.10)
        self.fitness["afs_big"] = ((5 if afs1 else 2) + (1 if afs2 else 3) + (-2 if vfs1 or vfs2 else 0)) * (1 if foodgen2 else 0.5) * (0.75 if foodgen1 else 1.10)
        self.fitness["afs_small"] = ((5 if afs2 else 2) + (1 if afs1 else 3) + (-2 if vfs1 or vfs2 else 0)) * (1 if foodgen2 else 0.5) * (0.75 if foodgen1 else 1.10)

    def get_organism_mutation_chance(self):
        mutation_gene = self.genepool["MUTATIONGENE"]
        mutation_chance = 0

        if mutation_gene[0] != mutation_gene[1]:
            mutation_chance = 40
        elif mutation_gene[0] and mutation_gene[1]:
            mutation_chance = 100
        else:
            mutation_chance = 5
    
        return mutation_chance

    @staticmethod
    def procreate(organism_a,organism_b):
        new_genpool = create_genepool()
        for gene in GENES_SET:
            new_genpool[gene] = Organism.get_random_allels_from_parents(gene,organism_a,organism_b)
        return Organism(new_genpool)
    
    @staticmethod
    def get_random_allels_from_parents(gene,organism_a,organism_b,mutation_chance_promile = 1):
    
        parent_a_allel = random.randint(0,1)    
        parent_a_random_allel = organism_a.genepool[gene][parent_a_allel]

        parent_b_allel = random.randint(0,1)
        parent_b_random_allel = organism_b.genepool[gene][parent_b_allel]

        a_mutation = random.randint(1,1000)
        if(a_mutation <= organism_a.get_organism_mutation_chance()):
            parent_a_random_allel = True if random.randint(0,1) == 1 else False

        b_mutation = random.randint(1,1000)
        if(b_mutation <= organism_b.get_organism_mutation_chance()):
            parent_b_random_allel = True if random.randint(0,1) == 1 else False

        return (parent_a_random_allel,parent_b_random_allel)  



    

