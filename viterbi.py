import numpy as np



def viterbi(emission_path, 
            state_matrix, 
            emission_matrix, 
            state_to_index, 
            emission_to_index,
            states,
            emissions) -> str:
    backtrack_graph = {}
    dp_array = {}
    equal_prob = 1.0 / len(states)
    for i, emission in enumerate(emission_path):
        process_dp_col(state_matrix, emission_matrix, state_to_index, 
                       emission_to_index, states, backtrack_graph, dp_array, 
                       equal_prob, i, emission)
    best_final_state = get_best_final_state(emission_path, states, dp_array)
    
    best_path = get_best_path(emission_path, backtrack_graph, best_final_state)

    return best_path

def get_best_path(emission_path, backtrack_graph, best_final_state):
    best_path = best_final_state
    best_prev_state = best_final_state

    for i in range(len(emission_path) - 1, 0, -1):
        key = (i, best_prev_state)
        best_prev_state = backtrack_graph[key]
        best_path = best_prev_state + best_path
    return best_path

def get_best_final_state(emission_path, states, dp_array):
    curr_max = 0
    best_final_state = None
    last_index = len(emission_path) - 1
    for state in states:
        if dp_array[last_index][state] > curr_max:
            curr_max = dp_array[last_index][state]
            best_final_state = state
    return best_final_state

def process_dp_col(state_matrix, emission_matrix, state_to_index, emission_to_index, states, backtrack_graph, dp_array, equal_prob, i, emission):
    dp_array[i] = {}
    for state in states:
        if i == 0:
            dp_array[i][state] = equal_prob * \
                emission_matrix[state_to_index[state], emission_to_index[emission]]
        else:
            max_prob = 0
            max_prev_state = None
            for prev_state in states:
                prob = dp_array[i-1][prev_state] * \
                    state_matrix[state_to_index[prev_state], state_to_index[state]] * \
                    emission_matrix[state_to_index[state], emission_to_index[emission]]
                if prob > max_prob:
                    max_prob = prob
                    max_prev_state = prev_state
            dp_array[i][state] = max_prob
            backtrack_graph[(i, state)] = max_prev_state





def read_input():
    with open("input.txt", "rt") as f:
        data = iter(f.readlines())

    emission_path = next(data).strip()
    assert next(data).startswith("-")
    emissions = next(data).strip().split()
    n_emissions = len(emissions)

    assert next(data).startswith("-")

    states = next(data).strip().split()
    n_states = len(states)

    assert next(data).startswith("-")


    state_matrix_headers = next(data).strip().split()
    assert state_matrix_headers == states
    state_to_index = {state: i for i, state in enumerate(states)}
    emission_to_index = {emission: i for i, emission in enumerate(emissions)}
    rows = []
    for i in range(n_states):
        row = next(data).strip().split()
        assert len(row) - 1 == n_states
        row = [float(x) for x in row[1:]]
        rows.append(row)
    state_matrix = np.array(rows)

    assert next(data).startswith("-")

    emission_matrix_headers = next(data).strip().split()
    assert emission_matrix_headers == emissions
    rows = []
    for i in range(n_states):
        row = next(data).strip().split()
        assert len(row) - 1 == n_emissions
        row = [float(x) for x in row[1:]]
        rows.append(row)
    emission_matrix = np.array(rows)

    return emission_path, emissions, states, state_matrix, emission_matrix, state_to_index, emission_to_index

def debug_input_read(read_input):
    emission_path, emissions, states, state_matrix, emission_matrix, state_to_index, emission_to_index = read_input()
    print("Emission Path:", emission_path)
    print("Emissions:", emissions)
    print("States:", states)
    print("State Transition Matrix:\n", state_matrix)
    print("Emission Matrix:\n", emission_matrix)
    print("State to Index Mapping:", state_to_index)
    print("Emission to Index Mapping:", emission_to_index)

if __name__ == "__main__":
    emission_path, emissions, states, state_matrix, emission_matrix, state_to_index, emission_to_index = read_input()
    best_path = viterbi(emission_path, 
            state_matrix, 
            emission_matrix, 
            state_to_index, 
            emission_to_index,
            states,
            emissions)
    
    print(best_path)