import numpy as np
import itertools
import random

# candidate locations including a central buffer (CB)
candidate_locations = {
    "Receiving": (0, 0),
    "LOC1": (1, 0),
    "LOC2": (2, 0),
    "LOC3": (0, 1),
    "LOC4": (1, 1),
    "LOC5": (2, 1),
    "LOC6": (0, 2),
    "LOC7": (1, 2),
    "CB": (1, 3),  # Assumed Central Buffer position
    "Shipping": (2, 3)
}

machines = ['VTC1', 'VTC2', 'CB', 'HMC', 'UMC', 'VMC', 'SHP']

process_plans = {
    'A': ['op1', 'op2', 'op3'],
    'B': ['op4', 'op2', 'op5', 'op6'],
    'C': ['op7', 'op8', 'op9', 'op10'],
    'D': ['op11', 'op12', 'op13'],
    'E': ['op14', 'op8', 'op15']
}

arrival_rates = {
    'A': 4,
    'B': 4,
    'C': 6,
    'D': 3,
    'E': 3
}

machine_operations = {
    'op1': 'VTC2',
    'op2': 'SHP',
    'op3': 'VMC',
    'op4': 'VTC1',
    'op5': 'VTC2',
    'op6': 'HMC',
    'op7': 'VTC1',
    'op8': 'SHP',
    'op9': 'UMC',
    'op10': 'VTC1',
    'op11': 'VTC2',
    'op12': 'VMC',
    'op13': 'HMC',
    'op14': 'VTC1',
    'op15': 'HMC'
}

processing_times = {
    'op1': 240,
    'op2': 120,
    'op3': 420,
    'op4': 260,
    'op5': 120,
    'op6': 300,
    'op7': 220,
    'op8': 90,
    'op9': 480,
    'op10': 120,
    'op11': 440,
    'op12': 300,
    'op13': 360,
    'op14': 150,
    'op15': 380
}

# initializing a flow matrix with zeros.
flow_matrix = np.zeros((len(machines), len(machines)))

# filling the flow matrix based on the process plans and arrival rates.
for part, operations in process_plans.items():
    rate = arrival_rates[part]
    for i in range(len(operations) - 1):
        from_machine = machine_operations[operations[i]]
        to_machine = machine_operations[operations[i + 1]]
        from_index = machines.index(from_machine)
        to_index = machines.index(to_machine)
        # multiply the flow by the processing time of the 'from' operation.
        flow_matrix[from_index][to_index] += rate * processing_times[operations[i]]

# manhattan distance function
def manhattan_distance(loc1, loc2):
    return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

# generating a distance matrix using the manhattan distance
locations = list(candidate_locations.keys())
distance_matrix = np.zeros((len(locations), len(locations)))
for i, loc1 in enumerate(locations):
    for j, loc2 in enumerate(locations):
        if i != j:
            distance_matrix[i][j] = manhattan_distance(candidate_locations[loc1], candidate_locations[loc2])

# function to generate an initial layout based on the flow matrix
def generate_initial_layout(flow_matrix, machines):
    machine_flow = np.sum(flow_matrix, axis=0) + np.sum(flow_matrix, axis=1)
    sorted_machines = [machine for _, machine in sorted(zip(machine_flow, machines), reverse=True)]
    return sorted_machines

# function to apply a simple improvement heuristic to the initial layout
def improve_layout(initial_layout, flow_matrix, distance_matrix, iterations=10000):
    best_layout = initial_layout.copy()
    best_distance = calculate_total_loaded_distance(best_layout, flow_matrix, distance_matrix)
    
    for _ in range(iterations):
        i, j = random.sample(range(len(best_layout)), 2)
        new_layout = best_layout.copy()
        new_layout[i], new_layout[j] = new_layout[j], new_layout[i]
        new_distance = calculate_total_loaded_distance(new_layout, flow_matrix, distance_matrix)
        if new_distance < best_distance:
            best_layout = new_layout
            best_distance = new_distance
    
    return best_layout

# function to calculate the total loaded distance for a layout
def calculate_total_loaded_distance(layout, flow_matrix, distance_matrix):
    position_dict = {machine: i for i, machine in enumerate(layout)}
    total_distance = 0
    for i in range(len(flow_matrix)):
        for j in range(len(flow_matrix[i])):
            if flow_matrix[i][j] > 0:
                from_pos = position_dict[machines[i]]
                to_pos = position_dict[machines[j]]
                total_distance += flow_matrix[i][j] * distance_matrix[from_pos][to_pos]
    return total_distance

# generating the initial and improved layouts
initial_layout = generate_initial_layout(flow_matrix, machines)
improved_layout = improve_layout(initial_layout, flow_matrix, distance_matrix)

# calculating the total loaded distances for both layouts
initial_distance = calculate_total_loaded_distance(initial_layout, flow_matrix, distance_matrix)
improved_distance = calculate_total_loaded_distance(improved_layout, flow_matrix, distance_matrix)

print("Initial Layout:", initial_layout)
print("Initial Total Loaded Distance:", initial_distance)
print("Improved Layout:", improved_layout)  
print("Improved Total Loaded Distance:", improved_distance)

#%% rest is for the reporting purposes only
locations = list(candidate_locations.keys())
distance_matrix_values = np.zeros((len(locations), len(locations)))

# filling the distance matrix with actual values
for i, loc1 in enumerate(locations):
    for j, loc2 in enumerate(locations):
        if i != j:
            distance_matrix_values[i][j] = manhattan_distance(candidate_locations[loc1], candidate_locations[loc2])

# generating the flow matrix
flow_matrix_values = np.zeros((len(machines), len(machines)))

# filling the flow matrix with actual values
for part, operations in process_plans.items():
    rate = arrival_rates[part]
    for i in range(len(operations) - 1):
        from_machine = machine_operations[operations[i]]
        to_machine = machine_operations[operations[i + 1]]
        from_index = machines.index(from_machine)
        to_index = machines.index(to_machine)
        flow_matrix_values[from_index][to_index] += rate * processing_times[operations[i]]

# function to print the matrices in a format suitable for Excel
def print_matrix(matrix):
    for row in matrix:
        print("\t".join(map(str, row)))

print("From-to Matrix:")
print_matrix(flow_matrix_values)

print("\nDistance Matrix:")
print_matrix(distance_matrix_values)
