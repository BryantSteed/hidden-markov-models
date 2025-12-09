import numpy as np



def compute_path_probability(emission_path, 
            state_matrix, 
            emission_matrix, 
            state_to_index, 
            emission_to_index,
            states) -> str:
    dp_array = {}
    equal_prob = 1.0 / len(states)
    for i, emission in enumerate(emission_path):
        process_dp_col(state_matrix, emission_matrix, state_to_index, 
                       emission_to_index, states, dp_array, 
                       equal_prob, i, emission)

    last_col = dp_array[len(emission_path) - 1]
    total_prob = sum(last_col[state] for state in states)
    return total_prob


def process_dp_col(state_matrix, emission_matrix, state_to_index, emission_to_index, states, dp_array, equal_prob, i, emission):
    dp_array[i] = {}
    for state in states:
        if i == 0:
            dp_array[i][state] = equal_prob * \
                emission_matrix[state_to_index[state], emission_to_index[emission]]
        else:
            total_prob = 0
            for prev_state in states:
                prob = dp_array[i-1][prev_state] * \
                    state_matrix[state_to_index[prev_state], state_to_index[state]] * \
                    emission_matrix[state_to_index[state], emission_to_index[emission]]
                total_prob += prob
            dp_array[i][state] = total_prob





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
    emission_path, emissions, states, state_matrix,\
    emission_matrix, state_to_index, emission_to_index = read_input()
    probability = compute_path_probability(emission_path, 
            state_matrix, 
            emission_matrix, 
            state_to_index, 
            emission_to_index,
            states)
    
    print(probability)