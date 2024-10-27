import random
import numpy as np

# Define the problem parameters
facilitators = ["Lock", "Glen", "Banks", "Richards", "Shaw", "Singer", "Uther", "Tyler", "Numen", "Zeldin"]

activities = ["SLA100A", "SLA100B", "SLA191A", "SLA191B", "SLA201", "SLA291", "SLA303", "SLA304", "SLA394", "SLA449", "SLA451"]

prefFacilitators = {
    "SLA100A": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA100B": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA191A": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA191B": ["Glen", "Lock", "Banks", "Zeldin"],
    "SLA201": ["Glen", "Banks", "Zeldin", "Shaw"],
    "SLA291": ["Lock", "Banks", "Zeldin", "Singer"],
    "SLA303": ["Glen", "Zeldin", "Banks"],
    "SLA304": ["Glen", "Banks", "Tyler"],
    "SLA394": ["Tyler", "Singer"],
    "SLA449": ["Tyler", "Singer", "Shaw"],
    "SLA451": ["Tyler", "Singer", "Shaw"]
}

otherFacilitators = {
    "SLA100A": ["Numen", "Richards"],
    "SLA100B": ["Numen",  "Richards"],
    "SLA191A": ["Numen",  "Richards"],
    "SLA191B": ["Numen",  "Richards"],
    "SLA201": ["Numen", "Richards", "Singer"],
    "SLA291": ["Numen",  "Richards", "Shaw", "Tyler"],
    "SLA303": ["Numen", "Singer", "Shaw"],
    "SLA304": ["Numen", "Singer", "Shaw", "Richards", "Uther", "Zeldin"],
    "SLA394": ["Richards", "Zeldin"],
    "SLA449": ["Zeldin", "Uther"],
    "SLA451": ["Zeldin", "Uther", "Richards",  "Banks"]
}

rooms = {"Slater 003": 45, "Roman 216": 30, "Loft 206": 75, "Roman 201": 50, "Loft 310": 108, "Beach 201": 60, "Beach 301": 75, "Logos 325": 450, "Frank 119": 60}

timeSlots = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]

expEnrollment = { "SLA100A": 50, "SLA100B": 50, "SLA191A": 50, "SLA191B": 50, "SLA201": 50, "SLA291": 50, "SLA303": 60, "SLA304": 25, "SLA394": 20, "SLA449": 60, "SLA451": 100}

# Define the fitness function
def fitness(schedule):
    score = 0
    timePairs = []
    professorLoad = []
    activityCheck = []

    for activity, room, timeSlot, facilitator in schedule:
        # Room Availability
        roomKey = (timeSlot, room)
        if roomKey in timePairs:
            score -= 0.5
        else:
            timePairs.append(roomKey)
         
        # Room Size Fitness
        if rooms[room] < expEnrollment[activity]:
            score -= 0.5
        elif rooms[room] > 3 * expEnrollment[activity]:
            score -= 0.2
        elif rooms[room] > 6 * expEnrollment[activity]:
            score -= 0.4
        else:
            score += 0.3

        # Facilitator Fitness
        loadKey = (facilitator, timeSlot)
        professorLoad.append(loadKey)
        loadTotal = professorLoad.count(facilitator)

        if facilitator in prefFacilitators[activity]:
            score += 0.5
        elif facilitator in otherFacilitators[activity]:
            score += 0.2
        else:
            score -= 0.1

        if loadTotal > 4:
            score -= 0.5
        elif loadTotal <= 2:
            score -= 0.4

        if professorLoad.count(loadKey) == 1:
            score += 0.2
        else:
            score -= 0.2
            
        # Activity scores
        #actKey = (activity, timeSlot)
        #activityCheck.append(actKey)
        #actTotal = activityCheck.count(actKey)

        #if activityCheck.count(actKey) == ""
        

    return score

# Genetic Algorithm Functions
def randomSchedule():
    schedule = []
    for activity in activities:
        room = random.choice(list(rooms.keys()))
        time_slot = random.choice(timeSlots)
        facilitator = random.choice(facilitators)
        schedule.append((activity, room, time_slot, facilitator))
    return schedule

def initializePop(population_size):
    population = [randomSchedule() for i in range(population_size)]

    return population

def softmax(scores):
    exp_scores = np.exp(scores)
    return exp_scores / np.sum(exp_scores)

def randomSelection(population, scores):
    probabilities = softmax(scores)
    selected_indices = np.random.choice(len(population), size=len(population), p=probabilities)
    selected_population = [population[i] for i in selected_indices]
    return selected_population

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(schedule, mutation_rate):
    mutated_schedule = []
    for activity, room, time_slot, facilitator in schedule:
        if random.random() < mutation_rate:
            room = random.choice(list(rooms.keys()))
            time_slot = random.choice(timeSlots)
            facilitator = random.choice(facilitators)
        mutated_schedule.append((activity, room, time_slot, facilitator))
    return mutated_schedule

def genetic_algorithm(population_size, mutation_rate, generations):
    population = initializePop(population_size)
    for _ in range(generations):
        scores = [fitness(schedule) for schedule in population]
        selected_population = randomSelection(population, scores)
        next_generation = []
        for i in range(0, len(selected_population), 2):
            parent1, parent2 = selected_population[i], selected_population[i + 1]
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            next_generation.extend([child1, child2])
        population = next_generation
    best_schedule = max(population, key=fitness)
    best_fitness = fitness(best_schedule)
    return best_schedule, best_fitness

# Main function
if __name__ == "__main__":
    best_schedule, best_fitness = genetic_algorithm(population_size=500, mutation_rate=0.01, generations=100)
    print("Best Fitness:", best_fitness)
    print("Best Schedule:")
    for activity, room, timeSlot, facilitator in best_schedule:
        print(activity, "|", room, "|", timeSlot, "|", facilitator)
